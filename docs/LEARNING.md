# Learning Notes — TCP Port Scanner (v1)

These notes explain the core ideas behind the v1 scanner. We keep them separate from the README to keep the main page crisp.

---

## 1) TCP sockets & ports
- **IP address** = network identity; **port** = which service.
- We use IPv4 TCP sockets: `socket.AF_INET`, `socket.SOCK_STREAM`.
- `connect_ex((host, port))` attempts a TCP handshake:
  - returns **0** ⇒ success (port **open**);
  - non‑zero ⇒ failure (usually closed/filtered).
- Each attempt uses a **short timeout** (`s.settimeout(0.5)`) so scans don’t hang.

---

## 2) Hostname resolution & service names
- `socket.gethostbyname(host)` converts a hostname to an IPv4 string; failures raise `socket.gaierror` (we return `None`).
- `socket.getservbyport(port, 'tcp')` maps common ports to names using the system database (e.g., `/etc/services`); if missing, it raises `OSError` and we return `"unknown"`.

---

## 3) Passive banner reads (non‑HTTP)
- Some protocols send a greeting line immediately after connect (SSH/FTP/SMTP/POP3/IMAP).
- We optionally do **one quick `recv(1024)`** with a short timeout; if bytes arrive, we decode the **first line** and print it as a “banner”.
- **HTTP** is request–response and does not greet; v1 intentionally **skips** HTTP probing to keep the project simple.

---

## 4) Timing, progress, and reporting
- **Elapsed time**: measured with `time.perf_counter()` (monotonic, high‑resolution).
- **Progress pulse**: `enumerate(..., start=1)` gives a 1‑based counter; we print every 50 ports and at the end, including **percentage** with `int(i/total*100)` capped at 100.
- **Reports**: we write every line plus a neat summary to a **timestamped** file (`scan_<ip>_<YYYYMMDD-HHMMSS>.txt`).

---

## 5) Ethics
- Only scan systems you own/control or have explicit permission to test.
- Keep reports private unless you own the system.

---

## 6) Future ideas (beyond v1)
- Optional HTTP header probe (parse the `Server:` header).
- Parallel scanning (threads/async) with care for rate limits.
- JSON/CSV output formats.
