import sys
import os
import numpy as np
import random
import string
import warnings
from scipy import signal
import stc
from lib_py import parameter as p
from lib_py import read_write_file as rwf


def message(index, now_dir, cover_image_name, channel, log):
	
	# Default
	if(p.message_choose == 0):
		return p.message_default
	
	# Exist message
	elif(p.message_choose == 1):
		return p.message_default
	
	# Random generate message len = 100~200
	else:
		s = ''
		
		# message character numbers
		# 12000 may be safe with payload=0.4
		#l = random.randint(120, 200)
		l = 12000
		for i in range(l):
			s = s + random.choice(string.ascii_letters)
		s = s + '\n'
		
		path = os.path.join(now_dir, p.message_embed) + channel + '/'
		
		if not os.path.isdir(path):
			os.mkdir(path)
		
		path = path + cover_image_name + '.txt'
		log.write('Message: ' + str(path)  + '\n')
		f = open(path, 'w')
		f.write(s)
		f.close()
		return path
		
def channel_choose():
	
	if(p.channel_code < 0 or p.channel_code > 4):
		print('Error channel code, please check channel code in parameter.')
		sys.exit(0)
	elif(p.channel_code > 0 and p.channel_code < 4):
		return [p.channel[p.channel_code]]
	else:
		return p.channel[1:]

def main():
	
	#####
	warnings.filterwarnings('ignore')
	#####
	
	log = open('files/log_embed', 'w')
	
	now_dir = os.getcwd()
	
	# ex. /home/.../pySTC/files/cover/
	cover_image_dir = os.path.join(now_dir, p.cover)
	
	# ex. /home/.../pySTC/files/stego/
	stego_image_dir = os.path.join(now_dir, p.stego)
	
	# All cover image in cover_image_dir
	# ex. ['color_001.bmp', 'color_002.bmp', ...]
	cover_image_filelist = os.listdir(cover_image_dir)
	cover_image_filelist.sort()
	
	#data_size = len(cover_image_filelist)
	data_size = 500
	print(str(data_size) + " images to embed.")
	if(data_size > 1000):
		report = 200
	elif(data_size < 10):
		report = 1
	else:
		report = int(data_size/10)
		
	channel_list = channel_choose()
	print("Each image will embed in channel", str(channel_list))
	print('Report completed every ' + str(report) +' pictures' + '\nStart...')
	print("Embedding...")
	
	for i in range(data_size):
		
		# Cover image 
		# ex. color_001.bmp
		cover_image = cover_image_filelist[i]

		# Cover image path
		# ex. /home/.../pySTC/files/cover/color_001.bmp
		cover_image_path = os.path.join(cover_image_dir, cover_image)

		# Cover image name and datatype
		# color_001 and .bmp
		cover_image_name = os.path.splitext(cover_image)[0]
		cover_image_datatype = os.path.splitext(cover_image)[1]
		
		for channel in channel_list:
			
			# Message to embed
			input_message_file = message(i, now_dir, cover_image_name, channel, log)

			stego_image_path = stc.embed(cover_image_path, stego_image_dir, cover_image, input_message_file, p.password, channel, log)
			
			log.write(os.path.split(stego_image_path)[1] + ' done.' + '\n\n\n')
		
		if((i+1)%(report)==0):
			print(str(i+1) + " images done.")

	
	log.close()
	print("Done\n\n")


if __name__ == "__main__":
	main()

