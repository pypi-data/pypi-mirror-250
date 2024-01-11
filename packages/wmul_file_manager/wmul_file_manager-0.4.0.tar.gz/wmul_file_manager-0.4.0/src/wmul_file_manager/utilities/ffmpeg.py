"""
@Author = 'Mike Stanley'

Interface to call ffmpeg from within Python. Note that the executable called need not actually be ffmpeg, it just
needs to obey the same command-line options.

============ Change Log ============
2018-May-01 = Imported from Titanium_Monticello to this project.

              Change bitrate comparisons from equality to greater-than / less-than.

              E.G.
              if bitrate == 320:
                    bitrate = "320000"

              became

              if bitrate > 192:
                    bitrate = "320000"

2017-Aug-11 = Modify to use python 3.5's .run method and to capture stderr and stdout instead of dumping to
                    console.

2015-Feb-25 = Created.

============ License ============
The MIT License (MIT)

Copyright (c) 2015, 2017-2018, 2024 Michael Stanley

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
import subprocess


def call(input_file_path, output_file_path, codec, bitrate, executable_path):
    bitrate = int(bitrate)

    if codec == "mp3":
        codec = "libmp3lame"

    if bitrate > 192:
        bitrate = "320000"
    elif bitrate > 160:
        bitrate = "192000"
    elif bitrate > 96:
        bitrate = "160000"
    elif bitrate <= 96:
        bitrate = "96000"

    return subprocess.run(
        [executable_path, "-i", input_file_path, "-codec:a", codec,  "-b:a", bitrate, output_file_path],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT
    )

