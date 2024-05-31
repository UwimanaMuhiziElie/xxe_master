import re
import urllib.parse
import base64
import requests
import logging
import concurrent.futures
from pathlib import Path
from requests.exceptions import RequestException
from payloads.payloads import Payloads

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class XXEDetector:
    def __init__(self, target_url):
        self.target_url = target_url
        self.payloads = Payloads('payloads/payloads.json').get_payloads()
        self.vulnerabilities = []

    def send_request(self, payload):
        headers = {'Content-Type': 'application/xml'}
        try:
            response = requests.post(self.target_url, data=f'<data>{payload}</data>', headers=headers)
            return response.text
        except RequestException as e:
            logging.error(f"Failed to send request: {e}")
            return None

    def is_xxe_detected(self, response):
        try:
            response = self.decode_response(response)
        except Exception as e:
            logging.error(f"Error decoding response: {e}")
            return False

        xxe_patterns = [
            r'<!DOCTYPE\s+[^>]*[\[><]+',
            r'\bENTITY\b',
            r'\bSYSTEM\b',
            r'XML\s+parsing\s+error',
            r'Entity\s+.+?\s+not\s+defined',
        ]

        for pattern in xxe_patterns:
            if re.search(pattern, response, re.IGNORECASE):
                logging.debug("XXE detected using pattern: {}".format(pattern))
                return True
        return False

    def decode_response(self, response):
        try:
            response = urllib.parse.unquote(response)
            response = base64.b64decode(response).decode('utf-8', errors='ignore')
        except Exception as e:
            raise Exception(f"Error decoding response: {e}")

        return response

    def send_and_detect(self, payload):
        response = self.send_request(payload)
        if response and self.is_xxe_detected(response):
            return {'payload': payload, 'response': response}
        return None

    def detect_xxe_vulnerabilities(self, attacker_url):
        logging.info("Starting XXE vulnerability detection using concurrent execution...")
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            results = list(executor.map(self.send_and_detect, [payload.replace("{{TARGET_URL}}", self.target_url).replace("{{ATTACKER_URL}}", attacker_url) for _, payloads in self.payloads.items() for payload in payloads]))

        for result in results:
            if result:
                logging.info(f"Vulnerability detected with payload: {result['payload']}")
                self.vulnerabilities.append({'type': 'Detected', 'payload': result['payload'], 'response': result['response']})

        return self.vulnerabilities

    def exploit_xxe(self, payload):
        logging.info(f"Attempting to exploit with payload: {payload}")
        response = self.send_request(payload)
        print("Exploitation Result:")
        print(response)
        print("=" * 50)

    def exploit_detected_vulnerabilities(self):
        if self.vulnerabilities:
            logging.info("Exploiting detected XXE vulnerabilities:")
            for vulnerability in self.vulnerabilities:
                self.exploit_xxe(vulnerability['payload'])

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
            print("No XXE vulnerabilities detected.")

    def save_report(self, report_data, filename="XXE_Report.txt"):
        home = Path.home()
        report_path = home / 'Downloads' / filename 
        if not report_path.parent.exists():
            report_path = home / filename 
        
        with report_path.open('w', encoding='utf-8') as report_file:
            report_file.write(report_data)
        print(f"Report saved to: {report_path}")
