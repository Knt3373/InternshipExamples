"""
Jack Duley, Glidepath Ltd
06/01/20

Cloning files from a git repository
"""
import log
import logging
import subprocess
import shlex
import sys
import copying 
import os
import shutil

repo_URL = "/glidepathgroup/CUSS-Platform/Bagdrop-HostSetup" #Where the git repo is, on Azure Git repo via SSH
bagdrop = "/home/coding_admin/Bagdrop/Bagdrop-HostSetup/"#Where the cloned repo needs to go

def cloneRepo():
    """
    pull the most recent data from the repo if the destination isn't updated.
    call the git commands from a subprocess shell command line
    """
    try:
        mod_logger.info("Attempting to clone to Bagdrop")
        os.chdir(os.path.abspath(bagdrop))#change directory to bagdrop
        p = subprocess.Popen(shlex.split("git clean -fd "), stdout=subprocess.PIPE, stderr=subprocess.PIPE) #clean out any changes in bagdrop
        p = subprocess.Popen(shlex.split("git pull {} ".format(repo_URL)), stdout=subprocess.PIPE, stderr=subprocess.PIPE)#update the repo if outdated
    except Exception as ex: 
        mod_logger.error("Cloning failed with Exception: {}".format(ex))
        sys.exit(1)
    else:
        mod_logger.info("Repo cloned to Bagdrop")

def main():
    """
    setup the mod logger and start the process of pulling data from the repo.
    once up to date, the copying script is called to copy all files into their respective destinations
    """
    #Logger setup
    global mod_logger
    mod_logger = logging.getLogger(__name__)
    log.main(mod_logger)
    mod_logger.info("Starting clone")
    #Moving git repo files to bagdrop
    cloneRepo()
    copying.main()#call the copying script

if __name__ == "__main__": 
    main()
    sys.exit(0)