# coding: utf-8
import init
from config import CODE_PR_DESC_TEMPLATE
from config import ark_job_template_dict, ark_job_shell_template_dict
from libs.jenkins import get_avaliable_port, add_job, get_markdown_badge_status


def create_ark_opening_pr_job_pair(number_of_pr, clone_url_of_pr, branch_of_pr, email_of_pr, job_type, shell_template):
    init.logger.info('ark: create %s job for pr %s' % (job_type, number_of_pr))
    shire_t_job_name = ark_job_template_dict['shire']
    t_job_name = ark_job_template_dict[job_type]
    shire_port = get_avaliable_port()
    shire_name = "ark-open-pr-%s-fake-shire-for-%s-%s" % (number_of_pr, job_type ,shire_port)
    add_job(shire_name, shire_t_job_name)
    port = get_avaliable_port()
    job_name = "ark-open-pr-%s-%s-%s" % (number_of_pr, job_type ,port)
    params = {}
    params['DESC'] = CODE_PR_DESC_TEMPLATE % ('ark', number_of_pr, 'ark', number_of_pr)
    params['GITREPO'] = clone_url_of_pr
    params['GITBRANCH'] = "origin/%s" % branch_of_pr
    params['SHELL'] = shell_template % (port, shire_port)
    params['EMAIL'] = email_of_pr
    add_job(job_name, t_job_name, **params)
    return job_name

def create_ci_suite_for_git_pr(pr_info_dict):
    ##== data prepare ==
    number_of_pr = pr_info_dict['number']
    clone_url_of_pr = pr_info_dict['repo_url']
    branch_of_pr = pr_info_dict['branch']
    email_prefix = pr_info_dict['email_prefix']
    email_of_pr = "%s@douban.com" % (email_prefix)
    job_name = create_ark_opening_pr_job_pair(number_of_pr, clone_url_of_pr, branch_of_pr, email_of_pr, 'suite', ark_job_shell_template_dict['suite'])
    comment = "suite: %s" % (get_markdown_badge_status(job_name,))
    return comment

