# -*- coding: utf-8 -*-
import requests
import json
import init
from config import CODE_API_BASE_URL


def get_opening_pull_request_info_list(repo):
    repo_url = CODE_API_BASE_URL + '/%s' % (repo,)
    open_pulls_url = repo_url + '/pulls'
    r = requests.get(open_pulls_url)
    if r.status_code != 200:
        return None
    return [_pr_json_to_info_dict(p) for p in r.json]

def get_info_dict_of_pull_request(repo, pid):
    repo_url = CODE_API_BASE_URL + '/%s' % (repo,)
    pull_url = repo_url + '/pull/%s' % (pid,)
    r = requests.get(pull_url)
    if r.status_code != 200:
        return None
    return _pr_json_to_info_dict(r.json)

def _pr_json_to_info_dict(json):
    init.logger.debug('pull request json: %s' % json)
    info_dict = {}
    info_dict['number'] = json['number']
    info_dict['repo_url'] = json['head']['repo']['clone_url']
    info_dict['branch'] = json['head']['ref']
    info_dict['email_prefix'] = json['head']['repo']['author']['login']
    info_dict['state'] = json['state']
    return info_dict

def comment_on_pull_request(repo, number_of_pr, comment):
    payload = {"content": comment}
    r = requests.post('%s/%s/pull/%s/comments' % (CODE_API_BASE_URL, repo, number_of_pr), data=payload)
    if r.status_code != 201:
        return None
    return r.json['id']
