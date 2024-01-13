from ._types import LogLevel

import asyncio
import aiofiles
from concurrent.futures import ThreadPoolExecutor
import logging
import os
import zipfile


class Moon:
    def __init__(
        self,
        name: str = __name__,
        log_file: str = 'moon.log',
        stream_handler: bool = True,
        file_handler: bool = True,
        disabled: bool = False,
        stream_level: int = LogLevel.DEBUG,
        file_level: int = LogLevel.DEBUG,
        stream_format: logging.Formatter | None = None,
        file_format: logging.Formatter | None = None
    ):
        """
        Initialize the Moon object.

        Parameters:
        - name: str, logger name (default is the name of the current module)
        - log_file: str, path to the log file (default is 'moon.log')
        - stream_handler: bool, whether to use a stream handler (default is True)
        - file_handler: bool, whether to use a file handler (default is True)
        - disabled: bool, whether the logger is disabled (default is False)
        - stream_level: int, log level for the stream handler (default is LogLevel.DEBUG)
        - file_level: int, log level for the file handler (default is LogLevel.DEBUG)
        - stream_format: logging.Formatter | None, log format for the stream handler
        - file_format: logging.Formatter | None, log format for the file handler
        """

        self._name = name
        self._log_file = log_file

        self._file_level = file_level
        self._stream_level = stream_level

        self._logger = logging.getLogger(self._name)
        self._logger.setLevel(level=self._stream_level)
        self._logger.disabled = disabled

        self._default_formatter = logging.Formatter(
            "[{name}] [{asctime}] - [{levelname}]: {message}",
            style='{'
        )

        self._stream_format = stream_format or self._default_formatter
        self._file_format = file_format or self._default_formatter

        self.add_stream_handler() if stream_handler else None
        self.add_file_handler() if file_handler else None

    def add_stream_handler(self):
        """
        Add a stream handler to the logger.
        """

        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(self._stream_level)
        stream_handler.setFormatter(self._stream_format)
        self._logger.addHandler(stream_handler)

    def add_file_handler(self, level=logging.DEBUG):
        """
        Add a file handler to the logger.
        """

        file_handler = logging.FileHandler(self._log_file)
        file_handler.setLevel(self._file_level)
        file_handler.setFormatter(self._file_format)
        self._logger.addHandler(file_handler)

    def archive(self):
        """
        Archive the log file into a ZIP file and remove the original log file.
        """

        archive_path = f"{self._log_file}.zip"

        with open(self._log_file, 'rb') as file:
            self._zip_log(archive_path, file)

        os.remove(self._log_file)

        return self
    
    def clear(self) -> None:
        """
        Clear the contents of the log file.
        
        This method opens the log file in write mode ('w') and overwrites its contents with an empty string.
        """
        with open(self._log_file, mode="w", encoding="utf-8") as file:
            file.write('')


    def remove(self) -> None:
        """
        Remove the log file.

        If the log file exists, this method deletes it. Use with caution, as it permanently removes the file.
        """
        if os.path.exists(self._log_file):
            os.remove(self._log_file)

    def _zip_log(self, archive_path, file):
        """
        Zip the log file and write it to the given archive path.
        """

        with open(archive_path, 'wb') as zipf:
            with zipfile.ZipFile(zipf, 'w') as zip_file:
                zip_file.writestr(
                    os.path.basename(self._log_file),
                    file.read()
                )

    def set_log_format(self, log_format):
        """
        Set the log format for all handlers.
        """

        self._default_formatter = logging.Formatter(log_format, style='{')

        for handler in self._logger.handlers:
            handler.setFormatter(self._default_formatter)

    def add_formatter(self, formatter):
        """
        Add a formatter to the logger.
        """

        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        self._logger.addHandler(handler)

    def del_formatters(self):
        """
        Remove all formatters from the logger.
        """
        
        for handler in self._logger.handlers:
            self._logger.removeHandler(handler)

    def del_formatter(self, formatter):
        """
        Remove a specific formatter from the logger.
        """

        if formatter in self._logger.handlers:
            self._logger.removeHandler(formatter)

    def set_formatter(self, formatter):
        """
        Set a formatter for the logger, removing existing formatters.
        """

        self._del_formatters()
        self._add_formatter(formatter=formatter)

    def edit_format(self, new_log_format: str) -> None:
        """
        Edit the log format for all handlers.
        """

        required_placeholders = ["{message}"]
        if all(ph in new_log_format for ph in required_placeholders):
            self.set_log_format(new_log_format)
        else:
            self._logger.error("Invalid log format")

    def reset_format(self) -> None:
        """
        Reset the log format to the default.
        """

        self.set_log_format(self._default_formatter)

    def base_logger(self) -> logging.Logger:
        """
        Get the base logger instance.
        """

        return self._logger
