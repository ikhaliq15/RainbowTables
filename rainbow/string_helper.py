import random

def random_string(string_length, alphabet):
	return ''.join(random.choice(alphabet) for _ in range(string_length))