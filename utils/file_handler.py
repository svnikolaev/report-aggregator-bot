import json
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


def write_data_to_file(data, file: Path):
    if not isinstance(file, Path):
        file = Path(file)
    logger.info(f'writing data:\n{data}')
    with open(file, 'w', encoding='utf-8') as f:
        f.write(json.dumps(data,
                           indent=4,
                           sort_keys=True,
                           separators=(',', ': '),
                           ensure_ascii=False))


def read_data_from_file(file: Path):
    if not isinstance(file, Path):
        file = Path(file)
    with open(file, 'r', encoding='utf-8') as f:
        try:
            data = json.load(f)
        except json.decoder.JSONDecodeError:
            data = None
    return data
