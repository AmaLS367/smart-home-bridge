"""
FastMCP server for Smart Home Integration.
"""
from typing import List, Dict, Optional
from mcp.server.fastmcp import FastMCP
from smart_home import chromecast
from smart_home import ble_scales

# Initialize FastMCP server
mcp = FastMCP("Smart Home Bridge")

@mcp.tool()
def cast_list_devices() -> List[str]:
    """Find all Chromecasts on the local network."""
    return chromecast.discover()

@mcp.tool()
def cast_play_youtube(video_query: str, device_name: Optional[str] = None) -> str:
    """Search for a video via yt-dlp and play it on the Chromecast."""
    chromecast.play_youtube(video_query, device_name)
    return f"Playing '{video_query}' on {device_name or 'default cast'}"

@mcp.tool()
def cast_pause(device_name: Optional[str] = None) -> str:
    """Pause playback on Chromecast."""
    chromecast.pause(device_name)
    return "Paused"

@mcp.tool()
def cast_resume(device_name: Optional[str] = None) -> str:
    """Resume playback on Chromecast."""
    chromecast.resume(device_name)
    return "Resumed"

@mcp.tool()
def cast_stop(device_name: Optional[str] = None) -> str:
    """Stop playback and quit the app on Chromecast."""
    chromecast.stop(device_name)
    return "Stopped"

@mcp.tool()
def cast_set_volume(level: float, device_name: Optional[str] = None) -> str:
    """Set volume (0.0 to 1.0) on Chromecast."""
    chromecast.set_volume(level, device_name)
    return f"Volume set to {level}"

@mcp.tool()
def cast_open_app(app_name: str, device_name: Optional[str] = None) -> str:
    """Open an application by name on Chromecast (e.g., youtube, netflix, spotify)."""
    chromecast.open_app(app_name, device_name)
    return f"Opened {app_name}"

@mcp.tool()
def scales_scan() -> List[Dict[str, str]]:
    """Find BLE scales in range."""
    return ble_scales.scan()

@mcp.tool()
def scales_read_weight(address: Optional[str] = None) -> float:
    """Connect/listen and read weight from the scale in kg."""
    return ble_scales.read_weight(address)

if __name__ == "__main__":
    mcp.run()
