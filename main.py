# -*- coding: utf-8 -*-
# Import needed Python default libraries
import base64, datetime, os, shutil, sys, traceback, gzip, platform, time, fnmatch
# Try to import the optionnal PyCryptoDome library (you need to install it)
try:
	from Crypto.Cipher import AES
except ImportError:
	print("WARNING: PyCryptoDome hasn't been found, MacOS or iOS GD Savefile fix won't work !")
	AES = None

# Set Python module variables
__version__ = "1.0.0"
__author__ = "HGStyle & WEGFan"

# Define some functions
def clear_screen():
	os.system('clear' if os.name != "nt" else "cls")

def exit(code=0):
	input('Press enter to exit...')
	if not code:
		clear_screen()
	sys.exit(code)

def fix_savefile(file, decode_type):
	# WARNING: This function does not create any backup !
	# Read the data
	data = open(file, 'rb').read()
	if decode_type.lower().strip() in ["windows", "android", "linux"]:
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
			traceback.print_exc()
			return False
	# todo: ask if ios gd uses macos encryption because im unsure
	elif decode_type.lower().strip() in ["macos", 'ios']:
		# Fix the Savefile with GD MacOS Savefile encryption/encoding
		if not AES:
			print('Please install PyCryptoDome before using that !')
			print('Read the README on the GitHub repo.')
			exit(1)
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
			traceback.print_exc()
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
	shutil.copyfile(file, os.path.join(dir, os.path.basename(file)))
	return True

def create_backup_dir(path):
	# Simple function to create backup directory
	dirname = "backup_" + datetime.datetime.now().strftime('Y%Y-M%m-D%d-h%H')
	if not os.path.exists(os.path.join(path, dirname)):
		os.mkdir(os.path.join(path, dirname))
	return os.path.join(path, dirname)

def is_valid_savefile(filepath):
	# Simple function that tries to decompress files that may be savefiles
	# If an error occurs while decrypting/decoding, its not a GD savefile
	# (it returns False) else it returns True (its a valid GD savefile)
	try:
		data = open(filepath, 'rb').read()
		if systemname in ["windows", "android", "linux"]:
			data = bytes(c ^ 11 for c in memoryview(data)[:len(data) & -4])
			data = base64.urlsafe_b64decode(data)
			data = gzip.decompress(data)
		else:
			if not AES:
				print('Please install PyCryptoDome before using that !')
				print('Read the README on the GitHub repo.')
				exit(1)
			cipher = AES.new(b'ipu9TUv54yv]isFMh5@;t.5w34E2Ry@{', AES.MODE_ECB)
			data = cipher.decrypt(data)
			if data[-1] < 16:
				data = data[:-last]
	except:
		return False
	return True

def search_savefile(name, path, print_results=False):
	results = []
	for root, dirs, files in os.walk(path, onerror=lambda _: None):
		try:
			for file in files:
				if fnmatch.fnmatch(file, name) and is_valid_savefile(os.path.join(root, file)):
					results.append(os.path.join(root, file))
					if print_results:
						print('Found savefile: ' + results[-1])
		except PermissionError:
			continue
	return results

if __name__ == "__main__":
	clear_screen()
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
THIS TOOL IS PROVIDEN WITHOUT ANY GUARANTEE OF SUCCESS,
OR MAY ACCIDENTALY BROKES YOUR SAVEFILES, THATS WHY IT
AUTOMATICALLY CREATES A BACKUP BEFORE MODIFYING ANYTHING !
Rollback this backup manually if you need it.
""")
	input('Press ENTER to start this programm !')
	clear_screen()
	# Ask user for the method to find Savefiles
	choices = [
		"Manual (will ask you for the Savefiles to fix, don't use unless you are a technerd)",
		"Automatic (will fix Savefiles in the default GD folder for your OS, don't use if you wanna fix a GDPS or your GD is modified)",
		"Automatic Search (will search the default app data directory for your OS to get Savefiles, recommended)",
		"Automatic Full Search (will search all your storage to find Savefiles, takes a very long time, use this as your last chance)"
	]
	choice = ask_for_choice("Choose a method to get Savefiles:\nNote that all the methods will make a backup of your savefiles !", choices)
	savefiles = []
	clear_screen()
	# Get the OS name
	systemname = ""
	if platform.system() == "Windows" or platform.system() == "Cygwin":
		systemname = "windows"
	elif platform.system() == "Darwin" and "Mac" in platform.platform():
		systemname = "macos"
	elif platform.system() == "Linux":
		systemname = "linux"
	elif platform.system() == "Android":
		systemname = "android"
	elif platform.system() == "Darwin" and "Mac" not in platform.platform():
		systemname = "ios"
	# Do the user choice method
	if choice == choices[0]:
		# Ask the user for the Savefiles
		while True:
			if len(savefiles):
				print('Savefiles list:')
			for savefile in savefiles:
				print(savefile)
			savefile = input('Input savefile path to add (empty to start fixing) -> ')
			if not savefile:
				break
			elif not os.path.exists(savefile):
				input('Savefile does not exists, check the filepath. Press enter to continue.')
			elif not os.access(savefile, os.R_OK):
				# Cannot access to path, gave tips to user based on the OS
				if systemname == "android":
					print('Access denied, be sure to have installed the modified version of the app modified by App Cloner, or root your device.')
				elif systemname == "ios":
					print('Access denied, be sure that your Apple device is jailbroken.')
				else:
					print('Access denied, try to relaunch this programm as root/administrator.')
					input('Press Ctrl+C to exit, press enter to continue.')
			else:
				savefiles.append(savefile)
			clear_screen()
	elif choice == choices[1]:
		print(f'Getting the appropriate app data folder for your system ({platform.platform()})...')  # I may put that code into a function, but later
		# Get the savefiles from the default folder for the OS
		if systemname == "windows":
			# Assuming its stored in %localappdata%/GeometryDash
			path = os.path.join(os.getenv('LOCALAPPDATA'), "GeometryDash")
		elif systemname == "macos":
			# Assuming its stored in ~/Library/Application Support/GeometryDash
			path = os.path.expanduser("~/Library/Application Support/GeometryDash")
		elif systemname == "linux":
			if os.path.exists(os.path.expanduser('~/.local/share/Steam/')) or os.path.exists(os.path.expanduser('~/.steam/')):
				# Assuming that the user uses Steam Play to run Geometry Dash
				if os.path.exists(os.path.expanduser('~/.local/share/Steam/')):
					steam_path = "~/.local/share/Steam/"
				elif os.path.exists(os.path.expanduser('~/.steam/')):
					if os.path.exists(os.path.expanduser('~/.steam/steam/')):
						steam_path = "~/.steam/steam/"
					else:
						steam_path = "~/.steam/"
				else:
					steam_path = "~/"
				path = os.path.expanduser(steam_path + "steamapps/compatdata/322170/pfx/drive_c/users/{}/Local Settings/Application Data/GeometryDash")
				# Gets the current Steam account username (needed to get the Geometry Dash Savefile path)
				try:
					steam_user_dir = os.path.expanduser(steam_path + "userdata")
					steam_user_dirs = [os.path.join(steam_user_dir, d) for d in os.listdir(steam_user_dir) if os.path.isdir(os.path.join(steam_user_dir, d))]
					steam_user_account = os.path.basename(max(steam_user_dirs, key=os.path.getmtime))
				except:
					steam_user_account = "steamuser"
				# Adds the Steam account username to the path
				path = path.format(steam_user_account)
			elif os.path.exists(os.path.expanduser('~/.local/share/lutris/')) or os.path.exists(os.path.expanduser('~/.lutris/')):
				# Assuming that the user uses Lutris to run Geometry Dash
				if os.path.exists(os.path.expanduser('~/.local/share/lutris/')):
					lutris_path = "~/.local/share/lutris/"
				elif os.path.exists(os.path.expanduser('~/.lutris/')):
					if os.path.exists(os.path.expanduser('~/.lutris/lutris/')):
						lutris_path = "~/.lutris/lutris/"
					else:
						lutris_path = "~/.lutris/"
				path = os.path.expanduser(lutris_path + "runners/wine/<version>/prefix/drive_c/users/{}/Local Settings/Application Data/GeometryDash")
				path = path.format(path.split(os.sep)[2])  # Replaces {} by current session username
			else:
				# Assuming that the user uses Wine to run Windows Geometry Dash
				if os.path.exists(os.path.expanduser('~/.wine/')):
					if os.path.exists(os.path.expanduser('~/.wine/wine/')):
						wine_path = "~/.wine/wine/"
					else:
						wine_path = "~/.wine/"
				elif os.path.exists(os.path.expanduser('~/.local/share/applications/wine/')):
					wine_path = "~/.local/share/applications/wine/"
				path = os.path.expanduser(wine_path + "drive_c/users/{}/Local Settings/Application Data/GeometryDash")
				path = path.format(path.split(os.sep)[2])  # Replaces {} by current session username
		elif systemname == "android":
			# Assuming its stored in /data/data/com.robtopx.geometryjump/ and user is root or has enabled access to this directory using App Cloner
			path = "/data/data/com.robtopx.geometryjump/"
		elif systemname == "ios":
			# Assuming its stored in /var/mobile/Containers/Data/Application/com.robtop.geometryjump/ and user has a jailbroken device
			path = "/var/mobile/Containers/Data/Application/com.robtop.geometryjump/"
		else:
			# Seriously ? Not using any of these operating systems ?
			print(f'Your operating system ({platform.platform()}) is not supported, why do you use this OS ?')
			print('If you are using Jython or Cygwin, please install and use the original Python implementation (CPython) instead.')
			exit(1)
		print('Folder found: ' + path)
		print('Checking path...')
		if not os.access(path, os.R_OK):
			# Cannot access to path, gave tips to user based on the OS
			if systemname == "android":
				print('Access denied, be sure to have installed the modified version of the app modified by App Cloner, or root your device.')
			elif systemname == "ios":
				print('Access denied, be sure that your Apple device is jailbroken.')
			else:
				print('Access denied, try to relaunch this programm as root/administrator.')
			exit(1)
		elif not os.path.exists(path):
			print("The automatically selected path hasn't been found, please use the \"Automatic Search\" mode.")
			exit(1)
		# Gets all the savefiles in this folder
		print('Getting savefiles...')
		for file in os.listdir(path):
			if file in ['CCGameManager.dat', 'CCLocalLevels.dat', 'CCGameManager2.dat', 'CCLocalLevels2.dat']:
				savefiles.append(os.path.join(path, file))
				print('Found savefile: ' + savefiles[-1])
	elif choice == choices[2]:
		# Browse the app data directory(s) of the OS to get Savefiles
		paths_to_browse = {
			"windows": [
				os.getenv('LOCALAPPDATA')
			],
			"macos": [
				os.path.expanduser("~/Library/Application Support")
			],
			"linux": [
				os.path.expanduser("~/.local/share"),
				os.path.expanduser("~/.steam"),
				os.path.expanduser("~/.lutris"),
				os.path.expanduser("~/.wine")
			],
			"android": [
				"/data/data"
			],
			"ios": [
				"/var/mobile/Containers/Data/Application"
			]
		}
		paths = paths_to_browse.get(systemname)
		if not paths:
			# Seriously ? Not using any of these operating systems ?
			print(f'Your operating system ({platform.platform()}) is not supported, why do you use this OS ?')
			print('If you are using Jython or Cygwin, please install and use the original Python implementation (CPython) instead.')
			exit(1)
		print('Searching OS app data directory for savefiles...')
		for path in paths:
			svs = search_savefile("*.dat", path, print_results=True)
			for savefile in svs:
				savefiles.append(savefile)
	elif choice == choices[3]:
		# Browse all the user storage to get Savefiles (long)
		root = os.path.abspath(os.path.sep)
		# On Windows, it'll be `C:\`, on Unix (MacOS, Linux, Android, iOS, etc...) it'll be `/`
		print("Searching root directory: " + root)
		print("This may take some time, grab a coffee.")
		print("Consider watching a film if your device has millions of files/folders.")
		print("IMPORTANT: DONT CLOSE THIS WINDOW / THIS APP (YOU CAN CHANGE APP BUT DONT CLOSE IT)")
		print("WARNING FOR MOBILE: IF YOUR DEVICE IS FROM A CHINESE COMPANY (LIKE SAMSUNG, HUAWEI OR XIAOMI)")
		print("CHANGING THIS APP MAY ACCIDENTALY STOP THE SEARCH BECAUSE OF THEIR DUMB OPTIMIZATION SYSTEM")
		print("IF YOU WANNA CHANGE APP, CLOSE THIS APP, GO TO SETTINGS -> APPS -> SELECT THE APP -> BATTERY")
		print("BATTERY OPTIMIZATION -> SELECT ALL APPS IF NEEDED -> SELECT THE APP AGAIN IF NEEDED -> DISABLE")
		print("THEN RESTART THE APP, LAUNCH THE PROGRAMM AGAIN, AND WHEN YOU SEE THIS SCREEN YOU CAN CHANGE APP")
		print("ALSO MAKE SURE TO DONT LOCK YOU DEVICE SCREEN (ON EVERY DEVICE) THIS MAY CLOSE THE PROGRAMM TOO")
		savefiles = search_savefile("*.dat", root, print_results=True)
	clear_screen()
	print('Backuping savefiles...')
	# For each savefile, create a backup dir (if needed) then backup the savefile in this directory
	for savefile in savefiles:
		path = os.path.abspath(os.path.dirname(savefile))
		backup_dir = create_backup_dir(path)
		backup_file(savefile, backup_dir)
		print('Backup saved for savefile: ' + savefile)
	print('Backup done.')
	time.sleep(3)
	# Fix all the savefiles
	clear_screen()
	print('Trying to fix savefiles...')
	errors = 0
	success = 0
	for savefile in savefiles:
		try:
			result = fix_savefile(savefile, systemname)
			print("Savefile fixed: " + savefile)
			success += 1
		except:
			print("Error while fixing savefile: " + savefile)
			errors += 1
	print("Savefiles has been fixed !")
	print(f"Success: {success}")
	print(f"Errors: {errors}")
	exit(0)
