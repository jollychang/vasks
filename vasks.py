#!/usr/bin/env python
# -*- coding: utf-8 -*-
from optparse import OptionParser
from jenkins import get_scm_dict_by_view, add_jobs, delete_jobs_by_view_url, add_all_in_one_job
from svn import get_svn_branches_list
from config import VIEW_URL
import init


def create_job():
    svnmap = get_svn_branches_list()
    init.logger.info("svn dict: %s", svnmap) 
    if len(svnmap) > 0:
        cimap = get_scm_dict_by_view(VIEW_URL)
        init.logger.info("jenkins scm dict: %s" % (cimap))
        cilist = list(set(cimap.itervalues()))
        init.logger.info("jenkins scm list: %s" % (cilist))
        for k in svnmap.iterkeys():
            if k in cilist:
                init.logger.info('%s is jenkins job     ' % k)
            else:
                email = svnmap[k]
                add_all_in_one_job(k, email)
                init.logger.info('creat jobs for %s' % k)
    else:
        init.logger.info('there is no new commit for branches') 

def main():
    parse = OptionParser(description='auto fetch svn branch and assign jenkins job\n http://code.dapps.douban.com/Vasks')
    parse.add_option('-c', '--create-job', action='store_true', help='create jobs')
    parse.add_option('-d', '--delete-jobs-by-view-url', action='store_true', help='delete all jobs in view')
    parse.add_option('-a', '--add-jobs-by-svn-email', action='store_true', help='add jobs by svn and email')
    parse.add_option('-s', '--svn-url', type='string', help='svn url')
    parse.add_option('-e', '--email', type='string', help='email for notification')
    parse.add_option('-v', '--view', type='string',default=VIEW_URL, help='view url')
    options, args = parse.parse_args()
    if options.delete_jobs_by_view_url:
        init.logger.info('delete job in view: %s', options)
        delete_jobs_by_view_url(options.view)
    elif options.add_jobs_by_svn_email:
        if options.svn_url and options.email:
            add_jobs(options.svn_url, options.email)
        else:
            init.logger.info('add jobs need svn url and email both')
    else:
        create_job()
        init.logger.info('create jobs finish!')

if __name__ == '__main__':
    main()
