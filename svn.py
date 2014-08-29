#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re, sys, subprocess
from os.path import join
import init

revision_file = join(init.INITPATH, 'revision.txt')
from config import SVN_ROOT_URL

def run_command(cmd):
    p = subprocess.Popen('cd %s; %s' % (init.VASKSPATH, cmd), shell=True,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return p.communicate()

def get_branch_url_by_file_list(text, depth=3):
    if 'branches' in text:
        m = re.search('/branches(/.*?){%s}' % depth, text)
        if m is not None:
            branch = m.group(0)
            branch_url = "%s%s" % (SVN_ROOT_URL, branch)
            return branch_url
        else:
            return 'create/delete branch not need run'
    else:
        return 'trunk not need run'


def get_branch_url_from_svn(text):
    for d in range(2, 7):
        branch_url = get_branch_url_by_file_list(text, d)
        if 'http' in branch_url and 'non-existent' not in check_shire(branch_url):
            return branch_url
    return 'non-existent shire branch'

def get_last_committer(branch_url):
    cmd = "svn info %s | grep 'Last Changed Author:' | awk '{ print $4 }'" % branch_url
    stdout, stderr = run_command(cmd)
    return stdout.strip()

def check_shire(branch_url):
    cmd = "svn list %s/info.txt" % branch_url
    stdout, stderr = run_command(cmd)
    return stderr.strip()

def remove_no_shire_branch_from_dict(dict):
    for k in dict.keys():
        if 'non-existent' in check_shire(k):
            del dict[k]
    return dict

def get_branch_by_svn_log(LastRevision, OldRevision):
    cmd = "svn log -r %s:%s  %s/branches/ -v | grep '   ' | awk '{print $2}'" % (LastRevision, OldRevision, SVN_ROOT_URL)
    stdout, stderr = run_command(cmd)
    svn_log_summarize = stdout.strip()
    return svn_log_summarize

def get_branch_dict_from_svn_log(LastRevision, OldRevision):
    svn_log_summarize = get_branch_by_svn_log(LastRevision, OldRevision)
    dict = {}
    for line in svn_log_summarize.split('\n'):
        line = "%s%s" % (SVN_ROOT_URL, line)
        if not text_in_dict(line, dict):
            text = get_branch_url_from_svn(line)
            committer = get_last_committer(text)
            email = "%s@douban.com" % committer
            if 'http' in text:
                dict[text] = email
    return dict 

def text_in_dict(text, dict):
    for k in dict.keys():
        if k in text:
            return True
    return False    

def get_svn_branches_list():
    old = get_old_revision().strip()
    last = get_last_revision()
    dict = {}
    if last>old:
        dict = get_branch_dict_from_svn_log(last, old)
    else:
        pass
    return dict

def get_last_revision():
    cmd = "svn info %s/branches | awk '/Revision:/ { print $2 }'" % SVN_ROOT_URL
    stdout, stderr = run_command(cmd)
    revision = stdout.strip()   
    try:
        f = open(revision_file, 'w')
    except IOError:
        print 'cannot write %s' % revision_file 
    else:
        f.write(revision)  
        f.close()
    return revision

def get_old_revision():
    try:
        f = open(revision_file, 'r')
    except IOError:
        print "cannot open %s" % revision_file
        revision = get_last_revision()
    else:
        revision = f.read().strip()
        f.close()
    return revision

def svn_log_today():
    import datetime
    today = datetime.date.today()
    tomorrow = today + datetime.timedelta(days=1)
    cmd = "svn log %s/branches -r {%s}:{%s} -v |grep '   ' |awk '{print $2}'" % (SVN_ROOT_URL, today, tomorrow)
    stdout, stderr = run_command(cmd)
    print stdout
