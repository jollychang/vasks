# -*- coding: utf-8 -*-
import init
from config import CODE_PR_DESC_TEMPLATE, JENKINS_URL
from libs.jenkins import get_avaliable_port, add_job, get_markdown_badge_status

def create_opening_pr_job(repo, number_of_pr, clone_url_of_pr, branch_of_pr, email_of_pr, job_template_name):
    init.logger.info('%s: create suite job for pr %s' % (repo, number_of_pr))
    t_job_name = job_template_name
    ####port
    port = get_avaliable_port()
    ####job name
    job_name = "%s-opening-pr-%s-suite-%s" % (repo, number_of_pr, port)
    ####job creation
    params = {}
    params['DESC'] = CODE_PR_DESC_TEMPLATE % (repo, number_of_pr, repo, number_of_pr)
    params['GITREPO'] = clone_url_of_pr
    params['GITBRANCH'] = "origin/%s" % branch_of_pr
    params['EMAIL'] = email_of_pr
    add_job(job_name, t_job_name, **params)
    return job_name

def create_ci_suite_for_git_pr(repo, pr_info_dict, job_template_name):
    ##== data prepare ==
    number_of_pr = pr_info_dict['number']
    clone_url_of_pr = pr_info_dict['repo_url']
    branch_of_pr = pr_info_dict['branch']
    email_prefix = pr_info_dict['email_prefix']
    email_of_pr = "%s@douban.com" % (email_prefix)
    job_name = create_opening_pr_job(repo, number_of_pr, clone_url_of_pr, branch_of_pr,email_of_pr, job_template_name)
    init.logger.info("jobname: %s/job/%s" % (JENKINS_URL, job_name))
    comment = "suite : %s" % (get_markdown_badge_status(job_name),)
    return comment

