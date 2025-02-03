import json
import base64
import re
from config.logger_config import setup_logging
from pathlib import Path

class Payloads:
    def __init__(self, filepath):
        self.logger = setup_logging()
        self.filepath = Path(filepath)
        self.payloads = self.load_payloads()

    def load_payloads(self):
        try:
            with self.filepath.open('r') as file:
                return json.load(file)
        except Exception as e:
            self.logger.error(f"Failed to load payloads from {self.filepath}: {e}")
            return {}

    def get_payloads(self, type=None):
        if type:
            return self.payloads.get(type, [])
        return self.payloads

    def add_payload(self, type, payload):
        if type in self.payloads:
            self.payloads[type].append(payload)
            self.logger.info(f"Added payload to {type}")
            self.save_payloads()
        else:
            self.logger.error(f"Payload type {type} does not exist")

    def save_payloads(self):
        try:
            with self.filepath.open('w') as file:
                json.dump(self.payloads, file, indent=4)
            self.logger.info("Payloads saved successfully")
        except Exception as e:
            self.logger.error(f"Failed to save payloads to {self.filepath}: {e}")

    def obfuscate_payload(self, payload, encoding_type):
        try:
            if encoding_type == 'base64':
                return base64.b64encode(payload.encode()).decode()
            elif encoding_type == 'unicode':
                return ''.join(f"\\u{ord(c):04x}" for c in payload)
            elif encoding_type == 'decimal':
                return ''.join(f"&#{ord(c)};" for c in payload)
            elif encoding_type == 'octal':
                return ''.join(f"\\{oct(ord(c))[2:]}" for c in payload)
            elif encoding_type == 'hex':
                return ''.join(f"&#x{ord(c):02x};" for c in payload)
            elif encoding_type == 'dword':
                if re.match(r'\d+\.\d+\.\d+\.\d+', payload): 
                    return payload.replace('127.0.0.1', '2130706433')
                else:
                    self.logger.error("Dword encoding is only applicable to IP addresses.")
                    return payload
            else:
                self.logger.error(f"Unknown encoding type: {encoding_type}")
                return payload
        except Exception as e:
            self.logger.error(f"Error obfuscating payload with {encoding_type}: {e}")
            return payload

    def apply_obfuscation(self, payload, encoding_types):
        obfuscated_payloads = []
        for encoding in encoding_types:
            obfuscated_payload = self.obfuscate_payload(payload, encoding)
            self.logger.info(f"Applied {encoding} encoding: {obfuscated_payload}")
            obfuscated_payloads.append(obfuscated_payload)
        return obfuscated_payloads
