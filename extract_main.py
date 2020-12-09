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


def main():
	
	#####
	warnings.filterwarnings('ignore')
	#####
	
	log = open('files/log_extract', 'w')
	
	now_dir = os.getcwd()
	
	# ex. /home/.../pySTC/files/stego/
	stego_image_dir = os.path.join(now_dir, p.stego)
	
	# All channel folder in stego_image_dir
	# ex. ['R', 'G', ...]
	stego_image_folder = os.listdir(stego_image_dir)
	stego_image_folder.sort()
	print(stego_image_folder)
	
	for j in range(len(stego_image_folder)):
		
		# Stego image path in channel folder
		# ex. /home/.../pySTC/files/stego/R/
		stego_image_folder_dir = os.path.join(stego_image_dir, stego_image_folder[j])
		
		# All stego image in stego_image_folder_dir
		# ex. ['color_001.bmp', 'color_002.bmp', ...]
		stego_image_filelist = os.listdir(stego_image_folder_dir)
		stego_image_filelist.sort()

		data_size = len(stego_image_filelist)
		print(str(data_size) + " images to extract in", os.path.join(p.stego, stego_image_folder[j]))
		if(data_size < 20):
			report = data_size
		else:
			report = int(data_size/20)
		print('Report completed every ' + str(report) +' pictures' + '\nStart...')
		print("Extracting...")
	
	
		for i in range(data_size):
			
			# Stego image 
			# ex. color_001.bmp
			stego_image = stego_image_filelist[i]

			# Stego image path
			# ex. /home/.../pySTC/files/stego/color_001.bmp
			stego_image_path = os.path.join(stego_image_folder_dir, stego_image)

			# Stego image name and datatype
			# color_001 and .bmp
			stego_image_name = os.path.splitext(stego_image)[0]
			stego_image_datatype = os.path.splitext(stego_image)[1]
			
			#
			output_message_folder_dir = os.path.join(now_dir, p.message_extract, stego_image_folder[j])
			if not os.path.isdir(output_message_folder_dir):
				os.mkdir(output_message_folder_dir)
			output_message_file = os.path.join(output_message_folder_dir, (stego_image_name + '.txt'))
			
			stc.extract(stego_image_path, p.password, output_message_file, log)
			
			log.write(os.path.split(stego_image_path)[1] + '\ndone.' + '\n\n\n')

			if((i+1)%(report)==0):
				print(str(i+1) + " images extract done.")
		print("Done\n\n")

	
	
	log.close()


if __name__ == "__main__":
	main()

