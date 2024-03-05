import csv
from collections import defaultdict
import datetime as dt

from pep_parse.constants import (
    BASE_DIR,
    DATETIME_FORMAT,
    RESULTS
)


class PepParsePipeline:

    def open_spider(self, spider):
        self.status_count = defaultdict(int)

    def process_item(self, item, spider):
        self.status_count[item['status']] += 1
        return item

    def close_spider(self, spider):
        results_dir = BASE_DIR / RESULTS
        results_dir.mkdir(exist_ok=True)
        now_formatted = dt.datetime.now().strftime(DATETIME_FORMAT)
        file_name = f'status_summary_{now_formatted}.csv'
        file_path = results_dir / file_name
        with open(file_path, 'w', encoding='utf-8') as f:
            csv.writer(f, dialect=csv.unix_dialect).writerows([
                ('Статус', 'Количество'),
                *self.status_count.items(),
                ('Всего', sum(self.status_count.values())),
            ])
