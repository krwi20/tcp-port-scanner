# TCP Port Scanner (v1, Python)

A **simple TCP port scanner** written in Python. It scans a target host over a given port range, prints progress, looks up common service names, and writes a timestamped report with a neat summary.

> **Ethical use only:** scan only systems you own/control or have explicit permission to test.

## What this v1 does
- Scan a **single port or a range** (TCP).
- **Hostname → IP** resolution.
- **Progress pulse** with percentage.
- **Duration + summary** at the end.
- **Service name lookup** (e.g., `80 → http`, `22 → ssh`, `631 → ipp`).
- **Timestamped report files**: `scan_<ip>_<YYYYMMDD-HHMMSS>.txt`.
- **Passive** banner read (one quick read) for protocols that greet immediately (e.g., SSH/FTP/SMTP).  
  *No HTTP-specific probing in v1.*

## Requirements
- Python 3 (standard library only; no extra packages).

## Usage
Interactive run:
```bash
python3 portscan.py
# Enter target (e.g. localhost or 127.0.0.1)
# Enter start port (e.g. 1)
# Enter end port   (e.g. 1024)
```

Example output (abridged):
```
Target: localhost (127.0.0.1)
Saving results to scan_127_0_0_1_20250913-143209.txt
Port 22 (ssh) is OPEN | banner: "SSH-2.0-OpenSSH_9.x Ubuntu-..."
...
Progress: 1024/1024 (100%) ports scanned...

---- Summary ----
Target   : localhost (127.0.0.1)
Ports    : 1-1024
Open     : 1 [22(ssh)]
Duration : 2.14s
Report   : scan_127_0_0_1_20250913-143209.txt
```

## Notes on banners
Some protocols (like **SSH**, **FTP**, **SMTP**) send a greeting immediately, which the scanner will capture if it arrives within a short timeout. **HTTP** is **request–response**, so it doesn’t greet by itself—v1 intentionally does **not** do HTTP probing.

## What I learned (short)
- TCP sockets: using `connect_ex((host, port))` as an “open port?” test.
- Hostname resolution and per-port service name lookup.
- Measuring durations with `time.perf_counter()`.
- Writing results + a summary to timestamped files.
- Why HTTP “banners” differ (request–response) and are skipped in v1.

## License
MIT (see `LICENSE`).

For longer notes, see [docs/LEARNING.md](docs/LEARNING.md)
