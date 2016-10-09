#!/bin/bash

echo "List all the repos by one user"

USER="wakaru44"
SITE="github.com"
BASELOCATION="/home/ubuntu/workspace/src/${SITE}/${USER}"

echo "The current user is ${SITE}/$USER"

# beware the url is kept to plaintext and not var because this should be a github specifiq thing.
# First, get the repos from github and put the list in a file
curl https://api.github.com/users/${USER}/repos | jq ".[]?.clone_url"
curl https://api.github.com/users/${USER}/repos | jq ".[]?.clone_url" > .ansible/${USER}.${SITE}.repos

# Then, use that file to get the locations where you are going to put those files
for url in $(cat .ansible/${USER}.${SITE}.repos ); do echo "\"${BASELOCATION}/$(basename $url | sed 's/\.git\"//g')\"" ; done > .ansible/${USER}.${SITE}.localpath

# and finally, I guess we will be
#    - putting all that together in a yaml like file???
#    - or consume this from ansible?
#    - or what?


echo "I have created this two files for you to create the task in yaml"
ls .ansible/${USER}*
