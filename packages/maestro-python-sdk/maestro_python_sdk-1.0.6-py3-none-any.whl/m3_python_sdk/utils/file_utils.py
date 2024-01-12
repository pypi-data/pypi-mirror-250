import os
from io import StringIO
from pathlib import Path
from typing import Any

from m3_python_sdk.utils.exeption import raise_application_exception


class FileLikeObjectPrepare:
    """
    Class for creating file-like objects from a raw data instead of writing
    to a file. Supports conversion in the json and csv formats.
    """

    def __init__(self, file_name: str, content: Any):
        """
        Initialize self.
        @param file_name: file name with extension
        @param content: a raw data
        """
        if "." not in file_name:
            raise_application_exception(
                code=None,
                content=f'Wrong file name - \'{file_name}\'. '
                        f'Please specify only the file name with extension.'
            )
        self.extension = Path(file_name).suffix.lower()
        self.content = content
        self.extension_mapping = {
            '.csv': self._csv_handler,
            '.json': self._json_handler,
            '.xml': self._string_handler
        }

    def transform(self) -> bytes:
        """
        @return: file-like object with the specified extension
        """
        handler = self.extension_mapping.get(self.extension)
        if not handler:
            raise_application_exception(
                code=None,
                content=f'Extension \'{self.extension}\' does not supported.'
            )

        return handler()

    def _csv_handler(self):
        import csv

        buffer = StringIO()
        writer = csv.writer(buffer)
        writer.writerows(self.content)
        return buffer.getvalue().encode()

    def _json_handler(self):
        import json

        buffer = StringIO()
        json.dump(self.content, buffer, indent=4)
        return buffer.getvalue().encode()

    def _string_handler(self):
        buffer = StringIO()
        buffer.write(self.content)
        return buffer.getvalue().encode()


def check_file_size(file_path, max_size_bytes):
    if max_size_bytes and os.path.getsize(file_path) > max_size_bytes:
        raise_application_exception(
            code=None,
            content=f'The size of the {file_path} file exceeds '
                    f'a maximum of {max_size_bytes} bytes'
        )
