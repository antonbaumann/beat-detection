import numpy as np
from scipy.io.wavfile import read


def read_wav_file(path):
	wav_data = read(path)
	rate = wav_data[0]
	data = wav_data[1]
	return data, rate


def normalize(data):
	return data / np.max(data)


def calculate_energy(data) -> float:
	return sum([np.sum(np.square(frame)) for frame in data])


# add clicking noise at beat-positions
# todo: cold be better ...
def apply_beat(data, peaks, block_size=1024):
	data_copy = data.copy()
	for peak in peaks:
		for i in range(peak, peak + block_size):
			data_copy[i] = 1
	return data_copy
