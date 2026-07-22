"""Unified CLI entry point for diagnostic utilities."""
import argparse
import sys
from diagnostics.system_check import run_all_checks


def main():
    parser = argparse.ArgumentParser(description="System diagnostics")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # system-check command
    check_parser = subparsers.add_parser("system-check", help="Run system diagnostics")
    check_parser.add_argument("--path", default="/", help="Path to check disk usage for")
    check_parser.add_argument("--host", default="8.8.8.8", help="Host to test network connectivity against")
    check_parser.add_argument("--port", type=int, default=53, help="Port to test network connectivity against")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(0)
    
    if args.command == "system-check":
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
