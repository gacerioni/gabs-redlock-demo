import csv
import os


class CSVManager:
    def __init__(self, filename):
        self.filename = filename

    def append_row(self, row_data):
        file_exists = os.path.isfile(self.filename)
        with open(self.filename, mode='a', newline='') as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow(['Header1', 'Header2'])  # Customize headers
            writer.writerow(row_data)
