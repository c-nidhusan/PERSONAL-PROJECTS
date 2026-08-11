#!/usr/bin/env python3
"""
QuickRecon — a lightweight, dependency-free recon toolkit.

Features
--------
- Subdomain enumeration via DNS brute-force
- TCP port scanning with threading
- Clean console output + optional file export

Author: Nidhusan
License: MIT — educational use only. Scan only systems you own
or have explicit written permission to test.
"""

import argparse
import concurrent.futures
import socket
import sys
import time

DEFAULT_PORTS = [21, 22, 23, 25, 53, 80, 110, 111, 135, 139, 143,
                 443, 445, 993, 995, 1723, 3306, 3389, 5900, 8080, 8443]
DEFAULT_WORDLIST = "subdomains.txt"
DEFAULT_TIMEOUT = 2.0
DEFAULT_THREADS = 50

BANNER = r"""
   ____        _      ____
  / __ \__  __(_)____/ __ \___  ________
 / / / / / / / / ___/ /_/ / _ \/ ___/ _ \
/ /_/ / /_/ / (__  ) _, _/  __/ /  /  __/
\___\_\__,_/_/____/_/ |_|\___/_/   \___/
   Lightweight recon toolkit (educational use only)
"""


def resolve(domain):
    """Return IPv4 for a hostname, or None if it doesn't resolve."""
    try:
        return socket.gethostbyname(domain)
    except socket.gaierror:
        return None


def brute_subdomains(domain, wordlist_path, threads):
    """Brute-force subdomains of `domain` using a wordlist."""
    try:
        with open(wordlist_path, encoding="utf-8") as f:
            words = [line.strip().lower() for line in f
                     if line.strip() and not line.startswith("#")]
    except OSError as e:
        print(f"[!] Cannot read wordlist {wordlist_path}: {e}")
        sys.exit(1)

    def check(word):
        name = f"{word}.{domain}"
        ip = resolve(name)
        return (name, ip) if ip else None

    print(f"[*] Brute-forcing {len(words)} subdomains of {domain} ...")
    found = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as ex:
        for result in ex.map(check, words):
            if result:
                name, ip = result
                found.append((name, ip))
                print(f"    [+] {name:<28} -> {ip}")
    return found


def scan_ports(host, ports, threads, timeout):
    """Scan TCP ports on a host, return the list of open ones."""
    def scan(port):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            if s.connect_ex((host, port)) == 0:
                return port
        return None

    print(f"[*] Scanning {len(ports)} ports on {host} ...")
    open_ports = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as ex:
        for port in ex.map(scan, ports):
            if port:
                open_ports.append(port)
                print(f"    [+] {host}:{port} open")
    return sorted(open_ports)


def main():
    p = argparse.ArgumentParser(
        description="QuickRecon — subdomain enumeration + port scanning "
                    "(educational use only)")
    p.add_argument("-d", "--domain", help="Target domain, e.g. example.com")
    p.add_argument("-w", "--wordlist", default=DEFAULT_WORDLIST,
                   help="Subdomain wordlist (default: subdomains.txt)")
    p.add_argument("-p", "--ports",
                   help="Comma-separated ports to scan "
                        "(default: common top-20)")
    p.add_argument("-t", "--threads", type=int, default=DEFAULT_THREADS,
                   help="Thread count (default: 50)")
    p.add_argument("--timeout", type=float, default=DEFAULT_TIMEOUT,
                   help="Connect timeout in seconds (default: 2)")
    p.add_argument("-o", "--out", help="Write results to this file")
    args = p.parse_args()

    print(BANNER)
    if not args.domain:
        p.error("you must provide a domain (use -d/--domain)")

    print("[!] Legal warning: only scan systems you own or have written "
          "permission to test. Misuse may be illegal.\n")

    start = time.time()
    results = {}

    subdomains = brute_subdomains(args.domain, args.wordlist, args.threads)
    results["subdomains"] = subdomains
    hosts = sorted({ip for _, ip in subdomains})

    ports = [int(x) for x in args.ports.split(",")] if args.ports else DEFAULT_PORTS
    for host in hosts:
        results[f"ports:{host}"] = scan_ports(host, ports, args.threads,
                                              args.timeout)

    elapsed = time.time() - start
    print(f"\n[+] Done in {elapsed:.1f}s — "
          f"{len(subdomains)} subdomains, "
          f"{sum(len(v) for k, v in results.items() if k.startswith('ports:'))} "
          f"open ports found.")

    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            for name, ip in subdomains:
                f.write(f"{name} {ip}\n")
            for host in hosts:
                for port in results.get(f"ports:{host}", []):
                    f.write(f"{host}:{port}\n")
        print(f"[+] Results saved to {args.out}")


if __name__ == "__main__":
    main()
