"""
@Author = 'Mike Stanley'

============ Change Log ============
2018-May-02 = Created.

============ License ============
The MIT License (MIT)

Copyright (c) 2018 Michael Stanley

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
from queue import Queue, Empty
from wmul_file_manager.ConvertFolderToMP3 import _ConversionFileInformationType
from wmul_file_manager.ConvertFolderToMP3 import NoMoreRawFiles
from wmul_file_manager import ConvertFolderToMP3
import datetime
import logging
import pathlib
import pytest
import threading
import time


'''Queue Helpers'''


def get_items_from_queue(input_queue):
    items_in_queue = []

    while True:
        try:
            item = input_queue.get(block=False)
            items_in_queue.append(item)
        except Empty:
            break

    return items_in_queue


def assert_queue_empty(input_queue):
    with pytest.raises(Empty):
        input_queue.get(block=False)


'''Guardian Classes tests'''


def test_no_more_raw_files():
    assert NoMoreRawFiles.file_info_type == _ConversionFileInformationType.NoMoreRawFiles


'''archive_yesterdays_files tests'''


@pytest.fixture(scope="function")
def setup_archive_yesterdays_files(mocker, tmpdir):
    mock_today = mocker.Mock(return_value=datetime.date(year=2018, month=5, day=4))
    mock_date = mocker.Mock(today=mock_today)
    mocker.patch("wmul_file_manager.ConvertFolderToMP3.date", mock_date)

    mock__archive_folder = mocker.patch("wmul_file_manager.ConvertFolderToMP3._archive_folder")
    folder1 = pathlib.Path(tmpdir.join("folder1"))
    folder2 = pathlib.Path(tmpdir.join("folder2"))
    yesterday_folder = folder1 / "2018-05-03"
    yesterday_folder_mp3 = folder1 / "2018-05-03_mp3"

    call_ffmpeg = "mock_call_ffmpeg"

    yield mock__archive_folder, folder1, folder2, yesterday_folder, yesterday_folder_mp3, call_ffmpeg


def test_archive_yesterdays_files_both_exist_same_folder(setup_archive_yesterdays_files, mocker):
    """
    GIVEN a list of two folders, both of which exist, a yesterday_folder that exists under the first folder, and a
        false separate_folder_flag,
    WHEN archive_yesterdays_files is called,
    THEN It will call _archive_folder once with the yesterday_folder as both the raw_files_folder and
        converted_files_final_folder arguments. The input args 'arguments' and 'call_ffmpeg' will also be passed in.
    """
    mock__archive_folder, folder1, folder2, yesterday_folder, _, call_ffmpeg = setup_archive_yesterdays_files

    folder1.mkdir(parents=True, exist_ok=True)
    folder2.mkdir(parents=True, exist_ok=True)
    yesterday_folder.mkdir(parents=True, exist_ok=True)

    arguments = mocker.Mock(source_paths=[folder1, folder2], separate_folder_flag=False)
    ConvertFolderToMP3.archive_yesterdays_files(arguments=arguments, call_ffmpeg=call_ffmpeg)

    mock__archive_folder.assert_called_once_with(yesterday_folder, yesterday_folder, arguments, call_ffmpeg)


def test_archive_yesterdays_files_both_exist_sep_folder(setup_archive_yesterdays_files, mocker):
    """
    GIVEN a list of two folders, both of which exist, a yesterday_folder that exists under the first folder, and a
        true separate_folder_flag,
    WHEN archive_yesterdays_files is called
    THEN It will call _archive_folder once with the yesterday_folder as the raw_files_folder argument and the
    yesterday_folder_mp3 as the converted_files_final_folder argument. The input args 'arguments' and 'call_ffmpeg'
    will also be passed in.
    """
    mock__archive_folder, folder1, folder2, yesterday_folder, yesterday_folder_mp3, \
        call_ffmpeg = setup_archive_yesterdays_files

    folder1.mkdir(parents=True, exist_ok=True)
    folder2.mkdir(parents=True, exist_ok=True)
    yesterday_folder.mkdir(parents=True, exist_ok=True)

    arguments = mocker.Mock(source_paths=[folder1, folder2], separate_folder_flag=True)
    ConvertFolderToMP3.archive_yesterdays_files(arguments=arguments, call_ffmpeg=call_ffmpeg)

    mock__archive_folder.assert_called_once_with(yesterday_folder, yesterday_folder_mp3, arguments, call_ffmpeg)


def test_archive_yesterdays_files_extra_doesnt_exist_same_folder(setup_archive_yesterdays_files, mocker):
    """
    GIVEN a list of two folders, only the first of which exists, a yesterday_folder that exists under the first folder,
        and a false separate_folder_flag,
    WHEN archive_yesterdays_files is called
    THEN It will still call _archive_folder. The fact that the extra folder does not exist is irrelevant.
    """
    mock__archive_folder, folder1, folder2, yesterday_folder, _, call_ffmpeg = setup_archive_yesterdays_files

    folder1.mkdir(parents=True, exist_ok=True)
    yesterday_folder.mkdir(parents=True, exist_ok=True)

    arguments = mocker.Mock(source_paths=[folder1, folder2], separate_folder_flag=False)
    ConvertFolderToMP3.archive_yesterdays_files(arguments=arguments, call_ffmpeg=call_ffmpeg)

    mock__archive_folder.assert_called_once_with(yesterday_folder, yesterday_folder, arguments, call_ffmpeg)


def test_archive_yesterdays_files_extra_doesnt_exist_sep_folder(setup_archive_yesterdays_files, mocker):
    """
    GIVEN a list of two folders, only the first of which exists, a yesterday_folder that exists under the first folder,
        and a true separate_folder_flag,
    WHEN archive_yesterdays_files is called
    THEN It will still call _archive_folder. The fact that the extra folder does not exist is irrelevant.
    """
    mock__archive_folder, folder1, folder2, yesterday_folder, yesterday_folder_mp3, \
        call_ffmpeg = setup_archive_yesterdays_files

    folder1.mkdir(parents=True, exist_ok=True)
    yesterday_folder.mkdir(parents=True, exist_ok=True)

    arguments = mocker.Mock(source_paths=[folder1, folder2], separate_folder_flag=True)
    ConvertFolderToMP3.archive_yesterdays_files(arguments=arguments, call_ffmpeg=call_ffmpeg)

    mock__archive_folder.assert_called_once_with(yesterday_folder, yesterday_folder_mp3, arguments, call_ffmpeg)


def test_archive_yesterdays_files_main_doesnt_exist_same_folder(setup_archive_yesterdays_files, mocker, caplog):
    """
    GIVEN a list of two folders, both of which exist, a yesterday_folder does not exist under the first folder, and a
        false separate_folder_flag,
    WHEN archive_yesterdays_files is called
    THEN It will not call _archive_folder and an error message will be logged.
    """
    mock__archive_folder, folder1, folder2, yesterday_folder, _, call_ffmpeg = setup_archive_yesterdays_files

    folder1.mkdir(parents=True, exist_ok=True)
    folder2.mkdir(parents=True, exist_ok=True)

    arguments = mocker.Mock(source_paths=[folder1, folder2], separate_folder_flag=False)
    ConvertFolderToMP3.archive_yesterdays_files(arguments=arguments, call_ffmpeg=call_ffmpeg)

    mock__archive_folder.assert_not_called()
    assert "Yesterday's folder does not exist. " in caplog.text


def test_archive_yesterdays_files_main_doesnt_exist_sep_folder(setup_archive_yesterdays_files, mocker, caplog):
    """
    GIVEN a list of two folders, both of which exist, a yesterday_folder does not exist under the first folder, and a
        true separate_folder_flag,
    WHEN archive_yesterdays_files is called
    THEN It will not call _archive_folder and an error message will be logged.
    """
    mock__archive_folder, folder1, folder2, yesterday_folder, _, call_ffmpeg = setup_archive_yesterdays_files

    folder1.mkdir(parents=True, exist_ok=True)
    folder2.mkdir(parents=True, exist_ok=True)

    arguments = mocker.Mock(source_paths=[folder1, folder2], separate_folder_flag=True)
    ConvertFolderToMP3.archive_yesterdays_files(arguments=arguments, call_ffmpeg=call_ffmpeg)

    mock__archive_folder.assert_not_called()
    assert "Yesterday's folder does not exist. " in caplog.text


"""archive_list_of_folders tests"""


@pytest.fixture(scope="function")
def setup_archive_list_of_folders(mocker, tmpdir):
    mock__archive_folder = mocker.patch("wmul_file_manager.ConvertFolderToMP3._archive_folder")
    folder1 = pathlib.Path(tmpdir.join("folder1"))
    folder2 = pathlib.Path(tmpdir.join("folder2"))
    tmp_path = pathlib.Path(tmpdir)
    call_ffmpeg = "mock_call_ffmpeg"

    yield mock__archive_folder, folder1, folder2, tmp_path, call_ffmpeg


def test_archive_list_of_folders_all_folders_exist_same_folder(setup_archive_list_of_folders, mocker):
    """
    GIVEN a list of two folders, both of which exist, and a false separate_folder_flag,
    WHEN archive_yesterdays_files is called,
    THEN It will call _archive_folder for each source_folder with the source_folder as both the raw_files_folder and
        converted_files_final_folder arguments. The input args 'arguments' and 'call_ffmpeg' will also be passed in.
    """
    mock__archive_folder, folder1, folder2, _, call_ffmpeg = setup_archive_list_of_folders

    folder1.mkdir(parents=True, exist_ok=True)
    folder2.mkdir(parents=True, exist_ok=True)
    arguments = mocker.Mock(source_paths=[folder1, folder2], separate_folder_flag=False)

    ConvertFolderToMP3.archive_list_of_folders(arguments=arguments, call_ffmpeg=call_ffmpeg)

    expected_calls = [
        mocker.call(folder1, folder1, arguments, call_ffmpeg),
        mocker.call(folder2, folder2, arguments, call_ffmpeg)
    ]

    mock__archive_folder.assert_has_calls(expected_calls)
    assert mock__archive_folder.call_count == 2


def test_archive_list_of_folders_all_folders_exist_sep_folders(setup_archive_list_of_folders, mocker):
    """
    GIVEN a list of two folders, both of which exist, and a true separate_folder_flag,
    WHEN archive_yesterdays_files is called,
    THEN It will call _archive_folder for each source_folder with the source_folder as the raw_files_folder argument
        and source_folder_mp3 as the converted_files_final_folder argument. The input args 'arguments' and
        'call_ffmpeg' will also be passed in.
    """
    mock__archive_folder, folder1, folder2, tmp_path, call_ffmpeg = setup_archive_list_of_folders

    folder1.mkdir(parents=True, exist_ok=True)
    folder2.mkdir(parents=True, exist_ok=True)
    arguments = mocker.Mock(source_paths=[folder1, folder2], separate_folder_flag=True)

    ConvertFolderToMP3.archive_list_of_folders(arguments=arguments, call_ffmpeg=call_ffmpeg)

    expected_calls = [
        mocker.call(folder1, tmp_path / "folder1_mp3", arguments, call_ffmpeg),
        mocker.call(folder2, tmp_path / "folder2_mp3", arguments, call_ffmpeg)
    ]

    mock__archive_folder.assert_has_calls(expected_calls)
    assert mock__archive_folder.call_count == 2


def test_archive_list_of_folders_one_folder_doesnt_exist_same_folder(setup_archive_list_of_folders, mocker, caplog):
    """
    GIVEN a list of two folders, only one of which exists, and a false separate_folder_flag,
    WHEN archive_yesterdays_files is called,
    THEN It will call _archive_folder normally for the source_folder that exists and logs an error message for the
        source_folder that does not exist.
    """
    mock__archive_folder, folder1, folder2, _, call_ffmpeg = setup_archive_list_of_folders

    folder1.mkdir(parents=True, exist_ok=True)
    arguments = mocker.Mock(source_paths=[folder1, folder2], separate_folder_flag=False)

    ConvertFolderToMP3.archive_list_of_folders(arguments=arguments, call_ffmpeg=call_ffmpeg)

    mock__archive_folder.assert_called_once_with(folder1, folder1, arguments, call_ffmpeg)
    assert "Folder does not exist." in caplog.text


def test_archive_list_of_folders_one_folder_doesnt_exist_sep_folders(setup_archive_list_of_folders, mocker, caplog):
    """
    GIVEN a list of two folders, only one of which exists, and a true separate_folder_flag,
    WHEN archive_yesterdays_files is called,
    THEN It will call _archive_folder normally for the source_folder that exists and logs an error message for the
        source_folder that does not exist.
    """
    mock__archive_folder, folder1, folder2, tmp_path, call_ffmpeg = setup_archive_list_of_folders

    folder1.mkdir(parents=True, exist_ok=True)
    arguments = mocker.Mock(source_paths=[folder1, folder2], separate_folder_flag=True)

    ConvertFolderToMP3.archive_list_of_folders(arguments=arguments, call_ffmpeg=call_ffmpeg)

    mock__archive_folder.assert_called_once_with(folder1, tmp_path / "folder1_mp3", arguments, call_ffmpeg)
    assert "Folder does not exist" in caplog.text


"""_archive_folder tests"""


@pytest.fixture(scope="function", params=[True, False])
def setup__archive_folder(mocker, request):
    delete_files_flag = request.param
    mock_file_info_factory = mocker.Mock()
    mock_get_factory = mocker.patch(
        "wmul_file_manager.ConvertFolderToMP3._ConversionFileInformation.get_factory",
        mocker.Mock(return_value=mock_file_info_factory)
    )

    mock_populate_file_conversion_queue_ending_with_a_stop = mocker.patch(
        "wmul_file_manager.ConvertFolderToMP3._populate_file_conversion_queue_ending_with_a_stop"
    )
    mock_conversion_threads = [
        mocker.Mock(),
        mocker.Mock(),
    ]
    mock_spin_up_conversion_threads = mocker.Mock(return_value=mock_conversion_threads)
    mocker.patch("wmul_file_manager.ConvertFolderToMP3._spin_up_conversion_threads", mock_spin_up_conversion_threads)
    mock_delete_files = mocker.patch("wmul_file_manager.ConvertFolderToMP3._delete_files")

    raw_files_folder = "mock_raw_files_folder"
    converted_files_final_folder = "mock_converted_files_final_folder"
    arguments = mocker.Mock(
        desired_suffix="mock_desired_suffix",
        max_conversion_threads="mock_conversion_threads",
        delete_files_flag=delete_files_flag
    )
    call_ffmpeg = "mock_call_ffmpeg"

    ConvertFolderToMP3._archive_folder(
        raw_files_folder=raw_files_folder,
        converted_files_final_folder=converted_files_final_folder,
        arguments=arguments,
        call_ffmpeg=call_ffmpeg
    )

    return locals()


def test__archive_folder__get_factory_called_correctly(setup__archive_folder):
    """
    GIVEN that _archive_folder is called
    THEN it should call _ConversionFileInformation.get_factory once with raw_files_folder, temp_path, and
        converted_files_final_folder as arguments.
    """
    mock_get_factory = setup__archive_folder["mock_get_factory"]
    raw_files_folder = setup__archive_folder["raw_files_folder"]
    converted_files_final_folder = setup__archive_folder["converted_files_final_folder"]

    mock_get_factory.assert_called_once_with(
        raw_files_folder,
        converted_files_final_folder
    )


def test__archive_folder__populate_file_conversion_queue_ending_with_a_stop_called_correctly(setup__archive_folder):
    """
    GIVEN that _archive_folder is called
    THEN it should call _populate_file_copy_queue_ending_with_a_stop once with raw_files_folder, the factory retrieved
        from _ConversionFileInformation.get_factory, desired_suffix, and a queue.Queue as arguments.
    """
    raw_files_folder = setup__archive_folder["raw_files_folder"]
    arguments = setup__archive_folder["arguments"]
    mock_file_info_factory = setup__archive_folder["mock_file_info_factory"]
    mock_populate_file_conversion_queue_ending_with_a_stop = \
        setup__archive_folder["mock_populate_file_conversion_queue_ending_with_a_stop"]

    mock_populate_file_conversion_queue_ending_with_a_stop.assert_called_once()
    mock_call_args, mock_call_kwargs = mock_populate_file_conversion_queue_ending_with_a_stop.call_args
    raw_files_folder_arg, file_info_factory_arg, file_copy_queue_arg, desired_suffix_arg = mock_call_args

    assert raw_files_folder_arg == raw_files_folder
    assert file_info_factory_arg == mock_file_info_factory
    assert isinstance(file_copy_queue_arg, Queue)
    assert desired_suffix_arg == arguments.desired_suffix


def test__archive_folder__spin_up_conversion_threads_called_correctly(setup__archive_folder):
    """
    GIVEN that _archive_folder is called
    THEN it should call _spin_up_conversion_threads once with max_conversion_threads, call_ffmpeg,
        three queue.Queue 's as arguments.
    """
    arguments = setup__archive_folder["arguments"]
    mock_spin_up_conversion_threads = setup__archive_folder["mock_spin_up_conversion_threads"]
    call_ffmpeg = setup__archive_folder["call_ffmpeg"]

    mock_spin_up_conversion_threads.assert_called_once()
    mock_call_args, mock_call_kwargs = mock_spin_up_conversion_threads.call_args
    max_conversion_threads_arg, call_ffmpeg_arg, file_conversion_queue_arg, file_deletion_queue_arg = mock_call_args

    assert max_conversion_threads_arg == arguments.max_conversion_threads
    assert call_ffmpeg_arg == call_ffmpeg
    assert isinstance(file_conversion_queue_arg, Queue)
    assert isinstance(file_deletion_queue_arg, Queue)


def test__archive_folder__conversion_threads_joined(setup__archive_folder):
    """
    GIVEN that _archive_folder is called
    THEN it should call the .join method on each of the conversion threads.
    """
    mock_conversion_threads = setup__archive_folder["mock_conversion_threads"]
    for item in mock_conversion_threads:
        item.join.assert_called_once()


def test__archive_folder__delete_files_called_correctly(setup__archive_folder):
    """
    GIVEN that _archive_folder is called
    IF delete_files_flag is true
    THEN it should call _delete_files with a queue.Queue as argument.
    IF delete_files_flag is false
    THEN it should not call _delete_files
    """
    delete_files_flag = setup__archive_folder["delete_files_flag"]
    mock_delete_files = setup__archive_folder["mock_delete_files"]

    if delete_files_flag:
        mock_delete_files.assert_called_once()
        mock_call_args, mock_call_kwargs = mock_delete_files.call_args
        file_deletion_queue_arg, = mock_call_args
        assert isinstance(file_deletion_queue_arg, Queue)
    else:
        mock_delete_files.assert_not_called()


def test__archive_folder_same_file_deletion_queue_across_methods(setup__archive_folder):
    """
    GIVEN that _archive_folder is called
    IF delete_files_flag is true
    THEN it should send the same queue.Queue as file_deletion_queue to each of _spin_up_conversion_threads, and
        _delete_files
    IF delete_files_flag is false
    THEN _delete_files will not be called.
    """
    delete_files_flag = setup__archive_folder["delete_files_flag"]
    mock_spin_up_conversion_threads = setup__archive_folder["mock_spin_up_conversion_threads"]
    mock_delete_files = setup__archive_folder["mock_delete_files"]

    if delete_files_flag:
        mock_conversion_call_args, _ = mock_spin_up_conversion_threads.call_args
        _, _, _, file_deletion_queue_from_conversion = mock_conversion_call_args

        mock_delete_call_args, _ = mock_delete_files.call_args
        file_deletion_queue_from_delete, = mock_delete_call_args

        assert file_deletion_queue_from_conversion is file_deletion_queue_from_delete


"""_spin_up_conversion_threads tests"""


@pytest.fixture(scope="function")
def setup__spin_up_conversion_threads(mocker):
    def mock_wait(file_conversion_queue, file_deletion_queue, call_ffmpeg):
        time.sleep(0.5)
        return mocker.DEFAULT
    mock_convert_file = mocker.Mock(side_effect=mock_wait)
    mocker.patch("wmul_file_manager.ConvertFolderToMP3._convert_file", mock_convert_file)

    max_conversion_threads = 4
    call_ffmpeg_ = "foo"
    file_conversion_queue_ = "bar"
    file_deletion_queue_ = "blagoblag"

    threads = ConvertFolderToMP3._spin_up_conversion_threads(
        max_conversion_threads=max_conversion_threads,
        call_ffmpeg=call_ffmpeg_,
        file_conversion_queue=file_conversion_queue_,
        file_deletion_queue=file_deletion_queue_
    )

    yield locals()
    [this_thread.join() for this_thread in threads]


def test__spin_up_conversion_threads_convert_file_called_correctly(setup__spin_up_conversion_threads, mocker):
    """
    GIVEN that _spin_up_conversion_threads has been called.
    THEN it should call _convert_file with arguments of a file_copy_queue, file_conversion_queue, file_deletion_queue,
        and call_ffmpeg. It should call _convert_file once for each thread it spins up, equal to max_conversion_threads.
    """
    file_conversion_queue = setup__spin_up_conversion_threads["file_conversion_queue_"]
    file_deletion_queue = setup__spin_up_conversion_threads["file_deletion_queue_"]
    call_ffmpeg = setup__spin_up_conversion_threads["call_ffmpeg_"]
    max_conversion_threads = setup__spin_up_conversion_threads["max_conversion_threads"]
    mock_convert_file = setup__spin_up_conversion_threads["mock_convert_file"]

    standard_call = mocker.call(
            file_conversion_queue=file_conversion_queue,
            file_deletion_queue=file_deletion_queue,
            call_ffmpeg=call_ffmpeg
    )
    expected_calls = []
    for _ in range(max_conversion_threads):
        expected_calls.append(standard_call)

    mock_convert_file.assert_has_calls(expected_calls)
    assert mock_convert_file.call_count == max_conversion_threads


def test__spin_up_conversion_threads_correct_number_of_threads(setup__spin_up_conversion_threads):
    """
    GIVEN that _spin_up_conversion_threads has been called.
    THEN it should return an iterable (of threads) whose length is equal to max_conversion_threads.
    """
    threads = setup__spin_up_conversion_threads["threads"]
    max_conversion_threads = setup__spin_up_conversion_threads["max_conversion_threads"]
    assert len(threads) == max_conversion_threads


def test__spin_up_conversion_threads_returns_an_iterable_of_threads(setup__spin_up_conversion_threads):
    """
    GIVEN that _spin_up_conversion_threads has been called.
    THEN it should return an iterable. All the items in that iterable should be Threads.
    """
    threads = setup__spin_up_conversion_threads["threads"]

    for item in threads:
        assert isinstance(item, threading.Thread)


"""_delete_files tests"""


@pytest.fixture(scope="function")
def setup__delete_files(mocker, caplog):
    good_files = [
        mocker.Mock(name="good1", original_file_name=mocker.Mock(), file_info_type=_ConversionFileInformationType.Converted_File),
        mocker.Mock(name="good2", original_file_name=mocker.Mock(), file_info_type=_ConversionFileInformationType.Converted_File),
        mocker.Mock(name="good3", original_file_name=mocker.Mock(), file_info_type=_ConversionFileInformationType.Converted_File),
    ]

    bad_files = [
        mocker.Mock(name="bad1", original_file_name=mocker.Mock(), file_info_type=_ConversionFileInformationType.Raw_File),
        mocker.Mock(name="bad2", original_file_name=mocker.Mock(), file_info_type=_ConversionFileInformationType.Raw_File),
        mocker.Mock(name="bad3", original_file_name=mocker.Mock(), file_info_type=_ConversionFileInformationType.Raw_File),
    ]
    all_files = [
        *good_files,
        *bad_files
    ]

    test_deletion_queue = Queue()

    for item in all_files:
        test_deletion_queue.put(item)

    ConvertFolderToMP3._delete_files(test_deletion_queue)

    yield good_files, bad_files, test_deletion_queue, caplog.text


def test__delete_files_deletion_queue_empty(setup__delete_files):
    """
    GIVEN that _delete_files has been called.
    THEN the file_deletion_queue should be empty when it returns.
    """
    _, _, test_deletion_queue, _ = setup__delete_files
    assert_queue_empty(test_deletion_queue)


def test__delete_files_good_files_unlinked(setup__delete_files):
    """
    GIVEN that _delete_files has been called with a file deletion queue containing some files that are marked as
        converted and some other files.
    THEN it should unlink (delete) the files that have been marked as converted.
    """
    good_files, _, _, _ = setup__delete_files
    for item in good_files:
        item.original_file_name.unlink.assert_called_once()


def test__delete_files_bad_files_not_unlinked(setup__delete_files):
    """
    GIVEN that _delete_files has been called with a file deletion queue containing some files that are marked as
        converted and some other files.
    THEN it should not unlink (delete) the other files and it should log an error message for each such file.
    """
    _, bad_files, _, caplog_text = setup__delete_files
    for item in bad_files:
        item.original_file_name.unlink.assert_not_called()
        expected_text = f"File in deletion queue, but not converted. {str(item)}"
        assert expected_text in caplog_text


"""_populate_file_copy_queue_ending_with_a_stop tests"""


def test___populate_file_conversion_queue_ending_with_a_stop(mocker):
    """
    GIVEN that _populate_file_copy_queue_ending_with_a_stop is called with raw_files_folder, file_info_factory,
        file_copy_queue, and desired_suffix arguments.
    THEN it will called _populate_file_copy_queue with those same arguments, and tack a NoMoreRawFiles onto the end
        of the queue. In this test, that should be the only item in the queue.
    """
    mock_pfcc = mocker.Mock()
    mocker.patch("wmul_file_manager.ConvertFolderToMP3._populate_file_converstion_queue", mock_pfcc)

    test_conversion_queue = Queue()

    raw_files_folder = "mock_raw_files_folder"
    file_info_factory = "mock_file_info_factory"
    desired_suffix = "mock_desired_suffix"

    ConvertFolderToMP3._populate_file_conversion_queue_ending_with_a_stop(
        raw_files_folder=raw_files_folder,
        file_info_factory=file_info_factory,
        file_conversion_queue=test_conversion_queue,
        desired_suffix=desired_suffix
    )

    mock_pfcc.assert_called_once_with(raw_files_folder, file_info_factory, test_conversion_queue, desired_suffix)

    first_item_in_queue = test_conversion_queue.get(block=False)
    assert first_item_in_queue.file_info_type == _ConversionFileInformationType.NoMoreRawFiles

    assert_queue_empty(test_conversion_queue)


"""_populate_file_copy_queue tests"""


@pytest.fixture(scope="function")
def setup__populate_file_conversion_queue(fs, mocker):
    root_folder = pathlib.Path(r"test")
    directories = [
        root_folder,
        pathlib.Path(r"test\2")
    ]
    expected_files = [
        pathlib.Path(r"test\2016 Car Bash Promo.wav"),
        pathlib.Path(r"test\OnAir-1-2017-05-30_00-00-00-037.wav"),
        pathlib.Path(r"test\OnAir-1-2017-05-30_00-15-00-144.Wav"),
        pathlib.Path(r"test\OnAir-1-2017-05-30_00-30-00-157.waV"),
        pathlib.Path(r"test\OnAir-1-2017-05-30_00-45-00-208.wav"),
        pathlib.Path(r"test\2\OnAir-1-2017-05-30_01-00-00-017.wav"),
        pathlib.Path(r"test\2\OnAir-1-2017-05-30_01-15-00-067.wav"),
        pathlib.Path(r"test\2\OnAir-1-2017-05-30_01-30-00-127.wav"),
        pathlib.Path(r"test\2\OnAir-1-2017-05-30_01-45-00-195.wav"),
    ]
    unexpected_files = [
        pathlib.Path(r"test\30 Promo SBJ VO.sfk"),
        pathlib.Path(r"test\35 hiss.sfk"),
        pathlib.Path(r"test\2016 Car Bash Promo.mp3"),
        pathlib.Path(r"test\OnAir-1-2017-05-30_00-00-00-037.Mp3"),
    ]
    all_files = [
        *expected_files,
        *unexpected_files
    ]

    for item in directories:
        fs.create_dir(item)

    for item in all_files:
        fs.create_file(item)

    test_conversion_queue = Queue()

    mock_file_info_factory = mocker.Mock()

    ConvertFolderToMP3._populate_file_converstion_queue(
        raw_files_folder=root_folder,
        file_info_factory=mock_file_info_factory,
        file_conversion_queue=test_conversion_queue,
        desired_suffix=".wav"
    )

    return mock_file_info_factory, expected_files, test_conversion_queue


def test__populate_file_copy_queue_file_info_factory_called_correctly(setup__populate_file_conversion_queue, mocker):
    """
    GIVEN that _populate_file_copy_queue is called with a raw_files_folder containing several directories and files,
        some of which end in .wav and some of which do not, and a desired_suffix of .wav,
    THEN file_info_factory should be called for each of the files ending in .wav and only those files.
    """
    mock_file_info_factory, expected_files, _ = setup__populate_file_conversion_queue

    expected_calls = [mocker.call(_ConversionFileInformationType.Raw_File, item) for item in expected_files]
    mock_file_info_factory.assert_has_calls(expected_calls, any_order=True)

    assert mock_file_info_factory.call_count == len(expected_files)


def test__populate_file_copy_queue_queue_has_correct_number_of_items(setup__populate_file_conversion_queue):
    """
    GIVEN that _populate_file_copy_queue is called
    THEN the test_copy_queue should have the same number of items as expected_files.
    """
    _, expected_files, test_copy_queue = setup__populate_file_conversion_queue
    items_in_copy_queue = get_items_from_queue(test_copy_queue)
    assert len(items_in_copy_queue) == len(expected_files)


"""_convert_file tests"""


@pytest.fixture(scope="function")
def setup__convert_file(mocker, caplog):
    caplog.set_level(logging.DEBUG)

    def mock_ffmpeg_method(input_file_path, output_file_path):
        if input_file_path[0] == "X":
            return mocker.Mock(returncode=-1)
        else:
            return mocker.Mock(returncode=0)

    mock_ffmpeg = mocker.Mock(wraps=mock_ffmpeg_method)

    test_conversion_queue = Queue()
    test_deletion_queue = Queue()

    good_files = [
        mocker.Mock(source_path="foo7.txt", destination_path="foo8.txt",
                    file_info_type=_ConversionFileInformationType.Raw_File),
        mocker.Mock(source_path="foo9.txt", destination_path="foo10.txt",
                    file_info_type=_ConversionFileInformationType.Raw_File),
        mocker.Mock(source_path="foo11.txt", destination_path="foo12.txt",
                    file_info_type=_ConversionFileInformationType.Raw_File),
    ]

    bad_files = [
        mocker.Mock(source_path="Xfoo13.txt", destination_path="foo14.txt",
                    file_info_type=_ConversionFileInformationType.Raw_File),
    ]

    raw_files = [
        *good_files,
        *bad_files
    ]

    for item in raw_files:
        test_conversion_queue.put(item)

    test_conversion_queue.put(NoMoreRawFiles)

    ConvertFolderToMP3._convert_file(
        file_conversion_queue=test_conversion_queue,
        file_deletion_queue=test_deletion_queue,
        call_ffmpeg=mock_ffmpeg
    )
    caplog_text = caplog.text
    return locals()


def test__convert_file_correct_items_in_conversion_queue(setup__convert_file):
    """
    GIVEN that _convert_file_ has been called,
    THEN the first and only item remaining in the conversion_queue should be a NoMoreRawFiles.
    """
    test_conversion_queue = setup__convert_file["test_conversion_queue"]

    first_item_in_conversion_queue = test_conversion_queue.get(block=False)
    assert first_item_in_conversion_queue.file_info_type == _ConversionFileInformationType.NoMoreRawFiles
    assert_queue_empty(test_conversion_queue)


def test__convert_file_correct_items_in_deletion_queue(setup__convert_file):
    """
    GIVEN that _convert_file has been called,
    THEN the deletion_queue should contain each item in good_files and only those items.
    """
    test_deletion_queue = setup__convert_file["test_deletion_queue"]
    good_files = setup__convert_file["good_files"]

    items_in_test_deletion_queue = get_items_from_queue(test_deletion_queue)
    assert len(good_files) == len(items_in_test_deletion_queue)

    for item in good_files:
        assert item in items_in_test_deletion_queue


def test__convert_file_logger_warned_about_bad_file(setup__convert_file):
    """
    GIVEN that _convert_file has been called,
    THEN a log message should be made for each bad file.
    """
    caplog_text = setup__convert_file["caplog_text"]
    expected_string = "Return code bad: -1 \t <Mock id='"
    assert expected_string in caplog_text


def test__convert_file_all_files_file_converted_called(setup__convert_file):
    """
    GIVEN that _convert_file has been called,
    THEN each file should have had its file_converted method called exactly once.
    """
    raw_files = setup__convert_file["raw_files"]
    for item in raw_files:
        item.converted.assert_called_once()


def test__convert_file_ffmpeg_called_correctly(setup__convert_file):
    """
    GIVEN that _convert_file has been called,
    THEN for each file, call_ffmpeg should have been called with that file's arguments. call_ffmpeg should be called
        only that many times.
    """
    raw_files = setup__convert_file["raw_files"]
    mock_ffmpeg = setup__convert_file["mock_ffmpeg"]

    for item in raw_files:
        mock_ffmpeg.assert_any_call(input_file_path=item.source_path, output_file_path=item.destination_path)

    assert mock_ffmpeg.call_count == len(raw_files)


"""run_script tests"""


@pytest.fixture(scope="function")
def setup_run_script(mocker):
    mock_ffmpeg = mocker.patch("wmul_file_manager.utilities.ffmpeg.call")
    mock_yesterdays_files = mocker.patch("wmul_file_manager.ConvertFolderToMP3.archive_yesterdays_files")
    mock_list_of_folders = mocker.patch("wmul_file_manager.ConvertFolderToMP3.archive_list_of_folders")

    bitrate = "mock_bitrate"
    executable_path = "mock_executable_path"

    yield mock_ffmpeg, mock_yesterdays_files, mock_list_of_folders, bitrate, executable_path


def test_run_script_yesterday(setup_run_script, mocker):
    """
    GIVEN that run_script is called with arguments including a yesterday_flag of True,
    THEN it should call archive_yesterdays_files with those arguments.
    """
    mock_ffmpeg, mock_yesterdays_files, _, bitrate, executable_path = setup_run_script
    arguments = mocker.Mock(bitrate=bitrate, ffmpeg_executable=executable_path, yesterday_flag=True)
    ConvertFolderToMP3.run_script(arguments=arguments)
    assert_run_script_called_correctly(arguments, bitrate, executable_path, mock_ffmpeg, mock_yesterdays_files)


def test_run_script_list(setup_run_script, mocker):
    """
    GIVEN that run_script is called with arguments including a yesterday_flag of False,
    THEN it should call archive_list_of_folders with those arguments.
    """
    mock_ffmpeg, _, mock_list_of_folders, bitrate, executable_path = setup_run_script
    arguments = mocker.Mock(bitrate=bitrate, ffmpeg_executable=executable_path, yesterday_flag=False)
    ConvertFolderToMP3.run_script(arguments=arguments)
    assert_run_script_called_correctly(arguments, bitrate, executable_path, mock_ffmpeg, mock_list_of_folders)


def assert_run_script_called_correctly(arguments, bitrate, executable_path, mock_ffmpeg, mock_under_test):
    mock_under_test.assert_called_once()
    mock_call_args, mock_call_kwargs = mock_under_test.call_args
    arguments_arg, partial_ffmpeg_arg = mock_call_args
    partial_ffmpeg_kwags = partial_ffmpeg_arg.keywords
    assert arguments_arg == arguments
    assert partial_ffmpeg_arg.func == mock_ffmpeg
    assert partial_ffmpeg_kwags['codec'] == 'mp3'
    assert partial_ffmpeg_kwags['bitrate'] == bitrate
    assert partial_ffmpeg_kwags['executable_path'] == executable_path
