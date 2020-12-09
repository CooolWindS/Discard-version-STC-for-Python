import sys
import os
from PIL import Image
from openpyxl import Workbook, load_workbook
from lib_py import parameter as p

def read_img_embed(cover_image_path, channel, log):
	
	im=Image.open(cover_image_path)
	if(p.log_detail):
		log.write("Cover image: " + cover_image_path + '\n')
	
	# Gray_level img
	if im.mode in ['L']:
	
		if channel != 'L':
			print('Channel chose to embed is:', channel)
			print('But img is in L mode. Please check channel code in parameter.')
			sys.exit(0)
		
		image_split = {'L':im}
		if(p.log_detail):
			log.write("Image mode: " + str(im.mode) + '\n')
			log.write("Channel chose to embed: "+ str(channel) + " channel" + '\n')
	
	# Color img
	elif im.mode in ['RGB', 'RGBA', 'RGBX']:
		
		if(p.log_detail):
			log.write("Image mode: " + str(im.mode) + '\n')
			log.write("Channel chose to embed: "+ str(channel) + " channel" + '\n')
		
		r, g, b = im.split()
		image_split = {'R':r, 'G':g, 'B':b}
		
		im = im.getchannel(channel)
	
	else:
		print(cover_image_path)
		print("Image mode are not yet supported.")
		print("Image mode:", im.mode)
		sys.exit(0)
		
	return (im, image_split)
	
	
	
def save_img_embed(stego_image_dir, cover_image, im, width, height, stego, channel, image_split):
	
	# Save output message
	idx=0
	for j in range(height):
		for i in range(width):
			im.putpixel((i, j), stego[idx])
			idx += 1
			
	s = "_stego_" + channel + "."
	stego_image = (cover_image.replace(".", s))
	
	stego_image_dir_channel = stego_image_dir + channel + '/'
	
	if not os.path.isdir(stego_image_dir_channel):
		os.mkdir(stego_image_dir_channel)
		
	stego_image_path = os.path.join(stego_image_dir_channel, stego_image)
			
	if(channel == 'L'):
		im.save(output_img_path)
		return output_img_path
	
	elif(channel == 'R'):
		out = Image.merge("RGB", (im, image_split["G"], image_split["B"]))
	
	elif(channel == 'G'):
		out = Image.merge("RGB", (image_split["R"], im, image_split["B"]))
		
	elif(channel == 'B'):
		out = Image.merge("RGB", (image_split["R"], image_split["G"], im))
	
	else:
		print(stego_image_path)
		print("Error channel to save.")
		print("channel chose:", channel)
		sys.exit(0)
		return
	
	out.save(stego_image_path)
	return stego_image_path


def read_img_extract(stego_image_path, log):
	
	im=Image.open(stego_image_path)
	
	if(p.log_detail):
		log.write("Stego image: " + stego_image_path + '\n')
	
	# Gray_level img
	if im.mode in ['L']:
		
		image_split = {'L':im}
		channel_choose = 'L'
		
		if(p.log_detail):
			log.write("Image mode: " + str(im.mode) + '\n')
			log.write("Channel chose to extract: "+ str(channel_choose) + " channel" + '\n')
	
	# Color img
	elif im.mode in ['RGB', 'RGBA', 'RGBX']:
		
		channel_choose = stego_image_path[-5]
		
		if(p.log_detail):
			log.write("Image mode: " + str(im.mode) + '\n')
			log.write("Channel chose to extract: "+ str(channel_choose) + " channel" + '\n')
		
		im = im.getchannel(channel_choose)
		
	else:
		print(stego_image_path)
		print("Image mode are not yet supported.")
		print("Image mode:", im.mode)
		sys.exit(0)
		
	return (im, channel_choose)
		
		
		
		
	
	