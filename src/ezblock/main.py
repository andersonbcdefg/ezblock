import argparse
import os
import sys
import fire

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
    fire.Fire({
        "block": block_website,
        "unblock": unblock_website,
        "list": list_blocked_websites
    })