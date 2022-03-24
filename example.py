from rainbow import rainbow
import string
import hashlib

ALPHABET = list(string.ascii_lowercase)

preimage_length = 5
num_chains = 8000
chain_length = 2000

# Hash and the expected preimage of the hash
test_hash = "1f3870be274f6c49b3e31a0c6728957f" # MD5('apple')

# Make a fresh rainbow table
rainbow_table = rainbow.RainbowTable(preimage_length, ALPHABET, num_chains, chain_length)

# Generate the rainbow table
rainbow_table.generate()

# Write rainbow table to 'rainbow__.rbt'
rainbow_table.write_to_file(f"rainbow{preimage_length}.rbt")

# # Read rainbow table from 'rainbow__.rbt' (can be used if there is an already saved rainbow table file)
# rainbow_table.read_from_file(f"rainbow{preimage_length}.rbt")

# Search for the preimage of the hash
preimage = rainbow_table.search(test_hash)

# Test the preimage is correctly found
assert preimage is not None, 'Did not find any preimage for this hash in the table'
assert test_hash == hashlib.md5(preimage.encode()).hexdigest(), 'Hash of preimage does not match expected'

# Print out the preimage
print(f"The preimage of {test_hash} is {preimage}")