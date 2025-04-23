import csv
from typing import List

class DomainReader:
    def __init__(self, csv_file: str):
        self.csv_file = csv_file

    def get_domains(self) -> List[str]:
        domains = []
        try:
            with open(self.csv_file, 'r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    domains.append(row['domain'].strip())
        except Exception as e:
            raise Exception(f"Error reading CSV file: {str(e)}")
        return domains
