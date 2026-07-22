"""Basic system diagnostics: disk space, memory, and network connectivity.

Uses only the standard library so it runs anywhere without extra installs.
"""
import argparse
import os
import shutil
import socket


def check_disk_usage(path="/", min_free_percent=10):
    total, used, free = shutil.disk_usage(path)
    free_percent = (free / total) * 100
    ok = free_percent >= min_free_percent
    return {
        "path": path,
        "total_gb": round(total / (1024 ** 3), 2),
        "used_gb": round(used / (1024 ** 3), 2),
        "free_gb": round(free / (1024 ** 3), 2),
        "free_percent": round(free_percent, 1),
        "ok": ok,
    }


def check_memory(min_free_percent=10):
    meminfo = {}
    try:
        with open("/proc/meminfo", encoding="utf-8") as f:
            for line in f:
                key, value = line.split(":", 1)
                meminfo[key.strip()] = int(value.strip().split()[0])
    except FileNotFoundError:
        return {"available": False, "reason": "/proc/meminfo not found on this platform"}

    total_kb = meminfo.get("MemTotal", 0)
    available_kb = meminfo.get("MemAvailable", 0)
    free_percent = (available_kb / total_kb * 100) if total_kb else 0
    return {
        "available": True,
        "total_mb": round(total_kb / 1024, 1),
        "available_mb": round(available_kb / 1024, 1),
        "free_percent": round(free_percent, 1),
        "ok": free_percent >= min_free_percent,
    }


def check_network(host="8.8.8.8", port=53, timeout=3):
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return {"host": host, "port": port, "ok": True}
    except OSError as e:
        return {"host": host, "port": port, "ok": False, "error": str(e)}


def check_cpu_count():
    return {"cpu_count": os.cpu_count()}


def run_all_checks(disk_path="/", host="8.8.8.8", port=53):
    return {
        "disk": check_disk_usage(disk_path),
        "memory": check_memory(),
        "network": check_network(host, port),
        "cpu": check_cpu_count(),
    }


def main():
    parser = argparse.ArgumentParser(description="Run basic system diagnostics")
    parser.add_argument("--path", default="/", help="Path to check disk usage for")
    parser.add_argument("--host", default="8.8.8.8", help="Host to test network connectivity against")
    parser.add_argument("--port", type=int, default=53, help="Port to test network connectivity against")
    args = parser.parse_args()

    results = run_all_checks(args.path, args.host, args.port)

    print("--- Disk ---")
    disk = results["disk"]
    print(f"{disk['path']}: {disk['free_gb']}GB free of {disk['total_gb']}GB ({disk['free_percent']}%) "
          f"[{'OK' if disk['ok'] else 'LOW'}]")

    print("\n--- Memory ---")
    mem = results["memory"]
    if mem.get("available"):
        print(f"{mem['available_mb']}MB available of {mem['total_mb']}MB ({mem['free_percent']}%) "
              f"[{'OK' if mem['ok'] else 'LOW'}]")
    else:
        print(mem["reason"])

    print("\n--- Network ---")
    net = results["network"]
    if net["ok"]:
        print(f"Connected to {net['host']}:{net['port']} [OK]")
    else:
        print(f"Failed to connect to {net['host']}:{net['port']} [FAIL] ({net.get('error')})")

    print("\n--- CPU ---")
    print(f"CPU count: {results['cpu']['cpu_count']}")

    failures = [name for name, r in results.items() if isinstance(r, dict) and r.get("ok") is False]
    if failures:
        print(f"\n{len(failures)} check(s) failed: {', '.join(failures)}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
