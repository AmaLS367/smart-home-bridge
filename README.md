# Smart Home Bridge (Fork)

This project is a fork of [Signal Bridge](https://github.com/AletheiaVox/signal_bridge).
The original version contains full documentation for controlling intimate hardware via MCP.

This fork is focused on extending functionality for **Smart Home** integration and household devices.

## Smart Home Functionality

The following MCP tools are implemented in this version:

### 📺 Chromecast Control
Control Google Chromecast media devices on your local network:
- Discover devices.
- Play YouTube videos (search via `yt-dlp`).
- Playback control (pause, resume, volume).
- Open applications (Netflix, Spotify, etc.).

### ⚖️ BLE Scales
Integration with smart scales via Bluetooth Low Energy (BLE):
- Scan for scales in range.
- Real-time weight reading (support for Xiaomi Mi Scale and others).

## Installation & Setup

1. Install dependencies:
   ```bash
   pip install -e ".[dev]"
   ```
2. Configure environment variables in `.env` (if required).
3. Run the desired MCP server:
   ```bash
   python smart_home_mcp.py
   ```

## Code Quality
The project is configured with `ruff` and `mypy`. To run checks:
```bash
ruff check .
mypy . --ignore-missing-imports
```
