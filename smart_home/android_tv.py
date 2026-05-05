import os
import subprocess
import urllib.parse
from dotenv import load_dotenv

load_dotenv()

ADB_PATH = os.getenv("ADB_PATH", "adb")
TV_IP = os.getenv("ANDROID_TV_IP")
TV_PORT = os.getenv("ANDROID_TV_PORT", "5555")

# Common Keycodes:
# KEYCODE_HOME, KEYCODE_BACK, KEYCODE_DPAD_UP, KEYCODE_DPAD_DOWN, 
# KEYCODE_DPAD_LEFT, KEYCODE_DPAD_RIGHT, KEYCODE_DPAD_CENTER, 
# KEYCODE_VOLUME_UP, KEYCODE_VOLUME_DOWN, KEYCODE_MUTE, 
# KEYCODE_MEDIA_PLAY_PAUSE, KEYCODE_MEDIA_STOP, KEYCODE_MEDIA_NEXT, KEYCODE_MEDIA_PREVIOUS

# Common Packages:
# YouTube: com.google.android.youtube.tv
# Netflix: com.netflix.ninja
# Spotify: com.spotify.tv.android
# Prime Video: com.amazon.amazonvideo.livingroom

def _run_adb_cmd(args: list[str]) -> str:
    """Helper to run adb commands via subprocess."""
    try:
        cmd = [ADB_PATH] + args
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return f"ADB Error: {e.stderr.strip() or str(e)}"
    except Exception as e:
        return f"Error: {str(e)}"

def connect() -> str:
    """Connect to Android TV over Wi-Fi."""
    if not TV_IP:
        return "Error: ANDROID_TV_IP not set in environment."
    return _run_adb_cmd(["connect", f"{TV_IP}:{TV_PORT}"])

def send_key(keycode: str) -> str:
    """Send a keyevent to the TV."""
    return _run_adb_cmd(["shell", "input", "keyevent", keycode])

def open_app(package_name: str) -> str:
    """Open an application by its package name."""
    # Using monkey to launch the app's launcher category
    return _run_adb_cmd(["shell", "monkey", "-p", package_name, "-c", "android.intent.category.LAUNCHER", "1"])

def play_youtube(query: str) -> str:
    """Search and play a video on YouTube via deep link."""
    encoded_query = urllib.parse.quote(query)
    url = f"https://www.youtube.com/results?search_query={encoded_query}"
    return _run_adb_cmd([
        "shell", "am", "start", "-a", "android.intent.action.VIEW", 
        "-d", url, "com.google.android.youtube.tv"
    ])

def get_current_app() -> str:
    """Find the currently focused package name."""
    output = _run_adb_cmd(["shell", "dumpsys", "window", "windows"])
    if "Error" in output:
        return output
    
    # Simple parsing for focused app
    for line in output.splitlines():
        if "mCurrentFocus" in line or "mFocusedApp" in line:
            parts = line.split("/")
            if len(parts) > 0:
                # Extract package name from "...package/activity..."
                package_part = parts[0].split()[-1]
                return package_part
    return "Could not determine focused app"

def volume_set(level: int) -> str:
    """Set absolute volume level (0-15)."""
    if not (0 <= level <= 15):
        return "Error: Volume level must be between 0 and 15"
    return _run_adb_cmd(["shell", "media", "volume", "--stream", "3", "--set", str(level)])
