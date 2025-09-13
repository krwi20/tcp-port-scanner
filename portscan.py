#!/usr/bin/env python3
import socket
import time
from datetime import datetime

# --- Helpers ---
def resolve_host(target: str) -> str | None:
    """Return IPv4 string for a hostname/IP, or None if resolution fails."""
    try:
        return socket.gethostbyname(target)
    except socket.gaierror:
        return None

def svc_name(port: int) -> str:
    """Best-effort service name for a TCP port, or 'unknown'."""
    try:
        return socket.getservbyport(port, 'tcp')
    except OSError:
        return "unknown"

def main() -> int:
    # --- Inputs ---
    target = input("Enter target IP or hostname (e.g. 127.0.0.1): ").strip()
    try:
        start_port = int(input("Enter start port: ").strip())
        end_port   = int(input("Enter end port: ").strip())
    except ValueError:
        print("[!] Ports must be integers.")
        return 1
    if not (1 <= start_port <= 65535 and 1 <= end_port <= 65535 and start_port <= end_port):
        print("[!] Ports must be between 1 and 65535, and start <= end.")
        return 1

    ip = resolve_host(target)
    if ip is None:
        print(f"[!] Could not resolve '{target}'. Try an IP address or a valid hostname.")
        return 1

    started = datetime.now()
    ts = started.strftime("%Y%m%d-%H%M%S")
    outname = f"scan_{ip.replace('.', '_')}_{ts}.txt"

    print(f"Target: {target} ({ip})")
    print(f"Saving results to {outname}")

    # --- Scan ---
    t0 = time.perf_counter()
    open_ports: list[tuple[int, str]] = []
    total = end_port - start_port + 1

    with open(outname, "w", encoding="utf-8") as results:
        results.write(f"TCP scan report\n")
        results.write(f"Target: {target} ({ip})\n")
        results.write(f"Ports : {start_port}-{end_port}\n")
        results.write(f"Started: {started.isoformat()}\n\n")

        for i, port in enumerate(range(start_port, end_port + 1), start=1):
            name = svc_name(port)
            # Create a fresh TCP socket for each attempt
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(0.5)  # keep scans snappy
                result = s.connect_ex((ip, port))

                if result == 0:
                    # Passive banner grab only: read once briefly.
                    banner = ""
                    try:
                        s.settimeout(0.5)
                        data = s.recv(1024)  # may be empty for protocols that don't greet
                        if data:
                            banner = data.decode("utf-8", errors="replace").splitlines()[0].strip()
                    except Exception:
                        banner = ""

                    msg = f"Port {port} ({name}) is OPEN"
                    if banner:
                        msg += f' | banner: "{banner[:80]}"'
                    print(msg)
                    results.write(msg + "\n")
                    open_ports.append((port, name))
                else:
                    msg = f"Port {port} ({name}) is CLOSED"
                    print(msg)
                    results.write(msg + "\n")

            # progress pulse
            if i % 50 == 0 or i == total:
                pct = min(100, int(i / total * 100))
                print(f"Progress: {i}/{total} ({pct}%) ports scanned...")

        duration = time.perf_counter() - t0
        open_str = ", ".join(f"{p}({n})" for p, n in open_ports) if open_ports else "none"
        summary = (
            "\n---- Summary ----\n"
            f"Target   : {target} ({ip})\n"
            f"Ports    : {start_port}-{end_port}\n"
            f"Open     : {len(open_ports)} [{open_str}]\n"
            f"Duration : {duration:.2f}s\n"
            f"Report   : {outname}\n"
        )
        print(summary, end="")
        results.write(summary)

    return 0

if __name__ == "__main__":
    raise SystemExit(main())
