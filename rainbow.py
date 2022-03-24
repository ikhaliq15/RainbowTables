import string_helper
import hashlib
import json
import zlib

class RainbowTable:
	unique_preimages = set()

	def __init__(self, preimage_length, alphabet, num_chains, chain_length):
		self.table = dict()
		self.preimage_length = preimage_length
		self.alphabet = alphabet
		self.radix = len(self.alphabet)
		self.preimage_modulus = pow(self.radix, self.preimage_length)
		self.num_chains = num_chains
		self.chain_length = chain_length

	def generate(self):
		assert len(self.table) == 0, 'Can only generate on a fresh rainbow table'
		for _ in range(self.num_chains):
			if _ % 100 == 0:
				print(f"generated {_} chains")
			base = string_helper.random_string(self.preimage_length, self.alphabet)
			end_of_chain = self._end_of_chain(self.chain(base=base))
			if end_of_chain is not None and end_of_chain not in self.table:
				self.table[end_of_chain] = base
		print(f"rainbow table contains {len(self.table)} chains")
		print(f"generated {len(self.unique_preimages)} unique preimages")

	def search(self, goal_hash):
		for start_step in range(self.num_chains):
			for pre, _ in self.chain(base_hash=goal_hash, start_step=start_step):
				if pre in self.table:
					found_preimage = self._search_chain(self.chain(base=self.table[pre]), goal_hash)
					if found_preimage is not None:
						return found_preimage
		return None

	def chain(self, base=None, base_hash=None, start_step=0):
		assert base is not None or base_hash is not None, 'No base was provided'
		assert not base or not base_hash, 'Cannot provide two bases'
		if start_step <= self.chain_length + 1:
			if base_hash:
				cur_pre, cur_hash = None, base_hash
			else:
				cur_pre, cur_hash = base, hashlib.md5(base.encode()).hexdigest()
			yield cur_pre, cur_hash
			self.unique_preimages.add(cur_pre)
			for chain_step in range(start_step, self.chain_length):
				cur_pre = self.reduction(cur_hash, chain_step)
				cur_hash = hashlib.md5(cur_pre.encode()).hexdigest()
				yield cur_pre, cur_hash
				self.unique_preimages.add(cur_pre)

	def _end_of_chain(self, chain):
		last_pre = None
		for last_pre, _ in chain:
			pass
		return last_pre

	def _search_chain(self, chain, goal_hash):
		for p, h in chain:
			if h == goal_hash:
				return p
		return None

	def reduction(self, input_hash, chain_step):
		wrapped_hash = (int(input_hash, 16) + chain_step) % self.preimage_modulus
		induced_string = ""
		while len(induced_string) < self.preimage_length:
			alphabet_index, wrapped_hash = wrapped_hash % self.radix, wrapped_hash // self.radix
			induced_string += self.alphabet[alphabet_index]
		return induced_string

	# File I/O

	def write_to_file(self, filename):
		file = open(filename, "wb")
		json_table = json.dumps(self.table, separators=(',', ':'))
		json_table_compressed = zlib.compress(json_table.encode())
		file.write(json_table_compressed)
		file.close()

	def read_from_file(self, filename):
		assert len(self.table) == 0, 'Can only read file for a fresh rainbow table'
		file = open(filename, "rb")
		json_table = zlib.decompress(file.read()).decode()
		self.table = json.loads(json_table)