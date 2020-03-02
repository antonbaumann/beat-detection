import matplotlib.pyplot as plt
import numpy.fft as fft

import plot
from util import read_wav_file

'''
https://soundlab.cs.princeton.edu/publications/2001_amta_aadwt.pdf
'''


def detect_beats(data, frame_rate):
	freq_domain_left = fft.rfft(data[:, 0])
	freq_domain_right = fft.rfft(data[:, 1])
	plt.plot(freq_domain_left)
	plt.show()
	plt.plot(freq_domain_right)
	plt.show()
	pass


def main():
	data, rate = read_wav_file("testdata/take5.wav")
	plot.plot_beats(data, rate, [])
	detect_beats(data, rate)


if __name__ == '__main__':
	main()
