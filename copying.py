"""
Jack Duley, Glidepath Ltd
20/12/19

Copying files & images to Ansible 
"""
import log
import logging
import os
import shutil
import sys
#Directory variables: 
fileStruct = "/home/coding_admin/Bagdrop/" #Main outer file directory
images_Backup = "/home/coding_admin/Documents/Images/" #Wherever the backup of the images is stored
#Files to be copied to ansible:
updatedAnsible = "Bagdrop-HostSetup/ansible/" #Backup ansible directory
pcBackup = "Bagdrop-HostSetup/pc_backup/" #Backup directory
statLog = "Bagdrop-HostSetup/pc_stat_log/" #Log(s) directory
images = "ssbd_images/" #Images directory
#Files to be overridden in ansible:
ansibleMain = "ansible_files/ansible/" #Ansible directory
ansibleImages = "ansible_files/images/" #Images directory
ansibleBackup = "ansible_files/pc_backup/" #PC backup directory
ansibleStat = "ansible_files/pc_stat_log/" #PC stat_log directory

def fileTransfer(srcDir,dstDir):
    """
    transfer the files from the source to the destination.
    making sure that the source exists and isn't empty.
    catch any other errors that could occour
    """
    try:       
        #Can only copy files if source isn't empty & both destination & source exist
        if os.path.exists(srcDir) and len(os.listdir(srcDir))!=0:
            clear(dstDir)
            copy(srcDir,dstDir)
        elif not os.path.exists(srcDir):
            mod_logger.error("Doesn't exist: {}".format(srcDir))
            sys.exit(1)
        else:
            mod_logger.error("Empty source: {}".format(srcDir))
            sys.exit(1)
    except Exception as ex: #Catch any error in try block, e.g FileNotFoundError
        mod_logger.error("Transfer failed with Exception: {}".format(ex))
        sys.exit(1)
    else:
        mod_logger.info("Copied {} to {}".format(srcDir,dstDir))

def clear(dstDir):
    """
    clear out anything in the destination file location
    """
    for oldFile in os.listdir(dstDir):#Clearing destination
        old_path = os.path.join(dstDir,oldFile) #Creating a directory path
        if os.path.isfile(old_path) or os.path.islink(old_path):#old_path is a file or a link
            os.unlink(old_path)
        elif os.path.isdir(old_path):#old_path is a directory/folder
            shutil.rmtree(old_path) 

def copy(srcDir,dstDir):
    """
    copy all the files from source to destination
    """
    for newFile in os.listdir(srcDir):
        new_path = os.path.join(srcDir,newFile)
        if os.path.isfile(new_path) or os.path.islink(new_path):            
            shutil.copy(new_path, dstDir)#Copying from source
        elif os.path.isdir(new_path):
           inner_path = os.path.join(dstDir,newFile) 
           os.mkdir(inner_path)
           copy(new_path,inner_path)

def main():
    """
    setup the logger and call each method for each file to be transfered
    """
    #Logger setup
    global mod_logger
    mod_logger = logging.getLogger(__name__)
    log.main(mod_logger)
    mod_logger.info("Starting copy")
    
    #Copy images from backup to image
    mod_logger.info("Attempting to copy images")  
    fileTransfer(images_Backup,fileStruct+images)

    #Copy updatedAnsible to ansibleMain
    mod_logger.info("Attempting to copy ansible/")    
    fileTransfer(fileStruct+updatedAnsible,fileStruct+ansibleMain) 

    #Copy statLog to ansibleStat
    mod_logger.info("Attempting to copy pc_stat_log/")    
    fileTransfer(fileStruct+statLog,fileStruct+ansibleStat)

    #Copy pcBackup to ansibleBackup
    mod_logger.info("Attempting to copy pc_backup/")
    fileTransfer(fileStruct+pcBackup,fileStruct+ansibleBackup)

    #Copy images to ansibleImages
    mod_logger.info("Attempting to copy ssbd_images/")
    fileTransfer(fileStruct+images,fileStruct+ansibleImages)

if __name__ == "__main__":
    main()
    sys.exit(0)