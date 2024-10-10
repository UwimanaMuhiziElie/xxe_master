import logging
import sys
from pathlib import Path

def setup_logging():
    logger = logging.getLogger('XXEDetector')
    logger.setLevel(logging.DEBUG)

    log_file_path = Path('logs') / 'xxe_detector.log'
    log_file_path.parent.mkdir(exist_ok=True) 
    fh = logging.FileHandler(log_file_path)
    fh.setLevel(logging.DEBUG)

    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.INFO)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    logger.addHandler(fh)
    logger.addHandler(ch)

    return logger

