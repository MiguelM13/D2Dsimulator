import numpy as np
import time
from collections import deque


class Buffer:
    """Buffer class
    It's used for record signals, example:

    Initialize buffer with n vars:
    buffer = Buffer(x=0,y=0)

    Recording:
    buffer.record(x=1.3, y=2.4)

    End Record
    buffer.stop()

    :param siglen: max length per signal

    """
    def __init__(self, siglen=5000, **kwargs):
        self.kwargs = kwargs
        self.siglen = siglen
        self.signals = {ID: deque(maxlen=self.siglen) for ID in kwargs.keys()}
        self.time = deque(maxlen=self.siglen)
        self.recording = False
        self.initialTime = 0
        self.currentTime = 0

    def get_data(self):
        """It returns a copy of the storaged data"""
        return dict(self.signals)

    def sample_time(self):
        """It samples the time"""
        if not self.recording:
            self.recording = True
            self.initialTime = time.time()
        self.currentTime = time.time()
        self.time.append(self.currentTime)

    def get_time_count(self):
        """It returns """
        return self.currentTime - self.initialTime

    def fix_time_scale(self):
        """It fixes time scale"""
        dt_vec = np.diff(self.time)
        t = 0
        tvec = [t]
        for dt in dt_vec:
            t += dt
            tvec.append(t)
        self.signals["time"] = np.array(tvec)

    def record(self, **kwargs):
        """It records signals"""
        for ID in kwargs.keys():
            if ID in self.kwargs:
                self.signals[ID].append(kwargs[ID])
        # save the time of sampling
        self.sample_time()

    def print_data(self, lim=8):
        """It prints the signals in a nice format
        :param lim: limit to show elements with list/array indexing
        """
        for ID in self.signals:
            if len(self.signals[ID]) >= lim:
                print(ID, ": ")
                print(self.signals[ID][:lim], "...", self.signals[ID][-lim:])
                print("")
            else:
                print(ID, ":")
                print(self.signals[ID])
                print("")

    def print_size(self):
        """It prints the signals lengths in a nice format"""
        for ID in self.kwargs:
            print("{} -> {} ".format(ID, len(self.signals[ID])))

    def get_size(self):
        """It returns  the size/length of each signal recorded
        :return: size: dictionary with the names of the signals and their lengths
        """
        size = {}
        for ID in self.signals:
            try:
                size[ID] = len(self.signals[ID])
            except Exception as e:
                print(e)
        return size

    def get_length(self):
        """It returns the length of the recorded signals
        :return: length: signals length
        """
        length = len(list(self.signals.values())[0])
        return length

    def generate_time_vector(self, duration=1):
        """It generates a time vector from the signals sampled.
        :param duration: secs.
        """
        length = self.get_length()
        t = np.linspace(0, duration, length)
        self.signals["t_generated"] = t

    def save(self, name="default"):
        """It saves the data
        :param name: file name to save data
        """
        name += ".npy"
        np.save(name, self.signals)

    def data_to_array(self):
        """It converts signals in list format to numpy array format"""
        for ID in self.signals:
            if type(self.signals[ID]) != np.ndarray:
                self.signals[ID] = np.array(self.signals[ID])

    def stop(self, name="default", save=False, clear=False):
        """It processes the data recorded
        :param name: name to storage the data in a file
        :param save: save flag, if it's True then save data
        :param clear:
        :return:
        """
        self.currentTime = 0
        self.initialTime = 0
        self.recording = False
        self.data_to_array()
        self.fix_time_scale()
        self.signals["size"] = self.get_size()

        if save:
            self.save(name)
        if clear:
            self.clear()

    def clear(self):
        """It cleans the buffer"""
        self.currentTime = 0
        self.initialTime = 0
        self.recording = False
        for ID in self.signals:
            self.signals[ID] = deque(maxlen=self.siglen)
        self.time = deque(maxlen=self.siglen)
