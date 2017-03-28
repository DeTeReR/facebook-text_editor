import functools

import sys


@functools.lru_cache(None)
def calc_distance(words):
	one, two = words
	count = 0
	for char_one, char_two in zip(one, two):
		if char_one == char_two:
			count += 1
		else:
			break
	return len(one) + len(two) + 1 - (2 * count)


class Node(object):
	def __init__(self, word):
		self.word = word
		self.ordered_siblings = []
		self.distances = {}
		self._bests = {}

	def __repr__(self):
		return 'Node({})'.format(self.word)

	def add_sibling(self, other):
		distance = calc_distance(frozenset([self.word, other.word]))
		self.ordered_siblings.append((distance, other))
		self.ordered_siblings.sort(key=lambda x: x[0])
		self.distances[other] = distance

	def is_best(self, others, score):
		previous_score = self._bests.get(others)
		if previous_score is None or previous_score > score:
			self._bests[others] = score
		elif previous_score <= score:
			raise WorseError
		else:
			raise Exception('WTF')


def make_nodes(words):
	root = Node('')
	nodes = [root] + [Node(word.strip()) for word in words]
	for node in nodes:
		for other_node in nodes:
			if node != other_node:
				node.add_sibling(other_node)
	print('There are {} nodes'.format(len(nodes)))
	return root


class WorseError(ValueError):
	pass


def find_thing(root, current_node, pages_remaining, printed, cost_so_far):
	if current_node == root and pages_remaining == 0:
		return cost_so_far

	current_node.is_best(printed, cost_so_far)
	if current_node is not root:
		pages_remaining -= 1
		printed = printed.union(frozenset({current_node}))

	if pages_remaining == 0:
		return find_thing(root, root, pages_remaining, printed, cost_so_far + root.distances[current_node])
	else:
		values = []
		for distance, other_node in current_node.ordered_siblings:
			if other_node in printed:
				continue
			try:
				value = find_thing(
					root, other_node, pages_remaining, printed, cost_so_far + current_node.distances[other_node]
				)
				values.append(value)
			except WorseError:
				continue
		if not values:
			raise WorseError()
		return min(values)


def foo(words, pages):
	root = make_nodes(words)
	return find_thing(root, root, pages, frozenset([]), -1)


def main():
	filename = 'text_editor.txt'
	input_file = open(filename)
	count = int(input_file.readline())
	for i in range(count):
		dictionary_length, pages = input_file.readline().split()
		dictionary_length = int(dictionary_length)
		pages = int(pages)
		words = set()
		for j in range(dictionary_length):
			words.add(input_file.readline())
		sys.setrecursionlimit(dictionary_length * 2)
		result = foo(words, pages)
		print('Case #{}: {}'.format(i+1, result))

if __name__ == '__main__':
	main()