from collections import defaultdict
import csv
import datetime as dt

from pep_parse.settings import (
    BASE_DIR,
    DATETIME_FORMAT,
    RESULTS
)


class PepParsePipeline:

    def __init__(self):
        self.results_dir = BASE_DIR / RESULTS
        self.results_dir.mkdir(exist_ok=True)

    def open_spider(self, spider):
        self.status_count = defaultdict(int)

    def process_item(self, item, spider):
        self.status_count[item['status']] += 1
        return item

    def close_spider(self, spider):
        now_formatted = dt.datetime.now().strftime(DATETIME_FORMAT)
        file_name = f'status_summary_{now_formatted}.csv'
        file_path = self.results_dir / file_name
        with open(file_path, 'w', encoding='utf-8') as f:
            csv.writer(
                f,
                dialect=csv.unix_dialect,
                quoting=csv.QUOTE_NONE
            ).writerows((
                ('Статус', 'Количество'),
                *self.status_count.items(),
                ('Всего', sum(self.status_count.values())),
            ))
