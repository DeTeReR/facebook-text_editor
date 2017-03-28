import functools


@functools.lru_cache(None)
def calc_distance(one, two):
	count = 0
	for char_one, char_two in zip(one, two):
		if char_one == char_two:
			count += 1
		else:
			break
	return len(one) + len(two) + 1 - (2 * count)


@functools.lru_cache(None)
def cost(words):
	full_words = words + ('',)
	return sum(calc_distance(full_words[i], full_words[i+1]) for i in range(len(full_words) - 1))


@functools.lru_cache(None)
def min_cost_to_print(words, pages, previous):
	if pages == 0:
		return calc_distance(previous, '')
	elif len(words) == pages:
		return cost((previous,) + words)
	else:
		return min([
			min_cost_to_print(words[1:], pages, previous),
			min_cost_to_print(words[1:], pages - 1, words[0]) + calc_distance(previous, words[0])
		])


def reset():
	for func in (calc_distance, cost, min_cost_to_print):
		func.cache_clear()


def main():
	filename = 'text_editor.txt'
	input_file = open(filename)
	count = int(input_file.readline())
	print('There are {} cases to do'.format(count))
	for i in range(count):
		dictionary_length, pages = input_file.readline().split()
		dictionary_length = int(dictionary_length)
		pages = int(pages)
		words = []
		for j in range(dictionary_length):
			words.append(input_file.readline().strip())
		result = min_cost_to_print(tuple(sorted(words)), pages, '')
		reset()
		print('Case #{}: {}'.format(i+1, result))


if __name__ == '__main__':
	main()