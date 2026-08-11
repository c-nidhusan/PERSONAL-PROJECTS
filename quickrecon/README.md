# QuickRecon

> A lightweight, dependency-free recon toolkit for learning penetration testing.
> **Subdomain enumeration + TCP port scanning** in a single Python script.

Built as my first hands-on project while training on TryHackMe and working
toward bug bounty hunting. It uses **only the Python standard library** —
no `pip install` needed.

## Features

- 🌐 **Subdomain enumeration** via DNS brute-force (multi-threaded)
- 🔌 **TCP port scanning** of discovered hosts (multi-threaded, with timeout)
- 📄 **Clean console output** and optional text-file export (`-o`)
- ⚡ No external dependencies — runs on any Python 3.6+

## Requirements

- Python 3.6+
- A target you own or have written permission to test

## Usage

```bash
# Enumerate subdomains + scan default ports on all found hosts
python3 quickrecon.py -d example.com

# Use a custom wordlist
python3 quickrecon.py -d example.com -w my-wordlist.txt

# Scan specific ports only
python3 quickrecon.py -d example.com -p 80,443,8080

# Save results to a file
python3 quickrecon.py -d example.com -o results.txt

# Tune performance
python3 quickrecon.py -d example.com -t 100 --timeout 1.5
```

## Example output

```
$ python3 quickrecon.py -d example.com -p 80,443 -o results.txt

[*] Brute-forcing 55 subdomains of example.com ...
    [+] www.example.com               -> 93.184.216.34
[*] Scanning 2 ports on 93.184.216.34 ...
    [+] 93.184.216.34:80 open
    [+] 93.184.216.34:443 open

[+] Done in 3.2s — 1 subdomains, 2 open ports found.
[+] Results saved to results.txt
```

## Wordlists

A small starter list ships with the tool (`subdomains.txt`). For real
engagements, swap in a bigger list such as
[SecLists — Discovery/DNS](https://github.com/danielmiessler/SecLists/tree/master/Discovery/DNS).

## Roadmap

- [x] Subdomain brute-force
- [x] TCP port scan
- [ ] HTTP service banner grabbing
- [ ] Save results as JSON/CSV
- [ ] CIDR/range scanning

## ⚠️ Legal disclaimer

This tool is for **educational purposes only**. Only use it on systems you
own or have explicit written authorization to test. Unauthorized scanning is
illegal in most jurisdictions and I take no responsibility for misuse.

## License

MIT
