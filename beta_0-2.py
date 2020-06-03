import os
import hashlib
import shutil
import datetime
from harmoniser_ignore_lists import fixities as fixities_to_ignore
from harmoniser_ignore_lists import filenames as filenames_to_ignore 

logs_folder = "logs"

if not os.path.exists(logs_folder):
	os.makedirs(logs_folder)


def md5(my_file):
	hash_md5 = hashlib.md5()
	with open(my_file, "rb") as f:
		for chunk in iter(lambda: f.read(4096), b""):
			hash_md5.update(chunk)
	return hash_md5.hexdigest()

def get_files_and_folders_from_root(parent):
	my_files = {}
	my_hashes = {}
	my_filenames = {}
	my_file_ids = {}
	for root, subs, files in os.walk(parent):
			for f in files:
				my_file_path = os.path.join(root, f)
				my_md5 = md5(my_file_path)
				

				### ids
				__id, __ = f.rsplit(".", 1)
				if __id not in my_file_ids:
					my_file_ids[__id] = []
				my_file_ids[__id].append(my_file_path)

				### filenames
				if f not in my_filenames:
					my_filenames[f] = []
				my_filenames[f].append(my_file_path)

				### file paths
				my_file = os.path.join(root, f).replace(parent, "")[1:]
				my_files[my_file] = my_md5
				
				### hashes
				if my_md5 not in my_hashes:
					my_hashes[my_md5] = []
				my_hashes[my_md5].append(my_file)
	return my_files, my_hashes, my_filenames, my_file_ids

def delete_and_log(my_file, md5, commit=False, verbose=False):
	logfile =  f"{os.path.join(logs_folder, project_name_for_log)}_#_deleted_files.log"
	my_file = os.path.join(sidecar, my_file)

	if not os.path.exists(logfile):
		with open(logfile, 'a') as data:
			data.write(f"Sidecar Filename|MD5|Date/Time\n")

	with open(logfile, 'a') as data:
		data.write(f"{my_file}|{md5}|{datetime.datetime.now()}\n")
	if commit:
		os.remove(my_file)
	if verbose and not collisons_only:
		print (f"Deleting dup: {my_file}")

def filepath_exists_changed_file(my_file, master_md5, sidecar_md5, commit=False, verbose=False):

	logfile = f"{os.path.join(logs_folder, project_name_for_log)}_#_filepath_exists_content_changed.log"
	
	if not os.path.exists(logfile):
		with open(logfile, 'a') as data:
			data.write(f"Sidecar Filename|Master MD5|Sidecar MD5|Date/Time\n")

	with open(logfile, 'a') as data:
		data.write(f"{my_file}|{master_md5}|{sidecar_md5}|{datetime.datetime.now()}\n")
	if commit:
		pass
	if verbose:
		print (f"Fixity changed in {my_file}")

def fixity_exists_different_location(my_file, master_file, sidecar_md5, commit=False,verbose=False):
	
	logfile = f"{os.path.join(logs_folder, project_name_for_log)}_#_fixity_exists_content_different_locations.log"

	if not os.path.exists(logfile):
		with open(logfile, 'a') as data:
			data.write(f"Sidecar Filename|Master Filename|MD5|Date/Time\n")

	with open(logfile, 'a') as data:
		data.write(f"{my_file}|{master_file}|{sidecar_md5}|{datetime.datetime.now()}\n")
	if commit:
		pass
	if verbose:
		print (f"Fixity changed in {my_file}")

def filename_exists(sidecar_filename, sidecar_filepath, sidecar_md5, commit=False, verbose=False):
	logfile = f"{os.path.join(logs_folder, project_name_for_log)}_#_filename_exists.log"

	if not os.path.exists(logfile):
		with open(logfile, 'a') as data:
			data.write(f"Filename|Sidecar Filepath|Sidecar MD5|Date/Time\n")

	with open(logfile, 'a') as data:
		data.write(f"{sidecar_filename}|{sidecar_filepath}|{sidecar_md5}|{datetime.datetime.now()}\n")
	if commit:
		pass
	if verbose:
		print (f"filename exists {sidecar_filename}")

def fileid_exists(sidecar_fileid, sidecar_filepath, sidecar_md5, commit=False, verbose=False):
	logfile = f"{os.path.join(logs_folder, project_name_for_log)}_#_fileid_exists.log"
	
	if not os.path.exists(logfile):
		with open(logfile, 'a') as data:
			data.write(f"File_ID|Sidecar Filepath|Sidecar MD5|Date/Time\n")
	
	with open(logfile, 'a') as data:
		data.write(f"{sidecar_fileid}|{sidecar_filepath}|{sidecar_md5}|{datetime.datetime.now()}\n")
	if commit:
		pass
	if verbose:
		print (f"File ID exists {sidecar_fileid}")

def move_and_log(my_file, my_md5, commit=False, verbose=False):

	logfile = f"{os.path.join(logs_folder, project_name_for_log)}_#_moved_files.log"

	if not os.path.exists(logfile):
		with open(logfile, 'a') as data:
			data.write(f"Sidecar Filename|MD5|Date/Time\n")

	with open(logfile, 'a') as data:
		data.write(f"{my_file}|{my_md5}|{datetime.datetime.now()}\n")
	
	if commit:
		folder, __ = os.path.join(master, my_file).rsplit(os.sep, 1)
		if not os.path.exists(folder):
			os.makedirs(folder)
		shutil.move(os.path.join(sidecar, my_file), os.path.join(master, my_file)) 
		new_hash = md5(os.path.join(master, my_file))
		if not new_hash == my_md5:
			print (f"Copying for file {os.path.join(master, my_file)} has not resulted in the same fixity/file as we started with")
			print ("Quitting without completeing run.")

	
	if verbose and not collisons_only:
		print (f"Moving new: {my_file}")

def delete_empty_folders():
	folders = []
	for root, subs, files in os.walk(sidecar):
		for sub in subs:
			folders.append(os.path.join(root, sub))
	for folder in folders[::-1]:
		if len(os.listdir(folder)) == 0:
			os.rmdir(folder)

def do_purge_logs():
	for f in os.listdir(logs_folder):
		if f.startswith(project_name_for_log+"_#_"):
			log_path = os.path.join(logs_folder, f)
			print (f"Purged log file {f}")
			os.remove(log_path)
	print("\nFinished cleaning up logs \n")


def summeriser(master_files, sidecar_files):

	print ("\n*** Results ***\n") 
	if verbose:
		print ("Test run.\nThis is what will happen if you set commit to True\n")
	else:
		print ("Commit run.\nThe following changes where made\n")

	print (f"Total files in master: {len(master_files)}")
	print (f"Total files in sidecar: {len(sidecar_files)}")
	print ()
	for f in os.listdir(logs_folder):
		if f.startswith(project_name_for_log+"_#_"):
			log_path = os.path.join(logs_folder, f)

			with open(log_path) as data:
				lines = [x for x in data.read().split("\n") if x != ""]
			count = len(lines)-1
			my_string = f.replace(f"{project_name_for_log}_#_", "").replace(".log", "").replace("_", " ").capitalize()

			if my_string == "Deleted files":
				my_string = "Files deleted from sidecar as duplicate"
			elif my_string == "Filename exists":
				my_string = "Filename exists elsewhere in collection - no action"
			elif my_string == "Fixity exists content different locations":
				my_string = "Fixity exists elsewhere in collection - no action"
			elif my_string == "Moved files":
				my_string = "Files moved from sidecar to master (new content)"
			elif my_string == "Fileid exists":
				my_string = "File ID exists elsewhere in the collection"
			elif my_string == "Filepath exists content changed":
				my_string = "File exists in master but has different fixity - no action"
			print (f"{my_string}: {count}")
	print ()
	print (f"Finished at {str(datetime.datetime.now())[:-7]}")
	print ()



def process_sidecar_files(debug=False):

	if purge_logs:

		do_purge_logs()

	master_files, master_hashes, master_names, master_ids = get_files_and_folders_from_root(master)
	sidecar_files, sidecar_hashes, sidecar_names, sidecar_ids = get_files_and_folders_from_root(sidecar)
	for sidecar_filepath, sidecar_fixity in sidecar_files.items():

		file_processed = False

		### sort out the various identifiers
		if sidecar_filepath.count(os.sep) >= 1:
			__, sidecar_filename = sidecar_filepath.rsplit(os.sep, 1)
		else:
			sidecar_filename = sidecar_filepath

		if sidecar_filename.count(".") >= 1:
			sidecar_id, __ = sidecar_filename.rsplit(".", 1)
		else:
			sidecar_id = sidecar_filename

		if debug:
			print (sidecar_filepath)	

		### absolute match - 100% dup. 
		if sidecar_filepath in master_files and sidecar_files[sidecar_filepath] == master_files[sidecar_filepath]:
			delete_and_log(sidecar_filepath, sidecar_fixity, commit=commit,verbose=verbose)
			if debug:
				print (r"absolute match - 100% dup")

		### filepath exists - different fixities
		elif sidecar_filepath in master_files:
			filepath_exists_changed_file(sidecar_filepath, master_files[sidecar_filepath], sidecar_fixity, commit=commit,verbose=verbose)
			if debug:
				print ("filepath exists - different fixities")

		#### lower confidence matches
		
		### fixity exist
		elif sidecar_files[sidecar_filepath] in master_hashes and sidecar_files[sidecar_filepath] not in fixities_to_ignore and use_low_conf_fixity:
			fixity_exists_different_location(sidecar_filepath, master_hashes[sidecar_files[sidecar_filepath]], sidecar_files[sidecar_filepath], commit=commit,verbose=verbose)
			if debug:
				print ("fixity exist")
		
		### file name exists
		elif sidecar_filename in master_names and sidecar_filename not in filenames_to_ignore and use_low_conf_file_name:
			filename_exists(sidecar_filename, sidecar_filepath, sidecar_files[sidecar_filepath], commit=commit, verbose=verbose)
			if debug:
				print ("file name exists")

		### file id exists
		elif sidecar_id in master_ids and use_low_conf_file_id:
			fileid_exists(sidecar_id, sidecar_filepath, sidecar_files[sidecar_filepath], commit=commit, verbose=verbose)
			if debug:
				print ("file id exists")

		### Assumes new - move file into master
		else:
			move_and_log(sidecar_filepath, sidecar_files[sidecar_filepath], commit=commit,verbose=verbose)
			if debug:
				print ("Assumes new - move file into master")

		if debug:
			print ()

	delete_empty_folders()
	delete_empty_folders()
	print ()
	summeriser(master_files, sidecar_files)
	return 



####### EDIT FROM HERE DOWN ONLY ##############


### set to the full path of the canonical master
master = r"E:\ghost_collections\socials\master"

### set to the folder you want to merge
sidecar = r"E:\ghost_collections\socials\ftp"

### set to a useful name for your project   
project_name_for_log = "temp"



### N.B. verbose and commit are global controls. They are inhereted for all processing outcomes
### you can change the various processing outcomes to not use the global value in the main process
### e.g. you might want to log all deletes to screen only by doing:
###	
### 		 delete_and_log(filename, sidecar_files[filename],commit=commit,verbose=True)
###
###	and setting the global to False
###
### 		verbose = False
###

### logs to terminal if True, silent if False
verbose = True

### When verbose is True, only show items that are not absolute dups or considered new files (collisions only)
collisons_only = True

### if True  does moves/deletes - set to False for testing / dry runs 
commit = False

### if True checks for fixity throughout sets -  if fixity found - doesn't move, just logs
use_low_conf_fixity = True

### if True checks for filename throughout sets - if filename found - doesn't move, just logs. 
use_low_conf_file_name = True

### if True checks for file_id (filename, no file extention) throughout sets - if fileid found - doesn't move, just logs
use_low_conf_file_id = True

### use to clear any existing logs before running - useful when going from commit = False to commit = True
### double check you have set the correct project_name_for_log...  
purge_logs = True

process_sidecar_files(debug=False)
