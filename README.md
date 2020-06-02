# files harmoniser
A python tool that tries to merge a potential dup folder of files (recursively) with a canonical master. 

Definitions: 

Master - this is canonical master folder. It doesn't matter where it is. Files / folders are allowed to be put in this folder. They are not allowed to be deleted. 

Sidecar - this is the potential duplicate folder. Ideally its the same approx "shape" or structure as the canonical master. Files / Folders are allowed to be deleted from this folder. They are not allowed to be added. 

Fixity - fixity is the digital "fingerprint" of a file. It can be used to help establish digital uniqueness.  This tool uses MD5 as its fixity process.

## Notes

There are three potential outcomes. 

1. Move -  a file in the sidecar is considered new to the master folder, and is moved (not copied) from the sidecar to the master.
2. Delete - a file in the sidecar is considered to be a duplicate for a file in the master fodler, and is deleted. There are some senisitivity controls for how a duplicate status is established. 
3. No nothing - a file in the side car matches either fixity, filename, or file ID and is flagged/logged accordingly. This is dependant on the sensitivity controls.  

Written logs are always made for every step/check thats made and the resulting decions made by the tool. These are found in the 'log' folder. 

## How to use it

This tools assumes the following. You have python 3.6 or greater. You have programmatic access to both folders via python (master, and sidecar). 

There are some vaules to edit in the script: 

master - set this to your master folder
sidecar - set this to your sidecar folder
project_name_for_log - set this to a name associated with your file set so you monitor your log files. 


There are number of filters or switches in the tool that change its behaviour. 

The most important is 

    commit

When this is set to True, the tool is allowed to make changes to your files. Use woth caution. 

The others change the visible information or decision logic:

    verbose
    
When set to `True`, every item is logged on screen in the terminal view. Written logs are always made for every step regardless.

    collisions_only

When this is set to `True`, only the fixity / name space collisions are flagged on screen. It does not report the moves or deletes. Written logs are always made for every step regardless.

    use_low_conf_fixity

When set to `True` the tool considers a matching fixity found anywhere in the collection as a potent match, and sets a logged "Do nothing" status for a corresponding file. When set to `False` the fixity is only relevent for any file with a matching filepath in both folders. 

    use_low_conf_file_name 

When set to `True` the tool considers a matching filename (not path) found anywhere in the collection as a potent match, and sets a logged "Do nothing" status for a corresponding file. When set to `False` the filename (not path) is only relevent for any file with a matching filepath in both folders. 

    use_low_conf_file_id 

File ID is considered to be the filename with its file exension removed. E.g. the filename `my_file.doc` would have the file ID of `my_file`.
When set to `True` the tool considers a matching file ID (not path or name) found anywhere in the collection as a potent match, and sets a logged "Do nothing" status for a corresponding file. When set to `False` the ID (not path or name) is only relevent for any file with a matching filepath in both folders. This is lowest confidence matcher in the desicion logic. 

     purge_logs
 
 When this is set to 'True' before any processing is completed (and logged) the logs folder is checked for any log files that pertain to the project name set previously. If found, these are deleted. WHen set to `False` the logs are appended to every run. This means if `commits` are also not being made, the same information is recorded repeatedly. 
 
     debug
     
When this is set to `True` every decision for every file is shown on screen. Its useful when / if files aren't being recorded as you expect. 

Having work through the set of files, it gives a sumamry: 

    *** Results ***
    
    Test run.
    This is what will happen if you set commit to True
    
    Total files in master: 24338
    Total files in sidecar: 25328
    
    Files deleted from sidecar as duplicate:: 23660
    File ID exists elsewhere in the collection - no action: 176
    Filename exists elsewhere in collection - no action: 1
    Fixity exists elsewhere in collection - no action: 620
    Files moved from sidecar to master (new content): 871

    Finished at 2020-06-03 10:08:35

The corresponding log files, one for each outcome, is found in the `logs` folder

To make extra use of this tool, consider using it with the ghost-collection. This can speed up the processing test dramatically, especially if you're repeating steps to work out best results, or iterating through the collection.  

https://github.com/jayGattusoNLNZ/Ghost_Collections

Also consider using rePeater if you want to automate your decision logic. 

 https://github.com/jayGattusoNLNZ/rePeater
