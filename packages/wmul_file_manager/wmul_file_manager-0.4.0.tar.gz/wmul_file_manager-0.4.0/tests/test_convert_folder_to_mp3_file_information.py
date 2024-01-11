"""
@Author = 'Mike Stanley'

============ Change Log ============
2018-May-01 = Created.

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
import pytest
import random
from pathlib import Path
from wmul_file_manager.ConvertFolderToMP3 import _ConversionFileInformation
from wmul_file_manager.ConvertFolderToMP3 import _ConversionFileInformationType


@pytest.fixture(scope="function")
def setup_file_information(request):
    yield request.getfixturevalue(request.param)


@pytest.fixture(scope="function")
def setup_file_information_common(tmpdir):
    src_root = tmpdir.join("src")
    src_root.ensure(dir=True)

    src_file = src_root.join("temp.txt")
    src_file.write_binary(bytearray(random.randint(0, 255) for i in range(100)))

    converted_files_final_folder = tmpdir.join("dst")

    src_file = Path(src_file)
    src_root = Path(src_root)
    tmpdir_path = Path(tmpdir)
    converted_files_final_folder = Path(converted_files_final_folder)

    yield src_file, src_root, converted_files_final_folder, tmpdir_path


@pytest.fixture(scope="function")
def setup_file_information_init(setup_file_information_common):
    src_file, src_root, converted_files_final_folder, tmpdir_path = setup_file_information_common

    file_info = _ConversionFileInformation(
        file_info_type=_ConversionFileInformationType.Raw_File,
        source_file_path=src_file,
        source_root_path=src_root,
        converted_files_final_folder=converted_files_final_folder
    )
    yield file_info, src_file, tmpdir_path


@pytest.fixture(scope="function")
def setup_file_information_factory(setup_file_information_common):
    src_file, src_root, converted_files_final_folder, tmpdir_path = setup_file_information_common

    file_info_factory = _ConversionFileInformation.get_factory(
        root_path=src_root,
        converted_files_final_folder=converted_files_final_folder
    )

    file_info = file_info_factory(
        file_info_type=_ConversionFileInformationType.Raw_File,
        source_file_path=src_file
    )

    yield file_info, src_file, tmpdir_path


@pytest.mark.parametrize("setup_file_information", ["setup_file_information_init", "setup_file_information_factory"],
                         indirect=True)
def test_file_information_file_info_type(setup_file_information):
    file_info, _, _ = setup_file_information
    assert file_info.file_info_type == _ConversionFileInformationType.Raw_File


@pytest.mark.parametrize("setup_file_information", ["setup_file_information_init", "setup_file_information_factory"],
                         indirect=True)
def test_file_information_original_file_name(setup_file_information):
    file_info, src_file, _ = setup_file_information
    assert file_info.original_file_name == src_file


@pytest.mark.parametrize("setup_file_information", ["setup_file_information_init", "setup_file_information_factory"],
                         indirect=True)
def test_file_information_source_path(setup_file_information):
    file_info, src_file, _ = setup_file_information
    assert file_info.source_path == src_file


@pytest.mark.parametrize("setup_file_information", ["setup_file_information_init", "setup_file_information_factory"],
                         indirect=True)
def test_file_information_destination_path(setup_file_information):
    file_info, _, tmpdir_path = setup_file_information
    expected_final_file_name = tmpdir_path / "dst" / "temp.mp3"
    assert file_info.destination_path == expected_final_file_name


@pytest.mark.parametrize("setup_file_information", ["setup_file_information_init", "setup_file_information_factory"],
                         indirect=True)
def test_file_information_parents_created(setup_file_information):
    file_info, _, _ = setup_file_information
    assert file_info.destination_path.parent.exists()


@pytest.mark.parametrize("setup_file_information", ["setup_file_information_init", "setup_file_information_factory"],
                         indirect=True)
def test_file_information_str(setup_file_information):
    file_info, src_file, _ = setup_file_information
    assert str(file_info) == f"_ConversionFileInformation:\n_ConversionFileInformationType.Raw_File\n{src_file}"

