
# Least Significant Bit Steganography

### Sam Faulkner

1. Instructions on how to run your code for my graders
	The code has two ways it can be run:
    REQUIRES pygame. MUST run `$pip install pygame` or `$pip3 install pygame` or DOWNLOAD [here](https://www.pygame.org/download.shtml)

		`$ python LeastSignificantBit.py -n \<number of bits to change\> \<message file\> \<image\> \<output filename\>`
		`$ python LeastSignificantBit.py -n \<number of bits to look at\> \<image\> \<output filename\>`

    The first corresponds to encoding a given file in an image, outputting an image to the given filename.
    The second corresponds to decoding a message from a given image, and outputting the retrieved message to the filename.
    Be sure to use python3 if applicable!

2. The actual code
	See LeastSignificantBit.py!

3. A project report with the following:
  1. Group Information (name, group members, etc)
		Sam Faulkner srf767
  2. An introduction to your overall project
		This is a CLI tool that implements the Least Significant Bit algorithm. It manipulates the least significant bits in the color channels of each pixel
  3. A brief explanation of the algorithm you selected to implement
    The Least Significant bit algorithm works by encoding a message into the least significant bits of an image. If the number of bits changed is
    small enough, the difference won't be noticeable to the human eye (although very noticeable through the use of statistical analysis).
  4. A quick example of how the algorithm functions (by example) nothing big or extensive but enough to show the working of the algorithm
  	Assuming I have an 'image.png' and a 'message.txt' in my current working directory, run
  	`$ python LeastSignificantBit.py -n \<2\> \<message.txt\> \<image.png\> \<output.png\>`

  	You'll notice the output.png won't be noticeable different from the given 'image.png'
  	To retrieve the message, run
  	`$ python LeastSignificantBit.py -n \<2\> \<output.png\> \<output.txt\>`

  	'output.txt' will be identical to message.txt
  5. A flowchart, bulletpoint list, or something that outlines the major points of your program and algorithm
    * Accepts text files as input
    * Allows specifying how many bits in each color channel to manipulate
    * Runs in python
