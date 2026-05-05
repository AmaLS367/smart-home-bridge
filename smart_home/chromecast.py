import logging
from typing import List, Optional, Dict, Any, cast

import pychromecast
from pychromecast.controllers.youtube import YouTubeController
import yt_dlp

logger = logging.getLogger(__name__)

# Global state to keep track of discovered casts
_chromecasts: Dict[str, pychromecast.Chromecast] = {}

def discover() -> List[str]:
    """Find all Chromecasts on the local network."""
    global _chromecasts
    
    logger.info("Discovering Chromecasts...")
    chromecasts, browser = pychromecast.get_listed_chromecasts(friendly_names=None)
    
    _chromecasts = {cast.name: cast for cast in chromecasts if cast.name is not None}
    pychromecast.stop_discovery(browser)
    
    return list(_chromecasts.keys())

def _get_cast(device_name: Optional[str] = None) -> pychromecast.Chromecast:
    if not _chromecasts:
        discover()
        
    if not _chromecasts:
        raise ValueError("No Chromecast devices found on the network.")
        
    if device_name:
        if device_name not in _chromecasts:
            raise ValueError(f"Chromecast '{device_name}' not found.")
        device_cast = _chromecasts[device_name]
    else:
        # Get the first one
        device_cast = list(_chromecasts.values())[0]
        
    device_cast.wait()
    return device_cast

def play_youtube(video_query: str, device_name: Optional[str] = None):
    """Search for a video via yt-dlp and play it on the Chromecast."""
    device_cast = _get_cast(device_name)
    
    ydl_opts: Dict[str, Any] = {
        'format': 'best',
        'noplaylist': True,
        'extract_flat': True,
    }
    
    if not video_query.startswith("http"):
        query = f"ytsearch:{video_query}"
    else:
        query = video_query
        
    logger.info(f"Searching YouTube for: {query}")
    with yt_dlp.YoutubeDL(cast(Any, ydl_opts)) as ydl:
        info = ydl.extract_info(query, download=False)
        if info and 'entries' in info:
            entries = list(cast(Any, info['entries']))
            if entries:
                video_id = entries[0].get('id')
            else:
                video_id = None
        elif info:
            video_id = info.get('id')
        else:
            video_id = None
            
    if not video_id:
        raise ValueError("Could not find a video matching the query.")
        
    logger.info(f"Playing YouTube video ID: {video_id}")
    yt = YouTubeController()
    device_cast.register_handler(yt)
    yt.play_video(video_id)

def pause(device_name: Optional[str] = None):
    """Pause playback."""
    device_cast = _get_cast(device_name)
    device_cast.media_controller.pause()

def resume(device_name: Optional[str] = None):
    """Resume playback."""
    device_cast = _get_cast(device_name)
    device_cast.media_controller.play()

def stop(device_name: Optional[str] = None):
    """Stop playback and quit the app."""
    device_cast = _get_cast(device_name)
    device_cast.quit_app()

def set_volume(level: float, device_name: Optional[str] = None):
    """Set volume (0.0 to 1.0)."""
    device_cast = _get_cast(device_name)
    device_cast.set_volume(level)

def open_app(app_name: str, device_name: Optional[str] = None):
    """Open an application by name."""
    device_cast = _get_cast(device_name)
    
    # Map common app names to their Chromecast App IDs
    app_id_map = {
        "youtube": "233637DE", # pychromecast YouTube app ID
        "netflix": "CA5E8412",
        "spotify": "CC32E753",
    }
    
    app_id = app_id_map.get(app_name.lower())
    if not app_id:
        raise ValueError(f"Unknown app name: {app_name}. Supported apps: {list(app_id_map.keys())}")
        
    device_cast.start_app(app_id)
