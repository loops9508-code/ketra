# Ketra

**Ultra Smooth Media Player** by Vedansh Mandloi

Play YouTube, Instagram, local videos and images with hardware acceleration, full controls and almost zero lag.

---

## Features

- YouTube, Instagram, TikTok and most yt-dlp supported sites
- **Playlist support** (YouTube playlists + local .m3u / .txt)
- Queue system (`add`, `play`, `list`, `clear`)
- Local video files (mp4, mkv, webm, avi, etc.)
- Local images (jpg, png, webp, gif…)
- Hardware decoding + large cache → smooth playback
- Speed control, seek, volume, fullscreen, next/prev in playlist
- After a single video ends → popup asks for the next URL / path
- Windows, macOS and Linux support
- First-run auto setup for yt-dlp
- Clean terminal UI

---

## Requirements

- Python 3.9 or newer
- mpv (the actual player)
- yt-dlp (auto-downloaded by the app on first run)

---

## Installation

### 1. Get the project

```bash
git clone https://github.com/YOUR_USERNAME/ketra.git
cd ketra
```

Or just download the zip and extract it.

### 2. Install mpv (one time)

#### Windows (recommended)

```bash
winget install -e --id mpv-player.mpv-CI.MSVC
```

Alternative:

```bash
winget install -e --id mpv.mpv
```

#### macOS

```bash
brew install mpv yt-dlp
```

#### Linux (Ubuntu / Debian / Pop!_OS / Mint)

```bash
sudo apt update
sudo apt install mpv
```

#### Linux (Arch / Manjaro)

```bash
sudo pacman -S mpv
```

### 3. Run

```bash
python app.py
```

On first run the app will automatically download `yt-dlp` into the `ketra_bin` folder.

---

## Usage

```text
ketra › https://www.youtube.com/watch?v=dQw4w9WgXcQ
```

or

```text
ketra › C:\Videos\movie.mp4
```

or

```text
ketra › ./photo.jpg
```

You can also launch directly:

```bash
python app.py "https://youtube.com/watch?v=...."
python app.py "path/to/video.mkv"
```

### Player Controls

| Key          | Action                  |
|--------------|-------------------------|
| `Space`      | Play / Pause            |
| `←` `→`      | Seek ±5 seconds         |
| `↑` `↓`      | Seek ±60 seconds        |
| `[` `]`      | Speed slower / faster   |
| `>` / `<`    | Next / Previous (playlist) |
| `f`          | Fullscreen              |
| `m`          | Mute                    |
| `9` `0`      | Volume down / up        |
| `s`          | Screenshot              |
| `q` / `Esc`  | Close player            |

### Playlist & Queue Commands

```text
ketra › help                 # show all commands
ketra › add <url or path>    # add to queue
ketra › list                 # show queue
ketra › play                 # play entire queue
ketra › clear                # clear queue
```

**YouTube playlist** — just paste the playlist URL, Ketra will play the whole list with native next/prev support.

**Local playlist** — create a `.m3u` or `.txt` file with one URL/path per line and paste the file path.

When a single video finishes, a popup (or terminal prompt) appears so you can paste the next URL or local path.

---

## Project Structure

```text
ketra/
├── app.py          ← main program
├── LICENSE.txt
├── README.md
└── ketra_bin/      ← auto-created (yt-dlp + optional portable mpv)
```

---

## License

See [LICENSE.txt](LICENSE.txt)

- Free for personal use, learning, testing and modification
- **Commercial use is not allowed**

Copyright (c) 2026 Vedansh Mandloi

---

## Notes

- This project is made for fun and personal use.
- Quality and smoothness depend on your internet and hardware.
- For best results keep both mpv and yt-dlp updated.
