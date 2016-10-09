#!/usr/bin/ python

import requests
from os.path import join
import json

print "Just combine both list of repos and local paths"

username="wakaru44"
site="github.com" # could be github.com or bitbucket.com
base_location="~/workspace/src/{SITE}/{USER}".format(SITE=site,USER=username)



def old_combine():
    with open(".ansible/{0}.github.com.repos".format(username)) as f1:
        localpaths =".ansible/{0}.github.com.localpath".format(username) 
        with open(localpaths) as f2:
            def listero(repo,local):
                print """      - {{ "repo": "{0}",
                "dest": "{1}" }},""".format(repo.strip(" \n\t\"") ,local.strip(" \n\t\""))
                return (repo,local)
            map(listero,f1.readlines(), f2.readlines() )


def get_repo_list(login=username, site=site):
    """ obtain the updated list of
    public repos from the site for that user"""
    def boom():
        raise NotImplementedError

    apis = { "github.com": "https://api.github.com/users/{0}/repos",
            "bitbucket.com": boom
            }
    # get metadata about the user's repos
    uri  = apis[site].format(login)
    c = requests.get(uri)
    # parse the json and get only the clone_url for the repos
    js = json.loads(c.content)
    # in the shape of a tuple with name and clone_url
    repos = map(lambda x: ( x["name"], x["clone_url"] ), js)
    return repos


def compose_localpath(repo=None,base_location=base_location):
    """
    receive a tuple with the name of the repo and the clone_url,
    returns a dictionary with the pair (url,local path) 
    """
    assert repo is not None
    output =  """      - {{ "repo": "{0}",
                "dest": "{1}" }},""".format(repo[1], join(base_location,repo[0]))
    return output



if __name__=="__main__":
    repo_list = get_repo_list()
    print "\n".join(map(compose_localpath, repo_list))


