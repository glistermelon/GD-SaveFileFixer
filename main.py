#!/usr/bin/env python3
# -*- coding: utf-8 -*-
### DEVELOPER WARNING: THE SYNTAX USED IN THIS PROGRAM MOSTLY DOES NOT RESPECT THE PEP 8 SYNTAX, YOUVE BEEN WARNED ###
# Imports the necessary libraries
import base64
import os
import sys
import gzip
import customtkinter as tkinter
from tkinter import messagebox
import pywinstyles
from datetime import datetime
import shutil

IS_COMPILED = "__compiled__" in globals() # Difference between compiled and frozen:
IS_FROZEN = getattr(sys, 'frozen', False) # Frozing is putting Python and the script in an EXE like PyInstaller/Oxidizer

# Set some Python variables
__version__ = "2.0.0"
__author__ = "HGStyle"
__original_by__ = "WEGFan"
__program_name__ = "GD-SaveFile-Fixer"
__source__ = "https://github.com/HGStyle/GD-SaveFileFixer"
__license__ = "MIT License"

# Function to decode a savefile
def decode_savefile(data: bytes) -> bytes:
	# Decode the savefile using non-Apple GD encoding
	data = bytes(c ^ 11 for c in memoryview(data)[:len(data) & -4])
	data = base64.urlsafe_b64decode(data)
	data = gzip.decompress(data)
	return data

# Function to encode a savefile
def encode_savefile(data: bytes) -> bytes:
	# Encode the savefile using non-Apple GD encoding
	data = gzip.compress(data)
	data = base64.urlsafe_b64encode(data)
	data = bytes(c ^ 11 for c in data)
	return data

# Function to fix a savefile
def fix_savefile(filepath: str) -> bool:
	try:
		# Read the data
		data = open(filepath, 'rb').read()
		# Decode the savefile
		data = decode_savefile(data)
		if not data:
			return False
		# Fix the savefile
		data = data.replace(b'><', b'> <')
		# Encode the savefile
		data = encode_savefile(data)
		if not data:
			return False
		# Write the data
		with open(filepath, 'wb') as f:
			f.write(data)
		return True
	except Exception:
		return False

class BackupException(Exception):
	pass

def get_backup_dir(file_dir : str) -> str:
	date = datetime.now().strftime('%d-%m-%Y %H-%M-%S')
	backup_dir = os.path.join(file_dir, 'savefile fix backups ' + date)
	if os.path.exists(backup_dir):
		raise BackupException(f'Failed to get backup directory in {file_dir}')
	os.mkdir(backup_dir)
	return backup_dir

def backup_savefile(backup_dir, file_path : str) -> bool:
	backup_path = os.path.join(backup_dir, os.path.basename(file_path))
	if os.path.exists(backup_path):
		raise BackupException(f'Failed to backup {os.path.basename(file_path)}. Backup file name not available.')
	shutil.copy2(file_path, backup_path)

# Function to check is a file a Geometry Dash savefile (now its a better algorithm)
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
		decoded = decode_savefile(encoded).decode()
	except Exception:
		return False
	if not decoded:  # Decoding failed
		return False
	if "<" not in decoded or ">" not in decoded:
		return False  # Not XML data
	return True

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

window = tkinter.CTk()
window.title('GDPS Savefile Fixer (Windows)')

def clear_window():
	for w in window.winfo_children(): w.destroy()

def error(message):
	messagebox.showerror('Error', message)

def notify(message):
	messagebox.showinfo('Hello!', message)

def check_for_savefiles(folder : str):
	for f in os.listdir(folder):
		if is_savefile_name(f) and is_valid_savefile(os.path.join(folder, f)):
			return True
	return False

def try_fix_savefiles(savefile_dir : str):

	savefile_paths = [os.path.join(savefile_dir, f) for f in os.listdir(savefile_dir) if is_savefile_name(f)]
	savefile_paths = [p for p in savefile_paths if is_valid_savefile(p)]

	try:
		backup_dir = get_backup_dir(savefile_dir)
		for savefile_path in savefile_paths:
			backup_savefile(backup_dir, savefile_path)
	except BackupException as ex:
		error(str(ex))
		return

	fixed = 0
	failed = 0
	for savefile_path in savefile_paths:
		if fix_savefile(savefile_path): fixed += 1
		else: failed += 1
	notify(
		f'{fixed} savefiles were fixed.\n{failed} savefiles failed to be fixed.'
		+ f'\n\nIf your GDPS still doesn\'t open, request support on the Discord server.'
	)

def ask_initial_question():

	notify(
		'If the window appears to be frozen, don\'t panic! I don\'t feel like implementing multithreading today, so'
		' at the moment, whenever the program is actually doing stuff, the window freezes. Just wait for it to unfreeze.'
	)

	label = tkinter.CTkLabel(window, text='Have you renamed your GDPS since it stopped working?')
	label.pack(pady=10, padx=10)

	frame = tkinter.CTkFrame(window, fg_color="transparent")
	frame.pack(pady=10)

	yes_button = tkinter.CTkButton(frame, text='Yes', width=70, command=select_save_dir)
	yes_button.grid(column=0, row=0, padx=5)

	no_button = tkinter.CTkButton(frame, text='No', width=70, command=select_gdps)
	no_button.grid(column=1, row=0, padx=5)

def select_save_dir():

	clear_window()

	data_folder = os.getenv('LOCALAPPDATA')
	folders = [f for f in os.listdir(data_folder) if os.path.isdir(os.path.join(data_folder, f))]
	folders_with_savefiles = []
	for folder in (os.path.join(data_folder, f) for f in folders):
		try:
			for file in os.listdir(folder):
				if is_savefile_name(file) and is_valid_savefile(os.path.join(folder, file)):
					folders_with_savefiles.append(os.path.basename(folder))
					break
		except:
			pass # some folders can't be accessed for security reasons anyway

	if len(folders_with_savefiles) == 0:
		error('Failed to find any Geometry Dash save data on your PC.')
		window.destroy()
		return

	label = tkinter.CTkLabel(
		window,
		text='Do your recognize any of the following as the previous name of your GDPS executable?'
	)
	label.pack(pady=10, padx=10)

	select_dropdown = tkinter.CTkOptionMenu(
		master=window,
		values=folders_with_savefiles,
		width=200
	)
	select_dropdown.pack(pady=10)

	def fix_savefiles_callback():
		try_fix_savefiles(os.path.join(data_folder, select_dropdown.get()))

	continue_button = tkinter.CTkButton(window, text='I recognize this one', command=fix_savefiles_callback)
	continue_button.pack(pady=10)

	def no_callback():
		notify('I don\'t know where your savefile should be then! You can request support on the Discord server.')
		window.destroy()
		return

	no_button = tkinter.CTkButton(window, text='No', command=no_callback)
	no_button.pack(pady=10)

def select_gdps():

	clear_window()

	label = tkinter.CTkLabel(window, text='Please provide your GDPS executable (typically 2.1gdps.exe).')
	label.pack(pady=10, padx=10)

	path_input = tkinter.CTkEntry(window, width=400, placeholder_text='Input the file path here, or use the button below.')
	path_input.pack(pady=10, padx=10)

	savefile_dir = []

	def select_gdps_callback():

		nonlocal savefile_dir
		nonlocal select_button
		nonlocal fix_button

		select_button._state = tkinter.DISABLED
		pywinstyles.set_opacity(select_button, value=0.4)

		gdps_path = tkinter.filedialog.askopenfilename()[:-4]

		path_input.delete(0, 'end')
		path_input.insert(0, gdps_path)

		savefile_dir = os.path.join(os.getenv('LOCALAPPDATA'), os.path.basename(gdps_path))
		if not os.path.exists(savefile_dir):
			error('Failed to find your savefile location!')
			return

		if not check_for_savefiles(savefile_dir):
			error('The location where your savefile should be was found, but there are no savefiles there!')
			return

		select_button._state = tkinter.ACTIVE
		pywinstyles.set_opacity(select_button, value=1.0)

		fix_button._state = tkinter.ACTIVE
		pywinstyles.set_opacity(fix_button, value=1.0)

	select_button = tkinter.CTkButton(window, text='Select a File', command=select_gdps_callback)
	select_button.pack(pady=10)

	def fix_savefiles_callback():
		try_fix_savefiles(savefile_dir)

	fix_button = tkinter.CTkButton(window, text='Fix Savefile(s)', command=fix_savefiles_callback)
	fix_button._state = tkinter.DISABLED
	pywinstyles.set_opacity(fix_button, value=0.4)
	fix_button.pack(pady = 10)

# Run if not imported
if __name__ == "__main__":

	try:
		ask_initial_question()
		window.mainloop()
	except Exception as e:
		error('An exception occurred! Report this to Glistermelon:\n\n' + str(e))