import logging
import asyncio
from typing import List, Dict, Optional

from bleak import BleakScanner
from bleak.backends.device import BLEDevice

logger = logging.getLogger(__name__)

# Known scale service UUIDs or names
MI_SCALE_V1_NAME = "MI SCALE"
MI_SCALE_V2_NAME = "MIBFS"
WITHINGS_NAME_PREFIX = "Withings"

# Service UUIDs for Mi Scale
MI_SCALE_SERVICE = "0000181d-0000-1000-8000-00805f9b34fb"

def _is_scale(device: BLEDevice, advertisement_data) -> bool:
    name = device.name or ""
    if name in [MI_SCALE_V1_NAME, MI_SCALE_V2_NAME]:
        return True
    if name.startswith(WITHINGS_NAME_PREFIX):
        return True
    
    # Chipsea scale detection
    for company_id, data in advertisement_data.manufacturer_data.items():
        if len(data) >= 2 and data[0] == 0x02 and data[1] == 0xF8:
            return True

    # Check advertised services if available
    metadata_uuids = advertisement_data.service_uuids
    if MI_SCALE_SERVICE in metadata_uuids:
        return True
        
    return False

async def scan() -> List[Dict[str, str]]:
    """Find BLE scales in range."""
    logger.info("Scanning for BLE scales...")
    scales: List[Dict[str, str]] = []
    
    def detection_callback(device, advertisement_data):
        if _is_scale(device, advertisement_data):
            # Avoid duplicates
            if not any(s["address"] == device.address for s in scales):
                scales.append({
                    "address": device.address,
                    "name": device.name or "Unknown Scale",
                    "rssi": str(getattr(device, "rssi", 0))
                })

    scanner = BleakScanner(detection_callback)
    await scanner.start()
    await asyncio.sleep(5.0)
    await scanner.stop()
    return scales

async def read_weight(address: Optional[str] = None, timeout: int = 30) -> float:
    """Read weight by listening to BLE advertisements."""
    logger.info(f"Scanning to read weight from {address or 'any scale'}...")
    
    weight = None
    
    def detection_callback(device, advertisement_data):
        nonlocal weight
        if address and device.address.lower() != address.lower():
            return
            
        if not _is_scale(device, advertisement_data):
            return
            
        # Chipsea scale weight parsing
        for company_id, data in advertisement_data.manufacturer_data.items():
            if len(data) >= 13 and data[0] == 0x02 and data[1] == 0xF8:
                raw = (data[11] << 8) | data[12]
                weight_kg = raw / 100.0
                if weight_kg > 5.0:
                    weight = weight_kg
                    return

        # Fallback to Mi Scale service data if present
        service_data = advertisement_data.service_data
        for uuid, data in service_data.items():
            if uuid.startswith("0000181b") or uuid.startswith("0000181d"):
                if len(data) >= 13:
                    # Weight is usually in bytes 11 and 12 for V2
                    raw_weight = int.from_bytes(data[11:13], byteorder='little')
                    weight_kg = raw_weight * 0.005 
                    if weight_kg > 5.0:
                        weight = weight_kg
                        return

    scanner = BleakScanner(detection_callback)
    await scanner.start()
    
    # Wait for scale to broadcast (e.g. someone steps on it)
    for _ in range(timeout):
        await asyncio.sleep(1.0)
        if weight is not None:
            break
            
    await scanner.stop()
    
    if weight is not None:
        return round(weight, 2)
        
    return -1.0
