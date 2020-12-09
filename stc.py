import sys
import os
import math
import random
import struct
import hashlib
import cv2 
import numpy as np
from PIL import Image
from scipy import signal
from ctypes import *
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
from lib_py import read_write_file as rwf
from lib_py import parameter as p
import ctypes
import ctypes.util

def HILL(input_image):
	H = np.array(
	   [[-1,  2, -1],
		[ 2, -4,  2],
		[-1,  2, -1]])
	L1 = np.ones((3, 3)).astype('float32')/(3**2)
	L2 = np.ones((15, 15)).astype('float32')/(15**2)
	
	# Mod imageio.imread to cv2.imread ????????????
	#I = imageio.imread(input_image)
	
	# Maybe need split RGB channel instead of convert to grayscale
	I = cv2.imread(input_image,0)
	
	costs = signal.convolve2d(I, H, mode='same')  
	costs = abs(costs)
	costs = signal.convolve2d(costs, L1, mode='same')  
	costs = 1/costs
	costs = signal.convolve2d(costs, L2, mode='same')  
	costs[costs == np.inf] = 1
	
	return costs

def prepare_message(filename, password):

	f = open(filename, 'r')
	content_data = f.read().encode('utf-8')

	# Prepare a header with basic data about the message
	# Return a bytes object containing the values v1 packed according to the format string format.
	# "B": unsigned char format
	# 1: ???
	content_ver=struct.pack("B", 1) # version 1
	content_len=struct.pack("!I", len(content_data))
	content=content_ver+content_len+content_data

	# encrypt
	enc = encrypt(content, password)

	array=[]
	for b in enc:
		for i in range(8):
			array.append((b >> i) & 1)
	return array


# {{{ encrypt()
def encrypt(plain_text, password):

	salt = get_random_bytes(AES.block_size)

	# use the Scrypt KDF to get a private key from the password
	private_key = hashlib.scrypt(
		password.encode(), salt=salt, n=2**14, r=8, p=1, dklen=32)

	cipher = AES.new(private_key, AES.MODE_CBC)
	cipher_text = cipher.encrypt(pad(plain_text, AES.block_size))
	enc = salt+cipher.iv+cipher_text

	return enc
# }}}

# {{{ decrypt()
def decrypt(cipher_text, password):
	
	salt = cipher_text[:AES.block_size]
	iv = cipher_text[AES.block_size:AES.block_size*2]
	cipher_text = cipher_text[AES.block_size*2:]

	# Fix padding
	mxlen = len(cipher_text)-(len(cipher_text)%AES.block_size)
	cipher_text = cipher_text[:mxlen]

	private_key = hashlib.scrypt(
		password.encode(), salt=salt, n=2**14, r=8, p=1, dklen=32)

	cipher = AES.new(private_key, AES.MODE_CBC, iv=iv)
	decrypted = cipher.decrypt(cipher_text)
	#decrypted = unpad(decrypted, AES.block_size)

	return decrypted
# }}}


def embed(cover_image_path, stego_image_dir, cover_image,  msg_file_path, password, channel, log, payload=p.payload):

	me = os.path.abspath(os.path.dirname(__file__))
	lib = cdll.LoadLibrary(os.path.join(me, "lib", "stc.so"))
	
	cost_matrix = HILL(cover_image_path)
	
	# Prepare cover image
	im, image_split = rwf.read_img_embed(cover_image_path, channel, log)
	
	width, height = im.size
	
	if(p.log_detail):
		log.write("Image WxH: "+ str(width) + "x" + str(height) +'\n')
		
	I = im.load()
	cover = (c_int*(width*height))()
	idx=0
	for j in range(height):
		for i in range(width):
			cover[idx] = I[i, j]
			idx += 1


	# Prepare costs
	INF = 2**31-1
	costs = (c_float*(width*height*3))()
	idx=0
	for j in range(height):
		for i in range(width):
			if cover[idx]==0:
				costs[3*idx+0] = INF
				costs[3*idx+1] = 0
				costs[3*idx+2] = cost_matrix[i, j]
			elif cover[idx]==255:
				costs[3*idx+0] = cost_matrix[i, j]
				costs[3*idx+1] = 0 
				costs[3*idx+2] = INF
			else:
				costs[3*idx+0] = cost_matrix[i, j]
				costs[3*idx+1] = 0
				costs[3*idx+2] = cost_matrix[i, j]
			idx += 1

	# Prepare message
	msg_bits = prepare_message(msg_file_path, password)
	if len(msg_bits)>width*height*payload:
		print("Message too long")
		print('msg_bits: ' + str(len(msg_bits)))
		print('MAX payload bits: ' + str(width*height*payload))
		sys.exit(0)
	
	log.write('msg_bits: ' + str(len(msg_bits)) + '\n')
	log.write('MAX payload bits: ' + str(width*height*payload) + '\n')
	
	m = int(width*height*payload)
	message = (c_ubyte*m)()
	for i in range(m):
		if i<len(msg_bits):
			message[i] = msg_bits[i]
		else:
			message[i] = 0
			
	# Hide message
	stego = (c_int*(width*height))()
	
	# In stc_interface.cpp 
	a = lib.stc_hide(width*height, cover, costs, m, message, stego)
	
	# Save stego image
	stego_image_path = rwf.save_img_embed(stego_image_dir, cover_image, im, width, height, stego, channel, image_split)
	
	im.close()
	return stego_image_path


def extract(stego_image_path, password, output_message_file, log, payload=p.payload):

	me = os.path.abspath(os.path.dirname(__file__))
	lib = cdll.LoadLibrary(os.path.join(me, "lib", "stc.so"))
	
	# Prepare stego image
	im, channel_choose = rwf.read_img_extract(stego_image_path, log)
	
	width, height = im.size
	
	I = im.load()
	stego = (c_int*(width*height))()
	idx=0
	for j in range(height):
		for i in range(width):
			stego[idx] = I[i, j]
			idx += 1

	# Extract the message
	n = width*height;
	m = int(n*payload)
	extracted_message = (c_ubyte*m)()
	s = lib.stc_unhide(n, stego, m, extracted_message)

	# Save the message
	enc = bytearray()
	idx=0
	bitidx=0
	bitval=0
	for b in extracted_message:
		if bitidx==8:
			enc.append(bitval)
			bitidx=0
			bitval=0
		bitval |= b<<bitidx
		bitidx+=1
	if bitidx==8:
		enc.append(bitval)

	# decrypt
	cleartext = decrypt(enc, password)
 
	# Extract the header and the message
	content_ver=struct.unpack_from("B", cleartext, 0)
	content_len=struct.unpack_from("!I", cleartext, 1)
	content=cleartext[5:content_len[0]+5]

	s = content.decode(errors='ignore')
	
	f = open(output_message_file, 'w')
	f.write(s)
	f.close()
	
	log.write(output_message_file)



