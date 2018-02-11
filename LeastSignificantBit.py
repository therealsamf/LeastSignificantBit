#!/usr/bin/python3

"""Python program to implement least significant bit steganography"""

import pygame, sys, getopt
from pygame.locals import *
from typing import Dict, List, IO
from io import FileIO
import os.path

def main(args: List) -> None:
	"""
	Main entry point to the program

	Arguments:
	args -- arugments passed in from command line
	"""

	if len(args) < 2:
		print_usage()
		return

	try:
		opts, args = getopt.getopt(args, 'n:')
		opts = dict(opts)

		if len(args) == 3:
			#Retrieve the necessary arguments from the commandline
			message_file = args[0]
			input_image = args[1]
			output_filename = args[2]

			run_steganography(message_file, input_image, output_filename, opts)
		elif len(args) == 2:
			input_image = args[0]
			output_filename = args[1]

			decrypt_image(input_image, output_filename, opts)

	except getopt.GetoptError:
		print_usage()

def print_usage():
	"""
	Prints the usage of the tool to the console
	"""
	print_version()
	print()
	print('Usage: ')
	print('\tpython[3] LeastSignificantBit.py [-n 2] [options] <input_message_file> <input_image> <output_filename>')
	print('\tpython[3] LeastSignificantBit.py [-n 2] [options] <input_image> <output_filename>')
	print('Options: ')
	print('\t-n\tThe number of bits to modify in each pixel\'s channel')



def print_version():
	"""
	Prints the name and version of the program
	"""
	try:
		version_file = open('version.txt', 'r')
		version = version_file.readline();
		version_file.close()


		print('Least Significant Bit Steganography')
		print('By Sam Faulkner')
		print("version: " + str(version))
	except:
		pass

def decrypt_image(input_image_filename: str, output_filename: str, opts: Dict) -> None:
	"""
	Function that calls and/or performs the necessary functions to retrieve a message from 
	an image

	Arguments:
	input_image_filename -- the filepath of the image that has a secret message
	output_filename      -- the filepath of where they want the image saved
	"""

	image = retrieve_image(input_image_filename)

	output_file = get_output_file(output_filename)

	if not image or not output_file:
		return

	decrypt_message(image, output_file, int(opts['-n']))

def decrypt_message(image: pygame.Surface, output_file: IO[str], num_bits: int) -> None:
	"""
	Function that looks into the image and retrieves the hidden message

	Arguments:
	image       -- the pygame.Surface object holding the data
	output_file -- the writeable stream that we'll write the data to
	"""

	write_buffer = bytes()
	image_buffer = image.get_view('1')
	image_bytes = image_buffer.raw
	current_byte_index = 0

	current_bits = 0
	bit_mask = construct_mask(num_bits)

	done = False

	while not done and current_byte_index < len(image_bytes):
		for i in range(8):
			# because each value will only be a single byte, it doesn't matter what the byte order is
			retrieved_value = image_bytes[current_byte_index] & bit_mask
			current_bits = current_bits | (retrieved_value << (i * num_bits))

			current_byte_index += 1

		for i in range(num_bits):
			current_value = (current_bits & (0xFF << (i * 8))) >> (i * 8)
			
			current_byte = bytes([current_value])

			# Check for EOT character
			if (current_byte == b'\xFF'):
				done = True
				break

			write_buffer += current_byte

		current_bits = 0

		if output_file.write(write_buffer) != len(write_buffer):
			raise IOError('Unable to write the message to file')
		else:
			output_file.flush()
			write_buffer = bytes()


	output_file.flush()
	output_file.close()




def get_output_file(filepath: str) -> IO[str]:
	"""
	Function that returns a writable file stream from the given
	filename

	Arugments:
	filepath -- the filepath of where the output should go
	"""
	file = None

	try:
		file = FileIO(filepath, 'w')
	except (IOError, OSError) as e:
		print(e)

	return file

def run_steganography(message_filename: str, input_image_filename: str, output_filename: str, opts: Dict) -> None:
	"""
	Function that calls and/or performs the main steganographic function of the program

	Arguments:
	message_filename     -- filename of the user's desired hidden message
	input_image_filename -- filename of the user's png image they want to embed their message in
	output_filename      -- desired file the user wants to save their result to
	opts                 -- dictionary containing desired options
	"""

	message_file = retrieve_message_file(message_filename)
	image = retrieve_image(input_image_filename)


	# At this point error messages have already printed out to the user
	if not image or not message_file:
		return
	if not verify_filename(output_filename):
		return

	try:
		embed_image(message_file, image, int(opts['-n']))
	except Exception as e:
		print(e)

	pygame.image.save(image, output_filename)
	message_file.close()

def verify_filename(filename: str) -> bool:
	"""
	Verifies that the given filename is appropriate for
	saving a PNG image to

	Arguments:
	filename -- the filepath that requires verification
	"""

	root, ext = os.path.splitext(filename)

	# The only verification right now is checking for file extension,
	# as pygame relies on it being the correct kind
	if ext != '.png':
		return False

	return True

def retrieve_message_file(message_filename: str) -> IO[str]:
	"""
	Retrieves the file the user wants to use as his/her message

	Arguments:
	message_filename -- The filepath of where the message file is located
	"""

	message_file = None

	try:
		message_file = FileIO(message_filename)
	except (IOError, OSError) as e:
		print(e)

	return message_file

def retrieve_image(input_image_filename: str) -> pygame.Surface:
	"""
	Retrieves the file the user wants to use as their image, then
	uses pygame to load it into a usable data structure (pygame.Surface)

	Arguments:
	input_image_filename -- the filepath of the image file is located
	"""
	image = None

	try:
		root, ext = os.path.splitext(input_image_filename)
		if ext != '.png':
			raise IOError('\'<input_image>\' is not a .png file')

		# This checks if pygame can load extended image formats, which is necessary for PNGs
		if not pygame.image.get_extended():
			raise Error('pygame is not able to load .png images')

		image = pygame.image.load(input_image_filename)
	except (IOError, OSError) as e:
		print('invalid \'<input_image>\' argument')
		print(e)
	except Exception as e: 
		print(e)

	return image


def construct_mask(length: int) -> int:
	"""
	Constructs a variable length bit mask

	Arguments:
	length -- the length of the desired mask
	"""
	mask = '1' * length
	return int(mask, 2)

def construct_inverted_mask(length: int) -> int:
	"""
	Constructs a variable length bit mask with the
	intent that the mask can "mask off" certain values
	instead of retrieving them

	Arguments:
	length -- the length of the desired mask
	"""

	mask = '1' * (8 - length)
	mask += '0' * length
	return int(mask, 2)


def embed_image(message: IO[str], image: pygame.Surface, num_bits_modify: int) -> None:
	"""
	Mutates the given image to embed the given message within it

	Arguments:
	message -- the file object containing the wanted message
	image -- the pygame Surface with pixel data
	num_bits_modify -- the number of bits to modify in each pixel value
	"""

	if (num_bits_modify > 8):
		raise Error('No more than 8 bits per pixel\'s channel')
	elif (num_bits_modify <= 0):
		raise Error('Must modify at least 1 bit per pixel channel')

	image.lock()

	image_buffer = image.get_view('1')
	image_bytes = image_buffer.raw
	image_bytes_length = len(image_bytes)
	current_byte_index = 0

	stride_size = 8 * num_bits_modify
	bit_mask = construct_mask(num_bits_modify)
	inverted_mask = construct_inverted_mask(num_bits_modify)

	current_message_stream = message.read(stride_size)

	while len(current_message_stream) > 0:

		if len(current_message_stream) < stride_size:
			current_message_stream += b'\xFF'

		# Grab the value from the message
		bits = int.from_bytes(current_message_stream[::-1], byteorder='big')
		i = 0
		while (i * num_bits_modify) < (len(current_message_stream) * 8) + ((len(current_message_stream) * 8) % num_bits_modify):
			value_to_embed = (bits & (bit_mask << (num_bits_modify * i))) >> (num_bits_modify * i)
			current_image_byte = image_bytes[current_byte_index]
			current_image_byte = (current_image_byte & inverted_mask) | value_to_embed
			image_buffer.write(bytes([current_image_byte]), current_byte_index)

			i += 1
			current_byte_index += 1
			if current_byte_index >= len(image_bytes):
				raise Exception('Message too big for image')


		current_message_stream = message.read(stride_size)



	image.unlock()


if __name__ == '__main__':
	main(sys.argv[1:])

