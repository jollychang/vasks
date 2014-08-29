# coding: utf-8

from optparse import OptionParser
import init
from libs.jenkins import get_job_name_list_from_view, delete_job
from libs.code import get_opening_pull_request_info_list, get_info_dict_of_pull_request
from model.ark_code import create_ci_suite_for_git_pr
from config import ARK_OPENING_PR_VIEW_URL


def create_jobs(repo, view_url):
    opr_list = get_opening_pull_request_info_list(repo)
    job_name_list = get_job_name_list_from_view(view_url)
    pr_in_view = [job_name.split('-')[3] for job_name in job_name_list]
    if opr_list is False:
        init.logger.info('github repo is not reachable')
        return None
    if opr_list == []:
        init.logger.info('no opening pull requests')
        return 0
    for opr in opr_list:
        if not str(opr['number']) in pr_in_view:
            print opr
            comment = create_ci_suite_for_git_pr(opr)
            #comment_on_pull_request(owner, repo, opr['number'], comment)
            init.logger.info('ci suite created for pr No.%s' % (opr['number']))


def delete_jobs(repo, view_url):
    job_name_list = get_job_name_list_from_view(view_url)
    for job_name in job_name_list:
        pr_number = int(job_name.split('-')[3])
        pr_info = get_info_dict_of_pull_request(repo, pr_number)
        if pr_info['state'] == 'closed':
            init.logger.info('deleting job: %s of pr No.%s' % (job_name, pr_number))
            delete_job(job_name)


def main():
    parse = OptionParser(description='auto fetch git opening pull requests and assign jenkins job')
    parse.add_option('-a', '--create-jobs', action='store_true', help='add jobs')
    parse.add_option('-d', '--delete-jobs', action='store_true', help='delete old jobs')
    parse.add_option('-v', '--view-url', type='string', help='view url')
    options, args = parse.parse_args()
    view_url = options.view_url or ARK_OPENING_PR_VIEW_URL
    if options.delete_jobs:
        init.logger.info('delete jobs start!')
        delete_jobs('ark', view_url)
        init.logger.info('delete jobs finish!')
    if options.create_jobs:
        init.logger.info('create jobs start!')
        create_jobs('ark', view_url)
        init.logger.info('create jobs finish!')

if __name__ == '__main__':
    main()

