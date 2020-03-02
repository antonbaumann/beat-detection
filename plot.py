import matplotlib.pyplot as plt


def plot_beats(data, frame_rate, beats):
	fig, ax = plt.subplots()

	# add second x axis showing seconds
	ax2 = ax.secondary_xaxis(
		"top",
		functions=(
			lambda x: x / frame_rate,
			lambda x: x * frame_rate
		)
	)

	ax2.set_xlabel("seconds")
	ax.set_xlabel("frames")

	plt.plot(data)
	for beat in beats:
		plt.axvline(beat, color='r')
	plt.show()
