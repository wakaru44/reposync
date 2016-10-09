#!/usr/bin/ python

import requests
from os.path import join,isdir,expanduser
from os import makedirs
import os
import sys
import json
import logging
import subprocess

import argparse
import settings

"""
Repo Sync.

Clone all your repos from github and/or bitbucket.
"""

command_parser = argparse.ArgumentParser(
        description = "clone repos from public git accounts"
        )

command_parser.add_argument("-s","--settings", dest="settingsfile", help="alternative settings", required=False)
command_parser.add_argument("-v","--verbose", action="store_true", help="extra logging", required=False, default=False)

class cd:
    """Context manager for changing the current working directory"""
    def __init__(self, newPath):
        self.newPath = os.path.expanduser(newPath)

    def __enter__(self):
        self.savedPath = os.getcwd()
        os.chdir(self.newPath)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.savedPath)

def define_path(base_path, account):
    """extract the username and site details from the account
    and build the full path to be created
    """
    assert base_path is not ""
    assert account is not ""
    return join(expanduser(base_path), account)


def create_folders(base_path, account):
    """create a working folder structure based on the account"""
    wanted_path = define_path(base_path, account)
    logging.debug(wanted_path)
    try:
        makedirs(wanted_path)
        logging.info("Created working folder on {0}".format(wanted_path))
        return True
    except OSError as e:
        if e.errno is 17:
            logging.info( wanted_path + " " +  e.strerror)
            return True
        else:
            logging.error( wanted_path + " " +  e.strerror)
            return False


def get_repos(account, sites_override=None):
    """given a short code for an account, get the list of repos"""
    # parse the account to find the site
    site, username = account.split("/")
    # forward the query to the right method
    sites = sites_override or {"github.com": get_repos_github,
            "bitbucket.com": get_repos_bitbucket
            } 
    try:
        logging.info("getting repos for {0}".format(account))
        return sites[site](username)
    except KeyError:
        logging.error("site not found ({0})".format(account))
        logging.debug("in  ({0})".format(sites))
        return None


def get_repos_bitbucket(username):
    """Get the public repos of this guy"""
    assert username is not ""
    logging.debug("Getting bitbucket repos for {0}".format(username))
    return "bitbucket {0}".format(username)


def get_repos_github(username):
    """Get the public repos of this guy"""
    logging.debug("Getting github repos for {0}".format(username))
    if username == "":
	logging.error("Sorry, '{0}' is not a real username".format(username))
	return None
    response = requests.get("https://api.github.com/users/{0}/repos".format(username)).json()
    urls = [x["clone_url"] for x in response ] # jq filter = "[]?.clone_url"
    return urls


def extract_repo_name(repo):
    """ get the name out of the url of the repo
    """
    result = repo.split("/")[-1][:-4] #Dirty. but works
    logging.debug("The name of the repo is {0}".format(result))
    if result is not "":
        return result 
    else:
        raise TypeError("The repo {0} is bullshit".format(repo))


def clone_repo(base_path, repo):
    """
    go to the base_path and clone the repo
    """
    with cd(base_path):
        output = do_call("git clone {0}".format(repo))
        if output == 1:
            logging.info("The repo exists")
        else:
            logging.erro("Fuck")
    return output



def do_call(command):
    """
    a nicer method to call subprocess.call
    """

    try:
        result = subprocess.check_output(command.split(" "), shell=True)
        return result
    except subprocess.CalledProcessError as e:
        return_code = e.returncode
        logging.error("failed to run '{0}'".format(command))
        logging.error(e)
        return return_code

if __name__=="__main__":
    # Load passed parameters
    args = vars(command_parser.parse_args())
    # configure logging
    if args["verbose"]:
        logger= logging.DEBUG
    else:
        logger = logging.INFO

    logging.basicConfig(stream=sys.stderr,
            level=logger,
            format="REPOSYNC %(levelname)s \t- %(message)s")
    logging.error("Not implemented")
    logging.info("This is a work in progress. Handle with care")
    logging.debug("Now is time to design the script a little bit")

    ################################################################################
    # Now do some stuff.

    # load the defined repos from somewhere, aka the settings file
    accounts = settings.accounts
    # then build the folder structure
    logging.info("""
    Creating Folder Structure
    =========================""")
    for acc in accounts:
        create_folders(settings.workspace, acc)
    # then go to each repo and find out the list
    repos = {}
    logging.info("""
    Retrieving list of repositories.
    ================================""")
    for acc in accounts:
        repos[acc] = get_repos(acc)
    logging.debug( repos)

    #TODO: write the method to take all the repos, go to the folder, check if is downloaded, and if not, clone it
    for acc in accounts:
        # go to define_path,
        for repo in repos[acc]:
            #  check if repo exists, 
            repo_name = extract_repo_name(repo)
            base_path = define_path(settings.workspace, acc) 
            logging.debug("base path {0}".format(base_path))
            repo_path = join(base_path,repo_name) 
            logging.debug("repo path {0}".format(repo_path))
            git_path = join(repo_path,".git/")
            logging.info("Git path {0}".format(git_path))
            if isdir(git_path):
                # and if it does, go on
                logging.info("'{0}' is already in '{1}'".format(repo_name, repo_path))
                break
            else:
                # if it doesnt exist, go there and clone
                logging.info("Clonning '{0}' in '{1}'".format(repo_name, repo_path))
                clone_repo(base_path, repo)

