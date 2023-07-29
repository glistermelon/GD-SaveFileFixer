# -*- coding: utf-8 -*-
# Import needed Python default libraries
import base64, datetime, os, shutil, struct, sys, traceback, gzip
# Try to import the optionnal PyCryptoDome library (you need to install it)
try:
	from Crypto.Cipher import AES
except ImportError:
	print("WARNING: PyCryptoDome hasn't been found, MacOS GD Savefile fix won't work !")
	AES = None

# Set Python module variables
__version__ = "1.0.0"
__author__ = "HGStyle & WEGFan"

# Define some functions
def clear_screen():
	os.system('clear' if os.name != "nt" else "cls")

def fix_file(file, decode_type):
	# WARNING: This function does not create any backup !
	# Read the data
	data = open(file, 'rb').read()
	if decode_type.lower().strip() == in ["windows", "android", "linux"]:
		# Fix the Savefile with GD Windows/Android Savefile encryption/encoding
		try:
			# Decrypt/decode the Savefile
			data = bytes(c ^ 11 for c in memoryview(data)[:len(data) & -4])
			data = base64.urlsafe_b64decode(data)
			data = gzip.decompress(data)
			# Fix the Savefile (no one knows why this works but it does)
			data = data.replace(b'><', b'> <')
			# Encrypt/encode the Savefile back
			data = gzip.compress(data)
			data = base64.urlsafe_b64encode(data)
			data = bytes(c ^ 11 for c in data)
		except:
			# Some error occured
			return False
	# todo: ask if ios gd uses macos encryption because im unsure
	elif decode_type.lower().strip() in ["macos", 'ios']:
		# Fix the Savefile with GD MacOS Savefile encryption/encoding
		if not AES:
			print('Please install PyCryptoDome before using that !')
			print('Read the README on the GitHub repo.')
			return False
		try:
			# Decrypt/decode the Savefile
			cipher = AES.new(b'ipu9TUv54yv]isFMh5@;t.5w34E2Ry@{', AES.MODE_ECB)
			data = cipher.decrypt(data)
			if data[-1] < 16:
				data = data[:-last]
			# Fix the Savefile (no one knows why this works but it does)
			data = data.replace(b'><', b'> <')
			# Encrypt/encode the Savefile back
			if len(data) % 16:
				data += (16 - len_r).to_bytes(1, "little") * (16 - len_r)
			cipher = AES.new(b'ipu9TUv54yv]isFMh5@;t.5w34E2Ry@{', AES.MODE_ECB)
			data = cipher.encrypt(data)
		except:
			# Some error occured
			return False
	# Save the file
	with open(file, 'wb') as f:
		f.write(data)

def ask_for_choice(question, responses):
	# Function to ask a question and get a valid response from a set of responses
	print(question)
	resps = {}
	x = 1
	for response in responses:
		print(f"{x}. {response}")
		resps[str(x)] = response
		x += 1
	attempts = 0
	while True:
		if attempts != 0:
			print('Invalid response, please choose the number of the option.')
			print(question)
			for key in resps.keys():
				print(f"{key}. {resps[key]}")
		choice = input('Write your choice -> ')
		if choice.lower().strip() in resps.keys():
			return resps[choice.lower().strip()]
		else:
			attempts += 1
			clear_screen()

def ask_for_path(question):
	# Function to ask a question and get a valid filepath
	print(question)
	attempts = 0
	while True:
		if attempts != 0:
			print('Invalid filepath, please choose the number of the option.')
			print(question)
		choice = input('Write the filepath -> ')
		if os.path.exists(choice):
			return choice
		else:
			attempts += 1
			clear_screen()

def backup_file(file, dir):
	# Simple function to create a backup
	shutil.copyfile(file, os.path.join(dir, file))
	return True

def create_backup_dir(path):
	# Simple function to create backup directory
	dirname = "backup_" + datetime.datetime.now().strftime('Y%Y-M%m-D%d_h%H-m%M-s%S')
	os.mkdir(os.path.join(path, dirname))
	return os.path.join(path, dirname)

if __name__ == "__main__":
	# Prints informations to the user
	print("""Hello user ! (read this if its your first use)
It seems like you wanna fix your Geometry Dash Savefiles !
This programm was entirelly rewritten by HGStyle from
the WEGFans's tool Geometry-Dash-Savefile-Fix GitHub repo.
Thanks to him, I could never knew how to fix GD Savefiles
without his GitHub repository !
For more informations (like how to install PyCryptoDome),
go to: https://github.com/HGStyle/GD-SaveFileFixer/
Before running that programm, check for any warnings
before that text. (nothing before that text = you can run,
else please read the README file of my GitHub repo !)
""")
	input('Pres ENTER to start this programm !')
