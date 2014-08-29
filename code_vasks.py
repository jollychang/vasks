#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
所有code style的repo
'''
from optparse import OptionParser
import init
import re, sys
from libs.jenkins import get_job_name_list_from_view, delete_job
from libs.code import get_opening_pull_request_info_list, get_info_dict_of_pull_request, comment_on_pull_request
from model.code import create_ci_suite_for_git_pr


def create_jobs(repo, view_url, job_template_name):
    opr_list = get_opening_pull_request_info_list(repo)
    init.logger.info('opening PR  %s', ', '.join(str(e) for e in opr_list))
    job_name_list = get_job_name_list_from_view(view_url)
    pr_in_view = []
    for job_name in job_name_list:
        pr_number = _get_pr_id(job_name)
        pr_in_view.append(pr_number)
    init.logger.info('PR already in jenkins view %s', ', '.join(str(e) for e in pr_in_view))
    if not opr_list:
        init.logger.error('code repo is not reachable')
        return sys.exit(1)
    if opr_list == []:
        init.logger.info('no opening pull requests')
        return 0
    for opr in opr_list:
        if not int(opr['number']) in pr_in_view:
            comment = create_ci_suite_for_git_pr(repo, opr, job_template_name)
            init.logger.info('ci suite created for pr No.%s' % (opr['number']))


def delete_jobs(repo, view_url):
    job_name_list = get_job_name_list_from_view(view_url)
    for job_name in job_name_list:
        pr_number = _get_pr_id(job_name)
        pr_info = get_info_dict_of_pull_request(repo, pr_number)
        if pr_info['state'] == 'closed':
            init.logger.info('deleting job: %s of pr No.%s' % (job_name, pr_number))
            delete_job(job_name)

def _get_pr_id(jobname):
    m = re.match(r".*\-opening\-pr\-(\d+)\-.*", jobname)
    pr_id = int(m.group(1))
    return pr_id

def main():
    parse = OptionParser(description='auto fetch git opening pull requests and assign jenkins job')
    parse.add_option('-a', '--create-jobs', action='store_true', help='add jobs')
    parse.add_option('-d', '--delete-jobs', action='store_true', help='delete old jobs')
    parse.add_option('-r', '--repo', type='string', help='repo name, such as fm')
    parse.add_option('-v', '--view-url', type='string', help='view url')
    parse.add_option('-t', '--job-template-name', type='string', help='job template name')
    options, args = parse.parse_args()
    if options.delete_jobs:
        init.logger.info('delete jobs start!')
        delete_jobs(options.repo, options.view_url)
        init.logger.info('delete jobs finish!')
    if options.create_jobs:
        init.logger.info('create jobs start!')
        create_jobs(options.repo, options.view_url, options.job_template_name)
        init.logger.info('create jobs finish!')

if __name__ == '__main__':
    main()
