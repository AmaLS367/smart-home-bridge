import logging
import asyncio
from typing import List, Dict, Optional

from bleak import BleakScanner

logger = logging.getLogger(__name__)

# Known scale service UUIDs or names
MI_SCALE_V1_NAME = "MI SCALE"
MI_SCALE_V2_NAME = "MIBFS"
WITHINGS_NAME_PREFIX = "Withings"

# Service UUIDs for Mi Scale
MI_SCALE_SERVICE = "0000181d-0000-1000-8000-00805f9b34fb"

def _is_scale(device) -> bool:
    name = device.name or ""
    if name in [MI_SCALE_V1_NAME, MI_SCALE_V2_NAME]:
        return True
    if name.startswith(WITHINGS_NAME_PREFIX):
        return True
    
    # Check advertised services if available
    metadata_uuids = device.metadata.get("uuids", [])
    if MI_SCALE_SERVICE in metadata_uuids:
        return True
        
    return False

async def _scan_async() -> List[Dict[str, str]]:
    logger.info("Scanning for BLE scales...")
    devices = await BleakScanner.discover(timeout=5.0)
    scales = []
    for d in devices:
        if _is_scale(d):
            scales.append({
                "address": d.address,
                "name": d.name or "Unknown Scale",
                "rssi": d.rssi
            })
    return scales

def scan() -> List[Dict[str, str]]:
    """Find BLE scales in range."""
    return asyncio.run(_scan_async())

async def _read_weight_async(address: Optional[str]) -> float:
    """Read weight by listening to BLE advertisements."""
    logger.info(f"Scanning to read weight from {address or 'any scale'}...")
    
    weight = None
    
    def detection_callback(device, advertisement_data):
        nonlocal weight
        if address and device.address.lower() != address.lower():
            return
            
        if not _is_scale(device):
            return
            
        # Parse Xiaomi Mi Scale V2 (Miscale 2) advertisement data
        # Service Data UUID usually 0000181b-0000-1000-8000-00805f9b34fb
        service_data = advertisement_data.service_data
        for uuid, data in service_data.items():
            if uuid.startswith("0000181b") or uuid.startswith("0000181d"):
                # simplified parse for Mi Scale
                if len(data) >= 13:
                    # Weight is usually in bytes 11 and 12 for V2
                    raw_weight = int.from_bytes(data[11:13], byteorder='little')
                    # Scale unit check (byte 0)
                    # Simplified parsing for demonstration
                    weight_kg = raw_weight * 0.005 
                    weight = weight_kg

    scanner = BleakScanner(detection_callback)
    await scanner.start()
    
    # Wait for scale to broadcast (e.g. someone steps on it)
    for _ in range(10): # up to 10 seconds
        await asyncio.sleep(1.0)
        if weight is not None:
            break
            
    await scanner.stop()
    
    if weight is not None:
        return round(weight, 2)
        
    raise TimeoutError("Could not read weight data. Make sure to step on the scale.")

def read_weight(address: Optional[str] = None) -> float:
    """Connect/listen and read weight from the scale."""
    return asyncio.run(_read_weight_async(address))
