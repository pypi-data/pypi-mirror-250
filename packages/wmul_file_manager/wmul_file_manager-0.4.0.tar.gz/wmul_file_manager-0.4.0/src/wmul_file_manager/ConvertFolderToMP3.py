"""
@Author = 'Mike Stanley'

Script to archive a directory or set of directories into mp3 format. This script is multi-threaded and uses at least
two threads. One thread issues file copy commands to the os, the other calls the mp3 converter. Any extra threads call
additional mp3 converters.

Mainly designed to be run from command-line, but can also be called from other scripts.

============ Change Log ============
2022-Aug-02 = Convert .verbose logging to .debug.

2019-Jun-17 = Change to write the converted files directly into the destination folder instead of going through
              a temp folder.

2019-Jun-14 = Remove obsolete imports.

              Added logic to catch the exception, retry, and log if there is a permission error when deleting.

2018-May-10 = Rename ConvertFolderToMP3.FileInformationType to .ConverstionFileInformationType

              Rename ConvertFolderToMP3.FileInformation to .ConverstionFileInformation

2018-May-08 = Remove old command-line interface that was housed in this file and based on argparse.

2018-May-01 = Import from Titanium_Monticello to this package.

2017-Aug-18 = Move the logger from Utilities to Logger.

2017-Aug-10 = Add extensive logging.

              Add logic to gracefully handle when a provided source path does not exist.

              Modify _empty_temp_folder to use Utilities.empty_folder.

2017-Jul-28 = Refactor imports.

              Refactor calls to argparse.

              Refactor to eliminate the class.

              Refactor some names.

              Create a method to act as an external entry point for this script.

              Update documentation.

2015-Jun-04 = Created.

============ License ============
The MIT License (MIT)

Copyright (c) 2015, 2017-2019, 2022, 2024 Michael Stanley

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
from collections import namedtuple
from datetime import date, timedelta
from enum import Enum
from functools import partial
from queue import Queue, Empty
from threading import Thread
import time

from wmul_file_manager.utilities import ffmpeg
from wmul_file_manager.utilities.FileNamePrinter import object_cleaner

import wmul_logger

logger = wmul_logger.get_logger()


class _ConversionFileInformationType(Enum):
    Raw_File = 0
    Converted_File = 1
    NoMoreRawFiles = 2
    NoMoreConvertedFiles = 3


class _ConversionFileInformation:
    def __init__(self, file_info_type, source_file_path, source_root_path, converted_files_final_folder):
        self.file_info_type = file_info_type
        self.original_file_name = source_file_path
        self.source_path = source_file_path

        relative_to_root = source_file_path.relative_to(source_root_path).parent
        final_filename = source_file_path.stem + ".mp3"
        self.destination_path = converted_files_final_folder / relative_to_root / final_filename

        self._create_all_needed_parents()

        self._file_has_been_converted = False

    def __str__(self):
        return f"_ConversionFileInformation:\n{str(self.file_info_type)}\n{str(self.original_file_name)}"

    def _create_all_needed_parents(self):
        _ConversionFileInformation._create_parents(self.destination_path)

    def converted(self):
        self.file_info_type = _ConversionFileInformationType.Converted_File

    @staticmethod
    def _create_parents(file_path):
        file_parent = file_path.parent
        file_parent.mkdir(parents=True, exist_ok=True)

    @classmethod
    def get_factory(cls, root_path, converted_files_final_folder):
        def inner(file_info_type, source_file_path):
            return cls(file_info_type, source_file_path, root_path, converted_files_final_folder)
        return inner


class NoMoreRawFiles:
    file_info_type = _ConversionFileInformationType.NoMoreRawFiles


ConvertFolderToMP3Arguments = namedtuple(
    "ConvertFolderToMP3Arguments",
    [
        "source_paths",
        "desired_suffix",
        "bitrate",
        "ffmpeg_executable",
        "separate_folder_flag",
        "max_conversion_threads",
        "delete_files_flag",
        "yesterday_flag"
    ]
)


def archive_yesterdays_files(arguments, call_ffmpeg):
    logger.debug("In archive_yesterdays_files.")
    logger.debug(f"With {locals()}")
    yesterday = date.today() - timedelta(days=1)
    yesterday_folder_name = "{yr:04d}-{mo:02d}-{da:02d}".format(yr=yesterday.year, mo=yesterday.month,
                                                                da=yesterday.day)
    yesterday_raw_files_folder = arguments.source_paths[0] / yesterday_folder_name

    if not yesterday_raw_files_folder.exists():
        logger.critical(f"Yesterday's folder does not exist. {str(yesterday_raw_files_folder)}")
        return

    if arguments.separate_folder_flag:
        yesterday_converted_files_folder = \
            yesterday_raw_files_folder.parent / (yesterday_raw_files_folder.name + "_mp3")
    else:
        yesterday_converted_files_folder = yesterday_raw_files_folder

    _archive_folder(yesterday_raw_files_folder, yesterday_converted_files_folder, arguments, call_ffmpeg)


def archive_list_of_folders(arguments, call_ffmpeg):
    logger.debug("In archive_list_of_folders")
    logger.debug(f"With {locals()}")
    for source_path in arguments.source_paths:
        logger.info(f"In archive_list_of_folders, working on: {object_cleaner(source_path)}")
        if not source_path.exists():
            logger.warning("Folder does not exist.")
            continue

        if arguments.separate_folder_flag:
            converted_files_folder = source_path.parent / (source_path.name + "_mp3")
        else:
            converted_files_folder = source_path
        _archive_folder(source_path, converted_files_folder, arguments, call_ffmpeg)


def _archive_folder(raw_files_folder, converted_files_final_folder, arguments, call_ffmpeg):
    logger.debug("In _archive_folder")
    logger.debug(f"With {locals()}")
    file_info_factory = _ConversionFileInformation.get_factory(
        raw_files_folder,
        converted_files_final_folder
    )

    file_conversion_queue = Queue()

    _populate_file_conversion_queue_ending_with_a_stop(
        raw_files_folder,
        file_info_factory,
        file_conversion_queue,
        arguments.desired_suffix
    )

    file_deletion_queue = Queue()
    conversion_threads = _spin_up_conversion_threads(
        arguments.max_conversion_threads,
        call_ffmpeg,
        file_conversion_queue,
        file_deletion_queue
    )

    [this_thread.join() for this_thread in conversion_threads]
    logger.info("All conversion threads finished")
    if arguments.delete_files_flag:
        logger.info("Delete files true.")
        _delete_files(file_deletion_queue)


def _spin_up_conversion_threads(max_conversion_threads, call_ffmpeg, file_conversion_queue, file_deletion_queue):
    conversion_threads = []
    for i in range(max_conversion_threads):
        this_thread = Thread(
            target=_convert_file,
            name="File Conv {0}".format(i),
            kwargs={
                "file_conversion_queue": file_conversion_queue,
                "file_deletion_queue": file_deletion_queue,
                "call_ffmpeg": call_ffmpeg
            }
        )
        logger.debug(f"Starting File Conversion Thread: {i}")

        this_thread.start()
        conversion_threads.append(this_thread)
    return conversion_threads


def _delete_files(file_deletion_queue):
    while True:
        try:
            this_file = file_deletion_queue.get(block=False)
        except Empty:
            logger.debug("file_deletion_queue empty.")
            return
        if this_file.file_info_type == _ConversionFileInformationType.Converted_File:
            logger.debug(f"Deleting {object_cleaner(this_file)}")
            original_file_name = this_file.original_file_name
            try:
                original_file_name.unlink()
            except PermissionError as pe:
                # Wait 5 seconds, retry
                time.sleep(5)
                try:
                    original_file_name.unlink()
                except PermissionError as pe:
                    logger.error(f"Permission error on {original_file_name}")
        else:
            logger.warning(f"File in deletion queue, but not converted. {object_cleaner(this_file)}")


def _populate_file_conversion_queue_ending_with_a_stop(raw_files_folder, file_info_factory, file_conversion_queue,
                                                       desired_suffix):
    logger.debug(f"In _populate_file_copy_queue_ending_with_a_stop with {locals()}")
    _populate_file_converstion_queue(raw_files_folder, file_info_factory, file_conversion_queue, desired_suffix)
    logger.debug(f"Adding NoMoreRawFiles() to the file_copy_queue.")
    file_conversion_queue.put(NoMoreRawFiles())


def _populate_file_converstion_queue(raw_files_folder, file_info_factory, file_conversion_queue, desired_suffix):
    logger.debug(f"In _populate_file_copy_queue with {locals()}")
    for raw_item in raw_files_folder.iterdir():
        logger.debug(f"In _populate_file_copy_queue, working on {object_cleaner(raw_item)}")
        if raw_item.is_file():
            logger.debug("Is File.")
            if not raw_item.suffix.casefold() == desired_suffix.casefold():
                logger.debug(f"Not the desired suffix. {raw_item.suffix}\t{desired_suffix}")
                continue

            this_file = file_info_factory(_ConversionFileInformationType.Raw_File, raw_item)
            logger.debug("Adding file to copy queue.")
            file_conversion_queue.put(this_file)
        else:
            logger.debug("Is dir.")
            _populate_file_converstion_queue(raw_item, file_info_factory, file_conversion_queue, desired_suffix)


def _convert_file(file_conversion_queue, file_deletion_queue, call_ffmpeg):
    logger.debug(f"In _convert_file with {locals()}")
    while True:
        try:
            this_file = file_conversion_queue.get(block=True)
        except Empty:
            logger.debug("file_conversion_queue empty.")
            return
        if this_file.file_info_type == _ConversionFileInformationType.NoMoreRawFiles:
            logger.debug("NoMoreRawFiles reached.")
            file_conversion_queue.task_done()
            file_conversion_queue.put(this_file)
            # Reinsert the 'stop' file (to pass the stop message along to the other threads) before stopping
            #  this thread.
            return
        elif this_file.file_info_type == _ConversionFileInformationType.Raw_File:
            logger.debug(f"Converting {object_cleaner(this_file.source_path)}")

            completed_process = call_ffmpeg(
                input_file_path=str(this_file.source_path),
                output_file_path=str(this_file.destination_path)
            )
            file_conversion_queue.task_done()
            this_file.converted()
            if completed_process.returncode == 0:
                logger.debug("Return code good.")
                file_deletion_queue.put(this_file)
            else:
                logger.warning(f"Return code bad: {completed_process.returncode} \t {object_cleaner(this_file)}")
        else:
            logger.warning(f"File is not raw, but is still in the file conversion queue. {this_file}")


def run_script(arguments):
    logger.debug(f"Starting run_script with {arguments}")
    call_ffmpeg = partial(ffmpeg.call, codec="mp3", bitrate=arguments.bitrate,
                          executable_path=arguments.ffmpeg_executable)
    if arguments.yesterday_flag:
        archive_yesterdays_files(arguments, call_ffmpeg)
    else:
        archive_list_of_folders(arguments, call_ffmpeg)
