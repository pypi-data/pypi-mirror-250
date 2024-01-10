# SPDX-FileCopyrightText: 2024-present Anfeng Li <laf070810@163.com>
#
# SPDX-License-Identifier: MIT

import ctypes
import multiprocessing
import os
import sys
import time


class Tee(object):
    """
    Class used to grab standard output or another stream.
    """
    escape_char = "\b"

    def __init__(self, streams=None, output_filepath=None, threaded=True):
        if streams is None:
            self.original_streams = [sys.stdout, sys.stderr]
        elif isinstance(streams, list):
            self.original_streams = streams
        else:
            self.original_streams = [streams]
        self.output_filepath = output_filepath
        self.threaded = threaded

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, type, value, traceback):
        self.stop()

    def start(self):
        """
        Start capturing the stream data.
        """
        if self.output_filepath is None:
            self.output_file = None
        else:
            self.output_file = open(self.output_filepath, 'w')
        self.manager = multiprocessing.Manager()
        self.capturedtext = self.manager.Value(ctypes.c_wchar_p, '')
        self.original_stream_fds = [original_stream.fileno() for original_stream in self.original_streams]
        # Save a copy of the stream:
        self.duplicated_stream_fds = [os.dup(original_stream_fd) for original_stream_fd in self.original_stream_fds]
        self.duplicated_stdout = open(os.dup(sys.stdout.fileno()), 'w')
        # Create a pipe so the stream can be captured:
        self.pipe_out, self.pipe_in = os.pipe()
        # Replace the original stream with our write pipe:
        for original_stream_fd in self.original_stream_fds:
            os.dup2(self.pipe_in, original_stream_fd)
        if self.threaded:
            # Start thread that will read the stream:
            self.worker_thread = multiprocessing.Process(target=self.read_output)
            self.worker_thread.start()
            # Make sure that the thread is running and os.read() has executed:
            time.sleep(0.01)

    def stop(self):
        """
        Stop capturing the stream data and save the text in `capturedtext`.
        """
        # Flush the stream to make sure all our data goes in before
        # the escape character:
        for original_stream in self.original_streams:
            original_stream.flush()
        # Print the escape character to make the read_output method stop:
        os.write(self.pipe_in, self.escape_char.encode(self.original_streams[0].encoding))
        if self.threaded:
            # wait until the thread finishes so we are sure that
            # we have until the last character:
            self.worker_thread.join()
        else:
            self.read_output()
        # Close the pipe:
        os.close(self.pipe_in)
        os.close(self.pipe_out)
        for i in range(len(self.original_stream_fds)):
            # Restore the original stream:
            os.dup2(self.duplicated_stream_fds[i], self.original_stream_fds[i])
            # Close the duplicate stream:
            os.close(self.duplicated_stream_fds[i])
        self.duplicated_stdout.close()
        if self.output_file is not None:
            self.output_file.close()

    def read_output(self):
        """
        Read the stream data (one byte at a time)
        and save the text in `capturedtext`.
        """
        capturedtexts = []
        capturedtext = ''
        while True:
            char = os.read(self.pipe_out, 1).decode(self.original_streams[0].encoding)
            if not char or self.escape_char in char:
                break
            self.duplicated_stdout.write(char)
            if self.output_file is not None:
                self.output_file.write(char)
            capturedtext += char
            if len(capturedtext) >= 1000:
                capturedtexts.append(capturedtext)
                capturedtext = ""
        capturedtexts.append(capturedtext)
        capturedtext = ""
        self.capturedtext.value += ''.join(capturedtexts)
        if self.output_file is not None:
            self.output_file.flush()

    def get_capturedtext(self):
        return self.capturedtext.value
