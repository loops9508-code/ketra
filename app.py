#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ketra - Ultra Smooth Media Player
=================================
Author  : Vedansh Mandloi
Version : 1.5.0

Copyright (c) 2026 Vedansh Mandloi
This software is provided for personal use, testing, learning,
modification and fun only. Commercial use is strictly prohibited
without prior written permission from the author.

License: See LICENSE.txt
"""

from __future__ import annotations

import os
import sys
import shutil
import subprocess
import platform
import urllib.request
import time
import traceback
from pathlib import Path
from typing import Optional, List

# Optional GUI
HAS_TK = False
try:
    import tkinter as tk
    from tkinter import simpledialog, messagebox, ttk
    HAS_TK = True
except Exception:
    HAS_TK = False

# ──────────────────────────────────────────────
# Paths & Constants
# ──────────────────────────────────────────────
BASE_DIR = Path(__file__).parent.resolve()
BIN_DIR = BASE_DIR / "ketra_bin"
IS_WINDOWS = platform.system() == "Windows"
YTDLP_NAME = "yt-dlp.exe" if IS_WINDOWS else "yt-dlp"
YTDLP_PATH = BIN_DIR / YTDLP_NAME

VERSION = "1.5.0"
AUTHOR = "Vedansh Mandloi"

queue: List[str] = []

# ──────────────────────────────────────────────
# Colors
# ──────────────────────────────────────────────
class C:
    CYAN   = "\033[96m"
    GREEN  = "\033[92m"
    YELLOW = "\033[93m"
    RED    = "\033[91m"
    BOLD   = "\033[1m"
    DIM    = "\033[2m"
    END    = "\033[0m"

def clear_screen():
    os.system("cls" if IS_WINDOWS else "clear")

def banner():
    # Simple clean banner - works on all terminals
    print()
    print(C.CYAN + C.BOLD + "  ╔══════════════════════════════════════════╗" + C.END)
    print(C.CYAN + C.BOLD + "  ║                                          ║" + C.END)
    print(C.CYAN + C.BOLD + "  ║              K E T R A                   ║" + C.END)
    print(C.CYAN + C.BOLD + "  ║                                          ║" + C.END)
    print(C.CYAN + C.BOLD + "  ║       Ultra Smooth Media Player          ║" + C.END)
    print(C.CYAN + C.BOLD + "  ║          by Vedansh Mandloi              ║" + C.END)
    print(C.CYAN + C.BOLD + "  ║               v" + VERSION + "                     ║" + C.END)
    print(C.CYAN + C.BOLD + "  ║                                          ║" + C.END)
    print(C.CYAN + C.BOLD + "  ╚══════════════════════════════════════════╝" + C.END)
    print()

def info(msg: str):
    print(C.CYAN + msg + C.END)

def success(msg: str):
    print(C.GREEN + msg + C.END)

def warn(msg: str):
    print(C.YELLOW + msg + C.END)

def error(msg: str):
    print(C.RED + msg + C.END)

def dim(msg: str):
    print(C.DIM + msg + C.END)

# ──────────────────────────────────────────────
# Controls / Guidance Popup
# ──────────────────────────────────────────────
def show_controls_popup():
    """Clean guidance window with all controls and commands."""
    text = """KETRA CONTROLS & GUIDE
======================

PLAYER CONTROLS (focus the video window)
---------------------------------------
  Space          Play / Pause
  Left / Right   Seek 5 seconds
  Up / Down      Seek 60 seconds
  [  ]           Speed slower / faster
  >  <           Next / Previous (playlist)
  f              Fullscreen
  m              Mute
  9 / 0          Volume down / up
  s              Screenshot
  q / Esc        Close player

TERMINAL COMMANDS
-----------------
  <url or path>      Play immediately
  add <url/path>     Add to queue
  list               Show queue
  play               Play entire queue
  clear              Clear queue
  help               Show help
  controls           Open this guide
  q / quit           Exit

PLAYLIST SUPPORT
----------------
  • Paste YouTube playlist URL → full playlist
  • Local .m3u / .txt file → loads & plays
  • Use "add" then "play" for custom queue

TIPS
----
  • After a single video ends, you can paste next URL
  • Keep player window focused for keyboard controls
  • For best quality keep internet stable

Ketra v{ver}  •  by {author}
Personal use only • Not for commercial use
""".format(ver=VERSION, author=AUTHOR)

    if HAS_TK:
        try:
            root = tk.Tk()
            root.title("Ketra — Controls & Guide")
            root.geometry("520x580")
            root.resizable(True, True)
            try:
                root.attributes("-topmost", True)
            except Exception:
                pass

            frame = tk.Frame(root, padx=12, pady=10)
            frame.pack(fill="both", expand=True)

            txt = tk.Text(frame, wrap="word", font=("Consolas", 10), bg="#1e1e1e", fg="#d4d4d4",
                          insertbackground="white", relief="flat", padx=8, pady=8)
            txt.pack(fill="both", expand=True)
            txt.insert("1.0", text)
            txt.config(state="disabled")

            btn = tk.Button(frame, text="Close", command=root.destroy, width=12)
            btn.pack(pady=8)

            root.mainloop()
            return
        except Exception as e:
            dim("(popup failed: {})".format(e))

    # Terminal fallback
    print()
    print(text)

# ──────────────────────────────────────────────
# Download
# ──────────────────────────────────────────────
def download_file(url: str, dest: Path, desc: str = "Downloading") -> bool:
    print("  " + C.YELLOW + desc + "..." + C.END)
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Ketra/" + VERSION})
        with urllib.request.urlopen(req, timeout=120) as resp:
            total = int(resp.headers.get("Content-Length", 0))
            dest.parent.mkdir(parents=True, exist_ok=True)
            downloaded = 0
            block = 256 * 1024
            with open(dest, "wb") as f:
                while True:
                    chunk = resp.read(block)
                    if not chunk:
                        break
                    f.write(chunk)
                    downloaded += len(chunk)
                    if total > 0:
                        pct = min(100, downloaded * 100 // total)
                        bar_len = 32
                        filled = int(bar_len * downloaded / total)
                        bar = "#" * filled + "-" * (bar_len - filled)
                        print("\r  [" + bar + "] " + str(pct) + "%", end="", flush=True)
        print("\n  " + C.GREEN + "OK" + C.END)
        return True
    except Exception as e:
        error("  Download failed: " + str(e))
        return False

# ──────────────────────────────────────────────
# Tools
# ──────────────────────────────────────────────
def find_mpv() -> Optional[str]:
    pattern = "mpv.exe" if IS_WINDOWS else "mpv"
    try:
        for p in BIN_DIR.rglob(pattern):
            if p.is_file():
                return str(p)
    except Exception:
        pass
    return shutil.which("mpv")

def find_ytdlp() -> Optional[str]:
    if YTDLP_PATH.exists():
        return str(YTDLP_PATH)
    return shutil.which("yt-dlp") or shutil.which("youtube-dl")

def setup_ytdlp() -> bool:
    if find_ytdlp():
        return True
    info("First-time setup: downloading yt-dlp ...")
    url = (
        "https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp.exe"
        if IS_WINDOWS
        else "https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp"
    )
    ok = download_file(url, YTDLP_PATH, "yt-dlp")
    if ok and not IS_WINDOWS:
        try:
            YTDLP_PATH.chmod(0o755)
        except Exception:
            pass
    return ok

def try_winget_mpv() -> bool:
    if not IS_WINDOWS:
        return False
    packages = ["mpv-player.mpv-CI.MSVC", "mpv.mpv", "mpv-player.mpv"]
    for pkg in packages:
        print("  Trying winget -> " + pkg)
        try:
            r = subprocess.run(
                ["winget", "install", "-e", "--id", pkg,
                 "--accept-package-agreements", "--accept-source-agreements",
                 "--disable-interactivity"],
                capture_output=True, text=True, timeout=200
            )
            out = ((r.stdout or "") + (r.stderr or "")).lower()
            if r.returncode == 0 or "successfully installed" in out or "already installed" in out:
                success("  mpv ready")
                time.sleep(1.2)
                return True
        except Exception:
            continue
    return False

def print_manual_mpv_help():
    print("""
------------------------------------------------
mpv is required (one-time)

Windows:
  winget install -e --id mpv-player.mpv-CI.MSVC

macOS:
  brew install mpv yt-dlp

Linux (Ubuntu/Debian):
  sudo apt install mpv

Linux (Arch):
  sudo pacman -S mpv

Then close terminal, open NEW one, run: python app.py
------------------------------------------------
""")

def ensure_tools() -> bool:
    info("Checking tools...")
    if not find_ytdlp():
        if not setup_ytdlp():
            error("Could not download yt-dlp. Check internet.")
            return False
    if find_mpv():
        return True
    if try_winget_mpv() and find_mpv():
        return True
    print_manual_mpv_help()
    return False

# ──────────────────────────────────────────────
# Helpers
# ──────────────────────────────────────────────
def is_url(text: str) -> bool:
    t = text.lower().strip()
    return t.startswith(("http://", "https://", "www."))

def is_playlist_url(text: str) -> bool:
    t = text.lower()
    return any(k in t for k in [
        "playlist?list=", "list=", "/playlist/",
        "youtube.com/playlist", "&list=", "?list="
    ])

def is_image(path: str) -> bool:
    return Path(path).suffix.lower() in {
        ".jpg", ".jpeg", ".png", ".webp", ".gif",
        ".bmp", ".tiff", ".tif", ".avif", ".heic"
    }

def is_local_playlist(path: str) -> bool:
    try:
        p = Path(path).expanduser()
        return p.suffix.lower() in {".m3u", ".m3u8", ".txt", ".pls"} and p.is_file()
    except Exception:
        return False

def load_local_playlist(path: str) -> List[str]:
    items: List[str] = []
    p = Path(path).expanduser().resolve()
    try:
        with open(p, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if line.startswith("http") or (len(line) > 1 and line[1] == ":") or line.startswith("/"):
                    items.append(line)
                else:
                    cand = (p.parent / line).resolve()
                    items.append(str(cand) if cand.exists() else line)
    except Exception as e:
        error("Could not read playlist: " + str(e))
    return items

def show_queue():
    if not queue:
        dim("Queue is empty.")
        return
    print("\n" + C.BOLD + "Queue (" + str(len(queue)) + " items):" + C.END)
    for i, item in enumerate(queue, 1):
        short = item if len(item) < 70 else item[:67] + "..."
        print("  " + C.CYAN + str(i).rjust(2) + "." + C.END + " " + short)
    print()

def add_to_queue(item: str):
    item = item.strip().strip('"').strip("'")
    if not item:
        warn("Nothing to add.")
        return
    queue.append(item)
    success("+ Added  (total: " + str(len(queue)) + ")")

# ──────────────────────────────────────────────
# Playback (lightweight flags)
# ──────────────────────────────────────────────
def build_mpv_cmd(mpv: str, ytdlp: Optional[str], target: str, online: bool, playlist_mode: bool = False) -> list:
    # Lightweight but still smooth
    cmd = [
        mpv,
        "--hwdec=auto",
        "--vo=gpu",
        "--cache=yes",
        "--demuxer-max-bytes=120MiB",
        "--force-window=yes",
        "--osc=yes",
        "--volume=85",
        "--input-default-bindings=yes",
        "--input-vo-keyboard=yes",
    ]
    if playlist_mode:
        cmd.append("--loop-playlist=no")
    else:
        cmd.append("--keep-open=yes")

    if online and ytdlp:
        cmd.append("--script-opts=ytdl_hook-ytdl_path=" + ytdlp)
        cmd.append("--ytdl-format=bestvideo[height<=1080]+bestaudio/best")

    cmd.append(target)
    return cmd

def play_one(target: str, playlist_mode: bool = False) -> bool:
    target = target.strip().strip('"').strip("'")
    if not target:
        return False

    mpv = find_mpv()
    ytdlp = find_ytdlp()
    if not mpv:
        error("mpv not found.")
        return False

    online = is_url(target)
    if not online:
        try:
            p = Path(target).expanduser().resolve()
            if not p.exists():
                error("File not found -> " + str(p))
                return False
            target = str(p)
        except Exception as e:
            error("Invalid path: " + str(e))
            return False

    kind = "Playlist" if playlist_mode else ("Streaming" if online else ("Image" if is_image(target) else "Local"))
    success(">> " + kind)
    dim("   " + (target[:100] + "..." if len(target) > 100 else target))
    print()
    print(C.YELLOW + "  Space=Play/Pause  []=Speed  f=Fullscreen  q=Close" + C.END)
    print(C.DIM + "  Type 'controls' anytime for full guide" + C.END)
    print()

    cmd = build_mpv_cmd(mpv, ytdlp, target, online, playlist_mode)
    try:
        subprocess.run(cmd)
        return True
    except FileNotFoundError:
        error("mpv not runnable.")
        return False
    except KeyboardInterrupt:
        warn("Stopped.")
        return True
    except Exception as e:
        error("Playback error: " + str(e))
        return False

def play_queue():
    global queue
    if not queue:
        warn("Queue empty. Use: add <url>")
        return
    total = len(queue)
    success("Playing queue (" + str(total) + " items)")
    idx = 0
    while queue:
        item = queue.pop(0)
        idx += 1
        print("\n" + C.CYAN + "-- " + str(idx) + "/" + str(total) + " --" + C.END)
        play_one(item)
        if queue:
            dim(str(len(queue)) + " left")
    success("Queue finished.")

def ask_next_media() -> Optional[str]:
    if HAS_TK:
        try:
            root = tk.Tk()
            root.withdraw()
            try:
                root.attributes("-topmost", True)
            except Exception:
                pass
            result = simpledialog.askstring(
                "Ketra - Next",
                "Finished!\n\nPaste next URL or local path:\n(Cancel = stop)",
                parent=root
            )
            root.destroy()
            if result and result.strip():
                return result.strip()
            return None
        except Exception:
            pass

    print()
    warn("Finished.")
    try:
        nxt = input(C.CYAN + "Next URL / path (Enter=stop) > " + C.END).strip()
        return nxt if nxt else None
    except (KeyboardInterrupt, EOFError):
        return None

# ──────────────────────────────────────────────
# Commands
# ──────────────────────────────────────────────
def print_help():
    print("""
Commands:
  <url or path>        Play now
  add <url/path>       Add to queue
  list / queue          Show queue
  play / start         Play whole queue
  clear                Clear queue
  controls             Open controls guide (popup)
  help                 This help
  q / quit             Exit

Playlist:
  Paste YouTube playlist URL
  Or local .m3u / .txt file
""")

def handle_command(line: str) -> bool:
    global queue
    line = line.strip()
    if not line:
        return True

    low = line.lower()

    if low in {"q", "quit", "exit", "bye"}:
        success("Bye! - Ketra by " + AUTHOR)
        return False

    if low in {"help", "?", "h"}:
        print_help()
        return True

    if low in {"controls", "control", "guide", "keys"}:
        show_controls_popup()
        return True

    if low in {"list", "queue", "ls"}:
        show_queue()
        return True

    if low in {"clear", "clr"}:
        queue.clear()
        success("Queue cleared.")
        return True

    if low in {"play", "start", "go"}:
        play_queue()
        return True

    if low.startswith("add "):
        item = line[4:].strip()
        if not item:
            warn("Usage: add <url or path>")
            return True
        if is_local_playlist(item):
            entries = load_local_playlist(item)
            if entries:
                queue.extend(entries)
                success("+ Loaded " + str(len(entries)) + " items")
            else:
                warn("No valid entries.")
        else:
            add_to_queue(item)
        return True

    if is_local_playlist(line):
        entries = load_local_playlist(line)
        if not entries:
            error("No valid entries in playlist file.")
            return True
        queue.extend(entries)
        success("Loaded " + str(len(entries)) + " items. Starting...")
        play_queue()
        return True

    if is_url(line) and is_playlist_url(line):
        info("Playlist URL detected")
        play_one(line, playlist_mode=True)
        return True

    played = play_one(line)
    if played:
        nxt = ask_next_media()
        if nxt:
            return handle_command(nxt)
    return True

# ──────────────────────────────────────────────
# Main
# ──────────────────────────────────────────────
def main():
    clear_screen()
    banner()

    if not ensure_tools():
        try:
            input("\nPress Enter to exit...")
        except Exception:
            pass
        sys.exit(1)

    mpv = find_mpv()
    ytdlp = find_ytdlp()
    success("OK  mpv    " + str(mpv))
    success("OK  yt-dlp " + str(ytdlp))
    success("OK  Ketra v" + VERSION + " by " + AUTHOR)
    print()
    print(C.DIM + "Type 'controls' for full guide  |  'help' for commands" + C.END)
    print()

    if len(sys.argv) > 1:
        handle_command(" ".join(sys.argv[1:]))
        return

    print(C.BOLD + "Paste URL / path  or  type a command" + C.END)
    print()

    while True:
        try:
            line = input(C.CYAN + C.BOLD + "ketra > " + C.END)
        except (KeyboardInterrupt, EOFError):
            print()
            success("Bye! - Ketra by " + AUTHOR)
            break
        try:
            if not handle_command(line):
                break
        except Exception as e:
            error("Error: " + str(e))
            traceback.print_exc()
            warn("Continuing...")

if __name__ == "__main__":
    main()
