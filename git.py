#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import json
import init

from config import GITHUB_API_BASE_URL, GITHUB_USER, GITHUB_PASSWORD

def get_opening_pull_request_info_list(owner, repo):
    repo_url = GITHUB_API_BASE_URL + '/repos/%s/%s' % (owner, repo)
    open_pulls_url = repo_url + '/pulls'
    r = requests.get(open_pulls_url)
    if r.status_code != 200:
        return None
    return [_pr_json_to_info_dict(p) for p in r.json]

def get_info_dict_of_pull_request(owner, repo, pid):
    repo_url = GITHUB_API_BASE_URL + '/repos/%s/%s' % (owner, repo)
    pull_url = repo_url + '/pulls/%s' % (pid)
    r = requests.get(pull_url)
    if r.status_code != 200:
        return None
    return _pr_json_to_info_dict(r.json)

def _pr_json_to_info_dict(json):
    info_dict = {}
    info_dict['number'] = json['number']
    info_dict['repo_url'] = json['head']['repo']['clone_url']
    info_dict['branch'] = json['head']['ref']
    info_dict['email_prefix'] = json['head']['repo']['owner']['login']
    info_dict['state'] = json['state']
    return info_dict

def _get_access_token():
    r = requests.get(GITHUB_API_BASE_URL+'/authorizations', auth=(GITHUB_USER, GITHUB_PASSWORD))
    if r.status_code != 200:
        return None
    repo_token_list = [t['token'] for t in r.json if u'repo' in t['scopes']]
    if len(repo_token_list) > 0:
        return repo_token_list[0]
    r = requests.post(GITHUB_API_BASE_URL+'/authorizations', data='{"scopes":["repo"]}',auth=(GITHUB_USER, GITHUB_PASSWORD))
    if r.status_code != 201:
        return None
    return r.json['token']

def comment_on_pull_request(owner, repo, number_of_pr, comment):
    token = _get_access_token()
    if token is None:
        init.logger.info('cant get access_token. comment on %s/%s/pulls/%s failed' % (owner, repo, number_of_pr))
        return None
    headers = {'Authorization': 'Bearer %s' % token}
    payload = json.dumps({"body": comment})
    r = requests.post('%s/repos/%s/%s/issues/%s/comments' % (GITHUB_API_BASE_URL, owner, repo, number_of_pr), headers=headers, data=payload)
    if r.status_code != 201:
        return None
    return r.json['id']

