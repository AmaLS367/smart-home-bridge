"""
FastMCP server for Smart Home Integration.
"""
import asyncio
from functools import partial
from typing import Optional
from mcp.server.fastmcp import FastMCP
from smart_home import chromecast
from smart_home import ble_scales

# Initialize FastMCP server
mcp = FastMCP("Smart Home Bridge")

@mcp.tool()
async def cast_list_devices() -> str:
    """Find all Chromecasts on the local network."""
    try:
        devices = await asyncio.get_event_loop().run_in_executor(None, chromecast.discover)
        return str(devices)
    except Exception as e:
        return f"Error: {e}"

@mcp.tool()
async def cast_play_youtube(video_query: str, device_name: Optional[str] = None) -> str:
    """Search for a video via yt-dlp and play it on the Chromecast."""
    try:
        await asyncio.get_event_loop().run_in_executor(
            None, partial(chromecast.play_youtube, video_query, device_name)
        )
        return f"Playing '{video_query}' on {device_name or 'default cast'}"
    except Exception as e:
        return f"Error: {e}"

@mcp.tool()
async def cast_pause(device_name: Optional[str] = None) -> str:
    """Pause playback on Chromecast."""
    try:
        await asyncio.get_event_loop().run_in_executor(None, partial(chromecast.pause, device_name))
        return "Paused"
    except Exception as e:
        return f"Error: {e}"

@mcp.tool()
async def cast_resume(device_name: Optional[str] = None) -> str:
    """Resume playback on Chromecast."""
    try:
        await asyncio.get_event_loop().run_in_executor(None, partial(chromecast.resume, device_name))
        return "Resumed"
    except Exception as e:
        return f"Error: {e}"

@mcp.tool()
async def cast_stop(device_name: Optional[str] = None) -> str:
    """Stop playback and quit the app on Chromecast."""
    try:
        await asyncio.get_event_loop().run_in_executor(None, partial(chromecast.stop, device_name))
        return "Stopped"
    except Exception as e:
        return f"Error: {e}"

@mcp.tool()
async def cast_set_volume(level: float, device_name: Optional[str] = None) -> str:
    """Set volume (0.0 to 1.0) on Chromecast."""
    try:
        await asyncio.get_event_loop().run_in_executor(None, partial(chromecast.set_volume, level, device_name))
        return f"Volume set to {level}"
    except Exception as e:
        return f"Error: {e}"

@mcp.tool()
async def cast_open_app(app_name: str, device_name: Optional[str] = None) -> str:
    """Open an application by name on Chromecast (e.g., youtube, netflix, spotify)."""
    try:
        await asyncio.get_event_loop().run_in_executor(None, partial(chromecast.open_app, app_name, device_name))
        return f"Opened {app_name}"
    except Exception as e:
        return f"Error: {e}"

@mcp.tool()
async def scales_scan() -> str:
    """Find BLE scales in range."""
    try:
        scales = await ble_scales.scan()
        return str(scales)
    except Exception as e:
        return f"Error: {e}"

@mcp.tool()
async def scales_read_weight(address: Optional[str] = None) -> str:
    """Connect/listen and read weight from the scale in kg."""
    try:
        result = await ble_scales.read_weight(address)
        if result == -1.0:
            return "Could not read weight. Make sure you are standing on the scale and it is in range."
        return f"Weight: {result} kg"
    except Exception as e:
        return f"Error: {e}"

if __name__ == "__main__":
    mcp.run()
