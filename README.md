# iPod Music Sync

A command-line tool that automates getting new music onto a Rockboxed iPod — download from YouTube, standardize the audio format, and copy straight to the device.

## Why I built this

I wanted a seamless way to keep my iPod's music library organized without manually downloading, converting, and dragging files over every time I found something new. This script handles the whole pipeline from a single menu.

## What it does

1. **Queue management** — add artists/albums/singles to a queue, view or remove entries before running anything
2. **Download** — pulls audio from a YouTube link using `yt-dlp`, extracted as FLAC
3. **Convert** — normalizes every file to 44.1kHz / 16-bit sample format with `ffmpeg` so everything is consistent and playable on the device
4. **Sync** — copies the finished files into the iPod's music folder

You can run the whole pipeline for one queued item or batch-process the entire queue at once.

## How it works

Run the script and use the menu to:

```
1) Display Queue
2) Add to Queue
3) Remove from Queue
4) Execute ONE   — download, convert, and copy a single queued item
5) Execute ALL   — run the full pipeline for everything in the queue
0) Quit
```

Each queue entry stores the artist, the YouTube link, whether it's an album or single, and the release name.

## Requirements

- Python 3
- [`yt-dlp`](https://github.com/yt-dlp/yt-dlp)
- [`ffmpeg`](https://ffmpeg.org/)
- A mounted iPod (or any target folder) with a known file path

## Setup

Edit the two paths at the top of the script before running:

```python
DOWNLOAD_PATH = "/Users/yourname/Music/Downloads"
IPOD_PATH = "/Volumes/YOUR-IPOD-NAME/Music"
```

Then run:

```bash
python3 ipod.py
```

## Notes

This was built for personal use to solve a real, recurring annoyance — manually managing files for an offline music player. It's intentionally simple (no external config files, no GUI) since the goal was a fast, no-friction way to get music onto the device, not a polished product.
