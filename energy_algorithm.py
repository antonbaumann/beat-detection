import time


import numpy as np
from scipy.io.wavfile import write

import RingBuffer
from util import normalize, calculate_energy, apply_beat, read_wav_file
import plot

'''
https://mziccard.me/2015/05/28/beats-detection-algorithms-1/
http://archive.gamedev.net/archive/reference/programming/features/beatdetection/index.html
'''


def detect_beats(data, frame_rate, block_size=1024, buffer_size_seconds=1, scale=True) -> list:
	if scale:
		data = normalize(data)

	# init ring buffer
	frames = frame_rate * buffer_size_seconds
	buffer_size = frames // block_size

	index = 0

	ring_buffer = RingBuffer.RingBuffer(buffer_size)
	peaks = []

	while index < len(data) - block_size:
		# calculate current energy
		block = data[index:index + block_size]
		energy = calculate_energy(block)
		ring_buffer.put(energy)

		values = ring_buffer.values()[:-1]

		# calculate average energy in buffer
		# todo: save sum in buffer and change if new value is inserted
		avg = sum(values) / len(values)

		# calculate variance
		variance = sum([np.square(e - avg) for e in values]) / buffer_size
		c = (-0.0000015 * variance) + 1.5142857

		# if current energy over threshold -> add to peaks
		index_last_peak = peaks[-1] if len(peaks) != 0 else 0
		delta = index - index_last_peak
		min_delta = frame_rate * 0.2
		if ring_buffer.is_ready() and delta >= min_delta and energy > avg * c:
			peaks.append(index)

		index += block_size

	return peaks


def main():
	print('reading file ...')
	data, rate = read_wav_file("testdata/take5.wav")

	# trim sound data
	second_start = 0
	second_end = 30
	data = data[rate * second_start:rate * second_end]

	time_start = time.time()
	peaks = detect_beats(data, rate)
	time_end = time.time()

	print(f'took {time_end - time_start} seconds for {second_end - second_start} seconds of audio')
	bpm = len(peaks) / (second_end - second_start - 1) * 60
	print(f'BPM: {bpm}')

	plot.plot_beats(data, rate, peaks)

	new_data = apply_beat(data, peaks)
	write("out.wav", rate, new_data)


if __name__ == '__main__':
	main()
