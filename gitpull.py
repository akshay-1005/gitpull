#!/usr/bin/env python
# coding: utf-8

#! pip install GitPython

import os
import requests
import git
import hmac
import hashlib
import json
from flask import Flask, request, abort
from git.exc import InvalidGitRepositoryError, NoSuchPathError, GitCommandError

app = Flask(__name__)

username = os.environ['USERNAME']
genius_token = ['GENIUS']
#passwd = os.environ['PASSWD']
#w_secret = os.environ['WEBHOOK_SECRET']
#gh_token = os.environ['GH_TOKEN']



@app.route('/webhook', methods=['POST', 'GET', 'PULL'])

def webhook():

     
     print(os.getcwd())

     if request.method == 'POST':
        
        abort_code = 418
        # Do initial validations on required headers
        if 'X-Github-Event' not in request.headers:
            abort(abort_code)

        if 'X-Github-Delivery' not in request.headers:
            abort(abort_code)

        if 'X-Hub-Signature' not in request.headers:
            abort(abort_code)

        if not request.is_json:
            abort(abort_code)

        if 'User-Agent' not in request.headers:
            abort(abort_code)

        ua = request.headers.get('User-Agent')
        if not ua.startswith('GitHub-Hookshot/'):
            abort(abort_code)

        event = request.headers.get('X-GitHub-Event')
        if event == "ping":
            return json.dumps({'msg': 'Hi!'})

        if event != "push":
            return json.dumps({'msg': "Wrong event type"})

        x_hub_signature = request.headers.get('X-Hub-Signature')
        # webhook content type should be application/json for request.data to have the payload
        # request.data is empty in case of x-www-form-urlencoded
        # if not is_valid_signature(x_hub_signature, request.data, w_secret):
        #     print('Deploy signature failed: {sig}'.format(sig = x_hub_signature))
        #     abort(abort_code)

        payload = request.get_json()
        if payload is None:
            print('Deploy payload is empty: {payload}'.format(
                payload=payload))
            abort(abort_code)

        if payload['ref'] != 'refs/heads/master':
            return json.dumps({'msg': 'Not master; ignoring'})

        repo = git.Repo("https://github.com/akshay-1005/bag-boost.git")
        origin = repo.remotes.origin
        origin.pull()
        print(os.getcwd())
        print("++++")
        return 'Code pulled and updated', 200

     else:
        return 'No new commit made', 400

    # if len(pull_info) == 0:
    #      return json.dumps({'msg': "Didn't pull any information from remote!"})
    #  if pull_info[0].flags > 128:
    #      return json.dumps({'msg': "Didn't pull any information from remote!"})
    
    #  commit_hash = pull_info[0].commit.hexsha
    #  build_commit = f'build_commit = "{commit_hash}"'
    #  print(f'{build_commit}')
    #  return 'Updated server to commit {commit}'.format(commit = commit_hash)


if __name__ == '__main__':
    app.run()
