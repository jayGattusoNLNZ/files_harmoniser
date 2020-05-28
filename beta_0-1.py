import os
import hashlib
import shutil
import datetime

def md5(my_file):
	hash_md5 = hashlib.md5()
	with open(my_file, "rb") as f:
		for chunk in iter(lambda: f.read(4096), b""):
			hash_md5.update(chunk)
	return hash_md5.hexdigest()

def get_files_and_folders_from_root(parent):
	my_files = {}
	my_hashes = {}
	for root, subs, files in os.walk(parent):
			for f in files:
				my_md5 = md5(os.path.join(root, f))
				my_file = os.path.join(root, f).replace(parent, "")[1:]
				my_files[my_file] = my_md5

				if my_md5 not in my_hashes:
					my_hashes[my_md5] = []
				
				my_hashes[my_md5].append(my_file)
	return my_files, my_hashes

def delete_and_log(my_file, md5, commit=False, verbose=False):
	my_file = os.path.join(sidecar, my_file)
	with open(f"{project_name_for_log}_deleted_files.log", 'a') as data:
		data.write(f"{my_file}|{md5}|{datetime.datetime.now()}\n")
	if commit:
		os.remove(my_file)
	if verbose:
		print (f"Deleting dup: {my_file}")

def move_and_log(my_file, md5, commit=False, verbose=False):
	with open(f"{project_name_for_log}_moved_files.log", 'a') as data:
		data.write(f"{my_file}|{md5}|{datetime.datetime.now()}\n")
	if commit:
		folder, __ = os.path.join(master, my_file).rsplit(os.sep, 1)
		if not os.path.exists(folder):
			os.makedirs(folder)
		shutil.move(os.path.join(sidecar, my_file), os.path.join(master, my_file)) 
	if verbose:
		print (f"Moving new: {my_file}")

def do_nothing_and_log(my_file, md5_1, md5_2, commit=False, verbose=False):
	with open(f"{project_name_for_log}_fixity_mismatch_files.log", 'a') as data:
		my_file_1 = os.path.join(master, my_file)
		my_file_2 = os.path.join(sidecar, my_file)
		data.write(f"{my_file_1}|{md5_1}|{my_file_2}|{md5_2}|{datetime.datetime.now()}\n")
	if commit:
		pass
	if verbose:
		print (f"Fixity Mismatch: {my_file}")

def delete_empty_folders():
	folders = []
	for root, subs, files in os.walk(sidecar):
		for sub in subs:
			folders.append(os.path.join(root, sub))
	for folder in folders[::-1]:
		if len(os.listdir(folder)) == 0:
			os.rmdir(folder)



master = r"C:\projects\files_harmoniser\test_master"
sidecar = r"C:\projects\files_harmoniser\test_sidecar"
project_name_for_log = "test-files"

verbose = True
commit = False

master_files, master_hashes = get_files_and_folders_from_root(master)
sidecar_files, sidecar_hashes = get_files_and_folders_from_root(sidecar)

master_hashes
for filename, v in sidecar_files.items():
	if filename in master_files:
		if sidecar_files[filename] == master_files[filename]:
			delete_and_log(filename, sidecar_files[filename],commit=commit,verbose=verbose)
		else:
			do_nothing_and_log(filename, master_files[filename], sidecar_files[filename],commit=commit,verbose=verbose)
	else:
		move_and_log(filename, sidecar_files[filename],commit=commit,verbose=verbose)
delete_empty_folders()