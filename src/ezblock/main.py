import argparse
import os
import sys

HOSTS_PATH = '/etc/hosts'
LOCALHOST = '127.0.0.1'

def read_hosts_file():
    with open(HOSTS_PATH, 'r') as file:
        return file.readlines()

def write_hosts_file(lines):
    with open(HOSTS_PATH, 'w') as file:
        file.writelines(lines)

def block_website(domain):
    lines = read_hosts_file()
    if f"{LOCALHOST} {domain}\n" not in lines:
        lines.append(f"{LOCALHOST} {domain}\n")
        write_hosts_file(lines)
        print(f"Blocked {domain}")
    else:
        print(f"{domain} is already blocked")

def unblock_website(domain):
    lines = read_hosts_file()
    new_lines = [line for line in lines if not line.strip().endswith(domain)]
    if len(new_lines) < len(lines):
        write_hosts_file(new_lines)
        print(f"Unblocked {domain}")
    else:
        print(f"{domain} is not blocked")

def list_blocked_websites():
    lines = read_hosts_file()
    blocked = [line.split()[-1] for line in lines if line.startswith(LOCALHOST) and len(line.split()) == 2]
    if blocked:
        print("Blocked websites:")
        for domain in blocked:
            print(domain)
    else:
        print("No websites are currently blocked")

def main():
    parser = argparse.ArgumentParser(description="Block or unblock websites by modifying /etc/hosts")
    parser.add_argument("action", choices=["block", "unblock", "list"], help="Action to perform")
    parser.add_argument("domain", nargs="?", help="Domain to block or unblock")

    args = parser.parse_args()

    if os.geteuid() != 0:
        print("This script must be run with sudo privileges")
        sys.exit(1)

    if args.action == "block" and args.domain:
        block_website(args.domain)
    elif args.action == "unblock" and args.domain:
        unblock_website(args.domain)
    elif args.action == "list":
        list_blocked_websites()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()