import json
from core.logger_config import setup_logging
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

if __name__ == '__main__':
    payloads = Payloads('payloads/payloads.json')
