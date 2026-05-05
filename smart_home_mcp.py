"""
FastMCP server for Smart Home Integration.
"""
import sys
import asyncio
from functools import partial
from typing import Optional
from mcp.server.fastmcp import FastMCP
from smart_home import chromecast
from smart_home import ble_scales
from smart_home import android_tv

# Initialize FastMCP server
mcp = FastMCP("Smart Home Bridge")

print("Smart Home Bridge starting...", file=sys.stderr)

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

@mcp.tool()
async def tv_connect() -> str:
    """Connect to Android TV over Wi-Fi."""
    try:
        return await asyncio.get_event_loop().run_in_executor(None, android_tv.connect)
    except Exception as e:
        return f"Error: {e}"

@mcp.tool()
async def tv_key(keycode: str) -> str:
    """Send a keycode to the TV (e.g., KEYCODE_HOME, KEYCODE_BACK, KEYCODE_DPAD_UP)."""
    try:
        return await asyncio.get_event_loop().run_in_executor(None, partial(android_tv.send_key, keycode))
    except Exception as e:
        return f"Error: {e}"

@mcp.tool()
async def tv_open_app(package_name: str) -> str:
    """Open an app by package name (e.g., com.google.android.youtube.tv)."""
    try:
        return await asyncio.get_event_loop().run_in_executor(None, partial(android_tv.open_app, package_name))
    except Exception as e:
        return f"Error: {e}"

@mcp.tool()
async def tv_play_youtube(query: str) -> str:
    """Search and play a video on YouTube on the TV."""
    try:
        return await asyncio.get_event_loop().run_in_executor(None, partial(android_tv.play_youtube, query))
    except Exception as e:
        return f"Error: {e}"

@mcp.tool()
async def tv_get_current_app() -> str:
    """Get the currently focused app's package name."""
    try:
        return await asyncio.get_event_loop().run_in_executor(None, android_tv.get_current_app)
    except Exception as e:
        return f"Error: {e}"

@mcp.tool()
async def tv_volume_set(level: int) -> str:
    """Set TV volume level (0-15)."""
    try:
        return await asyncio.get_event_loop().run_in_executor(None, partial(android_tv.volume_set, level))
    except Exception as e:
        return f"Error: {e}"

if __name__ == "__main__":
    mcp.run()
