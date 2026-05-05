# Smart Home Bridge
Give Claude control over your smart home devices.

## What this fork adds

### Signal Bridge (original)
- Intimate hardware control via Intiface Central
- vibrate/pulse/wave/escalate tools
- Safety governor with heat tracking

### Smart Home (this fork)
- Google Nest / Chromecast control (play YouTube, pause, volume, open apps)
- BLE smart scales (Chipsea/OKOK protocol, weight reading)

## Requirements

### Signal Bridge requirements
- Python 3.10+
- Intiface Central running on port 12345

### Smart Home requirements
- Python 3.10+
- Google Nest or Chromecast on local network
- BLE smart scale compatible with OKOK International app (Chipsea chip)

## Installation
```bash
pip install mcp buttplug python-dotenv pychromecast bleak yt-dlp
```
*Note: or use pip install -e ".[dev]" from pyproject.toml.*

## Claude Desktop config
Configure your `claude_desktop_config.json` as follows:
```json
{
  "mcpServers": {
    "signal-bridge": {
      "command": "python",
      "args": ["C:\\path\\to\\smart-home-bridge\\signal_bridge_mcp.py"]
    },
    "smart-home": {
      "command": "python",
      "args": ["C:\\path\\to\\smart-home-bridge\\smart_home_mcp.py"]
    }
  }
}
```
*Note: paths must be absolute and on Windows use double backslashes.*

## Available tools

### Signal Bridge tools
| Tool | Description |
| :--- | :--- |
| list_devices | List all connected intimate hardware. |
| vibrate | Start vibration on a device. |
| rotate | Start rotation on a device. |
| oscillate | Start oscillation on a device. |
| pulse | Perform a pulsing pattern. |
| wave | Perform a waving pattern. |
| escalate | Gradually increase intensity. |
| stop | Stop all activity on a device. |
| scan_devices | Trigger a device scan in Intiface. |
| safety_status | View current heat level and session stats. |

### Smart Home tools
| Tool | Description |
| :--- | :--- |
| cast_list_devices | Find all Chromecasts on the local network. |
| cast_play_youtube | Search and play a video on Chromecast. |
| cast_pause | Pause playback on Chromecast. |
| cast_resume | Resume playback on Chromecast. |
| cast_stop | Stop playback and quit the app. |
| cast_set_volume | Set volume (0.0 to 1.0) on Chromecast. |
| cast_open_app | Open an app (YouTube, Netflix, etc.) on Chromecast. |
| scales_scan | Find BLE scales in range. |
| scales_read_weight | Read weight from a smart scale in kg. |

## Supported devices
- **Chromecast**: Any Google Chromecast or Nest device on local network.
- **Scales**: Any scale compatible with OKOK International app (Chipsea chip) — these advertise via BLE manufacturer data with prefix `0x02 0xF8`.

## Credits
Original [Signal Bridge](https://github.com/AletheiaVox/signal_bridge) by AletheiaVox.
Built on [buttplug.io](https://buttplug.io) and MCP by Anthropic.
