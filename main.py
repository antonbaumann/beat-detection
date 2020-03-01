from scipy.io.wavfile import read
import matplotlib.pyplot as plt
import numpy as np
import RingBuffer
import time


def read_wav_file(path):
	wav_data = read(path)
	rate = wav_data[0]
	data = wav_data[1]
	return rate, data


def normalize(data):
	return data / np.max(data)


def calculate_energy(data) -> float:
	return sum([np.sum(np.square(frame)) for frame in data])


def main():
	print('reading file ...')
	rate, data = read_wav_file("testdata/120bpm_metronome.wav")

	second_start = 0
	second_end = 10
	data = data[rate * second_start:rate * second_end]

	data = normalize(data)

	# init ring buffer
	seconds = 1
	frames = rate * seconds
	block_size = 2048
	buffer_size = frames // block_size

	print(f'frames:     {frames}')
	print(f'blocksize:  {block_size}')
	print(f'buffersize: {buffer_size}')

	index = 0

	ring_buffer = RingBuffer.RingBuffer(buffer_size)
	peaks = []

	time_start = time.time()
	while index < len(data) - block_size:
		# calculate average energy in buffer
		values = ring_buffer.values()
		avg = sum(values) / len(values)

		# calculate current energy
		block = data[index:index+block_size]
		energy = calculate_energy(block)

		# calculate variance
		variance = sum([np.square(e - avg) for e in values]) / buffer_size
		c = (-0.0000015 * variance) + 1.5142857

		# if current energy over threshold -> add to peaks
		if ring_buffer.is_ready() and energy > avg * c:
			peaks.append(index)

		ring_buffer.put(energy)
		index += block_size

	time_end = time.time()
	print(f'took {time_end-time_start} seconds for {second_end-second_start} seconds of audio')

	fig, ax = plt.subplots()

	# add second x axis showing seconds
	ax2 = ax.secondary_xaxis(
		"top",
		functions=(
			lambda x: x / rate,
			lambda x: x * rate
		)
	)

	ax2.set_xlabel("seconds")
	ax.set_xlabel("frames")

	plt.plot(data)
	for peak in peaks:
		plt.axvline(peak, color='r')
	plt.show()


if __name__ == '__main__':
	main()
