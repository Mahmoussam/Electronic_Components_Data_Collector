import csv

class CSVWriter:
    def __init__(self, file_path, mode='w', newline='', encoding='utf-8', **writer_kwargs):
        """
        :param file_path: path to the CSV file
        :param mode: file mode, 'w' for write or 'a' for append
        :param newline: should be '' for csv on most platforms
        :param encoding: file encoding
        :param writer_kwargs: extra args passed to csv.writer (e.g. delimiter=',')
        """
        self._file = open(file_path, mode, newline=newline, encoding=encoding)
        self._writer = csv.writer(self._file, **writer_kwargs)

    def write_row(self, row):
        """Write a single row (an iterable of values)."""
        self._writer.writerow(row)

    def write_rows(self, rows):
        """Write multiple rows (an iterable of iterables)."""
        self._writer.writerows(rows)

    def close(self):
        """Flush and close the underlying file."""
        if not self._file.closed:
            self._file.close()

    def __enter__(self):
        """Support for `with CSVWriter(...) as w:`."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Ensure file is closed on exiting the with-block."""
        self.close()
