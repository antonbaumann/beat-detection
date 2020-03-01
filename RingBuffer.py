class RingBuffer:
	def __init__(self, size) -> None:
		self.size = size
		self.data = [0] * self.size
		self.index = 0

	def put(self, value) -> None:
		self.data[self.index % self.size] = value
		self.index += 1

	def values(self) -> list:
		return self.data[self.index:] + self.data[:self.index]

	def is_ready(self) -> bool:
		return self.index >= self.size
