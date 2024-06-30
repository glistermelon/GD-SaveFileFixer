#!/usr/bin/env python3
# -*- coding: utf-8 -*-
### DEVELOPER WARNING: THE SYNTAX USED IN THIS PROGRAM MOSTLY DOES NOT RESPECT THE PEP 8 SYNTAX, YOUVE BEEN WARNED ###
# Imports the necessary libraries
import base64
import datetime  # Don't forget to write datetime.datetime, and not just datetime !
import os
import shutil
import sys
import gzip
import platform
import time
import urllib.request  # Oh my fckin no. Not this fckin library.
import subprocess

# Function to clear the screen
def clear_screen() -> None:
	if os.name == 'nt':
		os.system('cls')
	else:
		print('\033c', end='')

# Function to set the terminal title
def set_title(title: str) -> None:
	if os.name == 'nt':
		os.system(f'title {title}')
	else:
		print(f"\033]0;{title}\a", end='')

# Function to exit
def exit(code: int = 0) -> None:
	input('Press Enter to exit...')
	if not code:
		clear_screen()
	sys.exit(code)

# Function to remove KeyboardInterrupt errors on Ctrl+C on input() functions
_input = input
def input(*args, **kwargs):
	try:
		return _input(*args, **kwargs)
	except KeyboardInterrupt:
		if "Press Enter to exit..." in args or "Press Enter to exit..." in kwargs.values():
			sys.exit(1)
		exit(1)

IS_COMPILED = "__compiled__" in globals() # Difference between compiled and frozen:
IS_FROZEN = getattr(sys, 'frozen', False) # Frozing is putting Python and the script in an EXE like PyInstaller/Oxidizer

if not(IS_COMPILED) and not(IS_FROZEN):
	# Tries to import PIP (to install other modules)
	try:
		exec('i  m  p  o  r  t p  i  p'.replace('  ', ''))  # Little hack so Depency Walkers used by compilers won't detect this import
	except ImportError:
		print('PIP is not installed. It is needed to download some additionnal modules to add functionnalities.')
		choice = input('Would you like to download it ? (y/n) -> ')
		if "y" in choice.lower():
			print('Installing PIP... This may take some time depending on your internet connection.')
			# Download the right installer
			pip_ver_dl_url = f"https://bootstrap.pypa.io/pip/{sys.version_info.major}.{sys.version_info.minor}/get-pip.py"
			pip_dl_url = "https://bootstrap.pypa.io/pip/get-pip.py"
			if urllib.request.urlopen(pip_ver_dl_url).getcode() // 100 == 2:
				urllib.request.urlretrieve(pip_ver_dl_url, 'get-pip.py')
			else:
				urllib.request.urlretrieve(pip_dl_url, 'get-pip.py')
			# Run the installer
			subprocess.run([sys.executable, "get-pip.py"])
			# Check PIP's installation
			try:
				exec('i  m  p  o  r  t p  i  p'.replace('  ', ''))  # Little hack so Depency Walkers used by compilers won't detect this import
				print('PIP installation has been successfull.')
			except ImportError:
				print('PIP installation has failed.')
				pip = None
		else:
			pip = None
	# Tries to import PyCryptoDome (to en/decrypt Apple GD savefiles)
	try:
		exec('f  r  o  m C  r  y  p  t  o  .  C  i  p  h  e  r i  m  p  o  r  t A  E  S'.replace('  ', ''))  # Little hack so Depency Walkers used by compilers won't detect this import
	except ImportError:
		print('PyCryptoDome is not installed. It is needed for fixing MacOS/iOS savefiles.')
		if pip:
			choice = input('Would you like to download it ? (y/n) -> ')
			if "y" in choice.lower():
				print('Installing PyCryptoDome... This may take some time depending on your internet connection.')
				subprocess.run([sys.executable, "-m", "pip", "install", "pycryptodome"])
				try:
					exec('f  r  o  m C  r  y  p  t  o  .  C  i  p  h  e  r i  m  p  o  r  t A  E  S'.replace('  ', ''))  # Little hack so Depency Walkers used by compilers won't detect this import
					print('PyCryptoDome installation has been successfull.')
				except ImportError:
					print('PyCryptoDome installation has failed.')
					AES = None
		else:
			print('PIP is not installed. Installing PyCryptoDome is impossible.')
			AES = None
else:
	try:
		from Crypto.Cipher import AES # This one should stay as-is even when compilling a binary/using a depency walker
	except ImportError:
		print('MacOS/iOS savefiles will not be fixed since PyCryptoDome is not available.')
		AES = None

# Set some Python variables
__version__ = "2.0.0"
__author__ = "HGStyle"
__original_by__ = "WEGFan"
__program_name__ = "GD-SaveFile-Fixer"
__source__ = "https://github.com/HGStyle/GD-SaveFileFixer"
__license__ = "MIT License"

# Function to decode a savefile
def decode_savefile(data: bytes, decode_type: str) -> bytes:
	if decode_type.lower().strip() in ["windows", "android", "linux"]:
		# Decode the savefile using non-Apple GD encoding
		data = bytes(c ^ 11 for c in memoryview(data)[:len(data) & -4])
		data = base64.urlsafe_b64decode(data)
		data = gzip.decompress(data)
	elif decode_type.lower().strip() in ["macos", 'ios']:
		if not AES:
			print('PyCryptoDome is not installed. Savefile decoding cannot be done.')
			return b""
		# Decode the savefile using Apple GD encoding
		cipher = AES.new(b'ipu9TUv54yv]isFMh5@;t.5w34E2Ry@{', AES.MODE_ECB)
		data = cipher.decrypt(data)
		if data[-1] < 16:
			data = data[:-data[-1]]
	else:
		print(f'Cannot decode savefile due to unknown encoding type called {decode_type}.')
		return b""
	return data

# Function to encode a savefile
def encode_savefile(data: bytes, encode_type: str) -> bytes:
	if encode_type.lower().strip() in ["windows", "android", "linux"]:
		# Encode the savefile using non-Apple GD encoding
		data = gzip.compress(data)
		data = base64.urlsafe_b64encode(data)
		data = bytes(c ^ 11 for c in data)
	elif encode_type.lower().strip() in ["macos", 'ios']:
		if not AES:
			print('PyCryptoDome is not installed. Savefile encoding cannot be done.')
			return b""
		# Encode the savefile using Apple GD encoding
		len_r = len(data) % 16
		if len_r:
			data += (16 - len_r).to_bytes(1, "little") * (16 - len_r)
		cipher = AES.new(b'ipu9TUv54yv]isFMh5@;t.5w34E2Ry@{', AES.MODE_ECB)
		data = cipher.encrypt(data)
	else:
		print(f'Cannot encode savefile due to unknown encoding type called {encode_type}.')
	return data

# Function to guess which GD encoding is being used
def guess_gd_encoding(data: bytes) -> str:
	try:
		decode_savefile(data, "windows")
	except Exception:
		return "macos"
	try:
		decode_savefile(data, "macos")
	except Exception:
		if not AES:
			return "macos"
		return "windows"
	return "windows"

# Function to fix a savefile
def fix_savefile(filepath: str, decode_type: str = "") -> bool:
	try:
		# Read the data
		data = open(filepath, 'rb').read()
		# Guess the GD encoding if needed
		if not decode_type:
			decode_type = guess_gd_encoding(data)
		# Decode the savefile
		data = decode_savefile(data, decode_type)
		if not data:
			return False
		# Fix the savefile
		data = data.replace(b'><', b'> <')
		# Encode the savefile
		data = encode_savefile(data, decode_type)
		if not data:
			return False
		# Write the data
		with open(filepath, 'wb') as f:
			f.write(data)
		return True
	except Exception:
		return False

# Function to ask a question and get a valid response from a set of responses
def ask_for_choice(question: str, responses: list) -> int:
	print(question)
	choices = ""
	valid_keys = []
	x = 1
	for response in responses:
		choices += f"{x}. {response}\n"
		valid_keys.append(str(x))
		x += 1
	print(choices)
	isfirstatt = True
	while True:
		if not isfirstatt:
			print('Invalid response, please choose the number of the option.')
			print(question)
			print(choices)
		choice = input('Write your choice -> ')
		if choice.lower().strip() in valid_keys:
			return int(choice.lower().strip()) - 1
		else:
			if isfirstatt:
				isfirstatt = False
			clear_screen()

# Function to ask a question and get a valid filepath
def ask_for_path(question: str) -> None:
	print(question)
	isfirstatt = True
	while True:
		if not isfirstatt:
			print('Invalid file path, please choose the number of the option.')
			print(question)
		choice = input('Write the filepath -> ').strip()
		if not choice:
			return ""
		choice = choice.replace('/', os.sep).replace('\\', os.sep)
		if os.path.exists(choice):
			return choice
		else:
			if isfirstatt:
				isfirstatt = False
			clear_screen()

# Function to create a backup of a file
def backup_file(filepath: str, dirpath: str) -> bool:
	output = os.path.join(dirpath, os.path.basename(filepath))
	shutil.copyfile(filepath, output)
	return os.path.exists(output)

# Function to get a backup directory
def get_backup_dir(path: str) -> str:
	dirpath = os.path.join(path, "backup_"
		+ datetime.datetime.now().strftime('Y%Y-M%m-D%d-h%H')
		+ str(round(time.time()))
	)
	if not os.path.exists(dirpath):
		os.mkdir(dirpath)
	return dirpath

# Function to check is a file a Geometry Dash savefile (now its a better algorythm)
def is_valid_savefile(filepath: str) -> bool:
	if not os.path.basename(filepath).startswith('CC'):
		return False  # Not a GD savefile filename
	if os.path.basename(filepath).startswith('CCBetter'):
		return False  # GD mod savefile filename
	if not filepath.endswith('.dat'):
		return False
	encoded = open(filepath, 'rb').read()
	if not encoded:  # Empty savefile
		return False
	try:
		decoded = decode_savefile(encoded, "windows").decode()
	except Exception:  # Not using non-Apple GD encoding
		try:
			decoded = decode_savefile(encoded, "macos").decode()
		except Exception:  # Not using Apple GD encoding
			return False
	if not decoded:  # Decoding failed
		return False
	if "<" not in decoded or ">" not in decoded:
		return False  # Not XML data
	return True

# Function to search for savefiles
def search_savefiles(path: str) -> list:
	results = []
	for root, dirs, files in os.walk(path, onerror=lambda _: None):
		try:
			for f in files:
				p = os.path.join(root, f)
				if p.split(os.sep)[-2].startswith('backup'):
					continue
				if is_valid_savefile(p):
					results.append(p)
					print('Found savefile: ' + results[-1])
		except PermissionError:
			continue
	return results

# Function to get the system name
def get_system_name() -> str:
	systemname = platform.system().lower()
	platformname = platform.platform().lower()
	if systemname == "windows" or systemname == "cygwin":
		return "windows"
	elif systemname == "darwin" and "mac" in platformname:
		return "macos"
	elif systemname == "linux":
		return "linux"
	elif systemname == "android":
		return "android"
	elif systemname == "darwin" and "mac" not in platformname:
		return "ios"
	else:
		print(f'Cannot recognise the system name called {systemname} {platformname}.')
		return ""

# Function to get Geometry Dash's data folder depending on the system
def get_game_data_folder(system_name: str) -> str:
	if system_name == "windows":  # Stored in %localappdata%\GeometryDash
		return os.path.join(os.getenv('LOCALAPPDATA'), "GeometryDash")
	elif system_name == "macos":  # Most likely stored in ~/Library/Application Support/GeometryDash
		path = os.path.expanduser("~/Library/Application Support/GeometryDash")
		if os.path.exists(path):
			return path
	elif system_name in ["linux", "macos"]:  # TODO: Maybe split these in multiple functions for better understanding
		if os.path.exists(os.path.expanduser('~/.local/share/Steam/')) or os.path.exists(os.path.expanduser('~/.steam/')): # Steam
			# Get the Steam folder
			if os.path.exists(os.path.expanduser('~/.local/share/Steam/')):
				steam_path = "~/.local/share/Steam/"
			elif os.path.exists(os.path.expanduser('~/.steam/')):
				if os.path.exists(os.path.expanduser('~/.steam/steam/')):
					steam_path = "~/.steam/steam/"
				else:
					steam_path = "~/.steam/"
			# Get the Geometry Dash data folder
			path = os.path.expanduser(steam_path +
				"steamapps/compatdata/322170/pfx/drive_c/users/{}/Local Settings/Application Data/GeometryDash")
			# Gets the current Steam account username (needed to get the data folder path)
			try:
				steam_user_dir = os.path.expanduser(steam_path + "userdata")
				steam_user_dirs = [os.path.join(steam_user_dir, d) for d in os.listdir(steam_user_dir)
					if os.path.isdir(os.path.join(steam_user_dir, d))]
				steam_user_account = os.path.basename(max(steam_user_dirs, key=os.path.getmtime))
			except:
				steam_user_account = "steamuser"
			# Get the final data folder path
			if os.path.exists(path.format(steam_user_account)):
				return path.format(steam_user_account)
		if os.path.exists(os.path.expanduser('~/.local/share/lutris/')) or os.path.exists(os.path.expanduser('~/.lutris/')): # Lutris
			# Get the Lutris folder
			if os.path.exists(os.path.expanduser('~/.local/share/lutris/')):
				lutris_path = "~/.local/share/lutris/"
			elif os.path.exists(os.path.expanduser('~/.lutris/')):
				if os.path.exists(os.path.expanduser('~/.lutris/lutris/')):
					lutris_path = "~/.lutris/lutris/"
				else:
					lutris_path = "~/.lutris/"
			# Get the Geometry Dash data folder
			path = os.path.expanduser(lutris_path +
				"runners/wine/{}/prefix/drive_c/users/{}/Local Settings/Application Data/GeometryDash")
			# Get the session name from the home folder
			username = path.split(os.sep)[2]
			# Get Lutris's Wine version
			wine_vers = [i for i in os.listdir(os.path.expanduser(lutris_path + "runners/wine"))
				if os.path.exists(path.format(i, username))]
			# Get the final data folder path
			if wine_vers:
				return path.format(wine_vers[0], username)
		if os.path.exists(os.path.expanduser('~/.wine/')) or os.path.exists(os.path.expanduser('~/.local/share/applications/wine/')): # Wine
			# Get the Wine folder
			if os.path.exists(os.path.expanduser('~/.wine/')):
				if os.path.exists(os.path.expanduser('~/.wine/wine/')):
					wine_path = "~/.wine/wine/"
				else:
					wine_path = "~/.wine/"
			elif os.path.exists(os.path.expanduser('~/.local/share/applications/wine/')):
				wine_path = "~/.local/share/applications/wine/"
			# Get the Geometry Dash data folder
			path = os.path.expanduser(wine_path + "drive_c/users/{}/Local Settings/Application Data/GeometryDash")
			# Get the session name from the home folder
			username = path.split(os.sep)[2]
			# Get the final data folder path
			if os.path.exists(path.format(username)):
				return path.format(username)
		print('Cannot get the game data folder due to unknown way of launching Geometry Dash under this Linux system.')
	elif system_name == "android":  # Stored in /data/data/com.robtopx.geometryjump/
		return "/data/data/com.robtopx.geometryjump/"
	elif system_name == "ios":  # Stored in /var/mobile/Containers/Data/Application/com.robtop.geometryjump/
		return "/var/mobile/Containers/Data/Application/com.robtop.geometryjump/"
	else:
		print(f'Cannot get the game data folder due to unknown system called {system_name}.')
		return ""

# Function to check if the folder available and show tips to users about it being inaccessible, if its the case
def is_folder_accessible(path: str, system_name: str) -> bool:
	if not os.path.exists(path):
		print('The data folder cannot be found. Please use annother mode.')
		if system_name == "linux":
			print('Note that the programm can only get the data folder if you play Geometry Dash using Steam, Lutris or Wine.')
		return False
	if os.access(path, os.R_OK) and os.access(path, os.W_OK):
		return True  # Folder is accessible
	if system_name == "android":
		print('The data folder is inaccessible. Make sure you rooted your phone, or that you modified the app using App Cloner.')
	if system_name == "ios":
		print('The data folder is inaccessible. Make sure you jailbroken your phone.')
	return False

# Function to check whenether a filename is being known as a savefile
def is_savefile_name(path: str):
	return os.path.basename(path) in [
		"CCGameManager.dat",
		"CCGameManager.dat.bak",
		"CCGameManager2.dat",
		"CCGameManager2.dat.bak",
		"CCLoaderManager.dat",
		"CCLoaderManager.dat.bak",
		"CCLoaderManager2.dat",
		"CCLoaderManager2.dat.bak",
		"CCLocalLevels.dat",
		"CCLocalLevels.dat.bak",
		"CCLocalLevels2.dat",
		"CCLocalLevels2.dat.bak"
	]

# Function to search for the savefiles from their static names
def search_static_savefiles(path: str) -> list:
	results = []
	for root, dirs, files in os.walk(path, onerror=lambda _: None):
		try:
			for f in files:
				p = os.path.join(root, f)
				if p.split(os.sep)[-2].startswith('backup'):
					continue
				if is_savefile_name(p) and is_valid_savefile(p):
					results.append(p)
					print('Found savefile: ' + results[-1])
		except PermissionError:
			continue
	return results

# Function to get the data folder depending on the system
def get_data_folder(system_name: str) -> list:
	return {
		"windows": [
			os.getenv('LOCALAPPDATA')
		],
		"macos": [
			os.path.expanduser("~/Library/Application Support"),
			os.path.expanduser("~/.wine"),
			os.path.expanduser("~/.lutris"),
			os.path.expanduser("~/.steam"),
			os.path.expanduser('~/.local/share/lutris/'),
			os.path.expanduser('~/.local/share/applications/wine/'),
			os.path.expanduser('~/.local/share/Steam/')
		],
		"linux": [
			os.path.expanduser("~/.wine"),
			os.path.expanduser("~/.lutris"),
			os.path.expanduser("~/.steam"),
			os.path.expanduser('~/.local/share/lutris/'),
			os.path.expanduser('~/.local/share/applications/wine/'),
			os.path.expanduser('~/.local/share/Steam/')
		],
		"android": [
			"/data/data"
		],
		"ios": [
			"/var/mobile/Containers/Data/Application"
		]
	}[system_name]

# Run if not imported
if __name__ == "__main__":
	print("""-----------------------------------------------------------
Hello user! READ THIS IF ITS YOUR FIRST USE. (IMPORTANT)
-----------------------------------------------------------
THIS TOOL IS PROVIDEN WITHOUT ANY GUARANTEE OF SUCCESS,
OR MAY ACCIDENTALY BROKES YOUR SAVEFILES, that's why it
automatically creates a backup before modifying any file!
Rollback this backup manually if you need it.
(TODO: Add a function to rollback backups of savefiles)
-----------------------------------------------------------
NOTE IF YOU USE AN ANDROID EMULATOR (Bluestacks, Nox, etc):
You must run this programm in the emulator using Termux
and follow the Android instructions, else it won't work !
-----------------------------------------------------------
NOTE IF YOU ARE USING WINE OR SIMILAR SOFTWARE:
On Linux and MacOS, downloading the programm and running it
by double-clicking it should work.
If it doesn't work, or you are not using Linux or MacOS
(example: any BSD system), download the Windows version
and run it in Wine or the programm you use to run the game.
-----------------------------------------------------------
THIS PROGRAM IS FREELY RELEASED UNDER MIT LICENSE.
IF YOU PAID FOR IT, YOU SHOULD ASK FOR REFUND!
-----------------------------------------------------------
ALWAYS DOWNLOAD THE PROGRAMM FROM OUR GITHUB (link below)
TO MAKE SURE YOU DON'T GET MALWARE!
-----------------------------------------------------------
For more informations/help, check our GitHub at:
		https://github.com/HGStyle/GD-SaveFileFixer/""")
	input('Press Enter to continue.')
	clear_screen()
	MODES_RESPONSES = [
		"Static Classic: Will get the game data folder for your OS, and repair only the known savefiles.",
		"Dynamic Classic: Will get the game data folder for your OS, and repair all the data files that uses GD encoding.",
		"Static Search: Will search for known savefiles recursively in the data folder of your OS.",
		"Dynamic Search: Will search for data files that uses GD encoding recursively in the data folder of your OS.",
		"Manual: Will ask you for the paths of the savefiles. Don't use if you are not guided or if you're not a technerd."
	]
	MODES_QUESTION = """
Which mode do you want to use? Every mode makes a backup of each file found.
NOTES ABOUT MODES:
	- Always try first Classic modes.
	- Search modes are a bit long but will work with GDPS while Classics modes can't.
	- Search modes are made to try to not corrupt non-GD files, however this is not guaranteed.
	- Manual is for you if you know where are your savefiles and what are their paths.""".strip()
	modes_choice = ask_for_choice(MODES_QUESTION, MODES_RESPONSES)  # decided to not care about this: peps.python.org/pep-8/#constants
	# Get the system name
	system_name = get_system_name()
	clear_screen()
	# Launch the selected mode
	if modes_choice in [0, 1]:
		gamedata_folder = get_game_data_folder(system_name)
		if modes_choice == 0:
			savefiles = search_static_savefiles(gamedata_folder)
		else:
			savefiles = search_savefiles(gamedata_folder)
	elif modes_choice in [2, 3]:
		data_folder = get_data_folder(system_name)
		if modes_choice == 2:
			savefiles = search_static_savefiles(data_folder)
		else:
			savefiles = search_savefiles(data_folder)
		game_names = [i[len(data_folder):].split(os.sep)[0] for i in savefiles]
		print("""
Which "copy of Geometry Dash" do you want to fix? Write the number of the choice.
You can put multiple ones by separating the numbers of your choice by a slash (/).
Not choosing anything by just pressing Enter will fix them all.""".strip())
		print('\n'.join(game_names))
		selected_game_names = []
		user_choice = input('---> ')
		if not user_choice:
			selected_game_names = game_names
		else:
			user_choice = user_choice.split('/')
			for selection in user_choice:
				if selection.strip() in game_names:
					selected_game_names.append(selection.strip())
				else:
					print(f'Ignoring "{selection.strip()}" as the name is not recognized.')
			if not selected_game_names:
				print('Warning: No valid name has been recognized, selecting them all...')
				selected_game_names = game_names
		savefiles = [i for i in savefiles if i[len(data_folder):].split(os.sep)[0] in selected_game_names]
	else:
		savefiles = []
		user_input = None
		while user_input != "":
			user_input = ask_for_path("Which file should be added to savefile list?" +
			   "\nEnter nothing to start fixing all the selected savefiles.")
			is_savefile = is_valid_savefile(user_input)
			if user_input and is_savefile:
				savefiles.append(user_input)
			elif user_input and not is_savefile:
				print('This savefile is not seeming valid. Make sure you did put the right file!' +
				   '\nIf you did, then sorry, everything in it is probably lost forever, and I cannot do anything.')
			clear_screen()
	clear_screen()
	print(f'{len(savefiles)} savefiles selected...')
	print('Backing up savefiles...')
	errors = 0
	for savefile in savefiles:
		try:
			backup_dir = get_backup_dir(os.path.dirname(savefile))
			backup_file(savefile, backup_dir)
		except Exception:
			errors += 1
			print('An exception occured while backuping file: ' + savefile)
	print('Backup done.')
	if errors > 0:
		if ask_for_choice(['Yes', 'No'], "Error(s) occured. Do you still want to try to fix the savefiles ?") == 1:
			exit()
	del errors  # A bit of cleanup (completely useless, I know)
	clear_screen()
	print('Fixing the savefiles...')
	errors = 0
	for savefile in savefiles:
		if not fix_savefile(savefile):
			errors += 1
			print('An exception occured while fixing file: ' + savefile)
		else:
			print('Savefile fixed successfully: ' + savefile)
	print('Fixing done.')
	if errors > 0:
		print(f'{errors} number of errors happened while fixing all of them.')
	print("Now, you can retry to launch Geometry Dash. If it didn't worked, I'm sorry, but I can't do anything more.")
	exit()
