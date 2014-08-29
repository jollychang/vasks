from jenkinsapi.api import Jenkins
from config import JENKINS_USER, JENKINS_PASSWORD, JENKINS_URL, job_template_dict, VIEW_URL, ark_job_template_dict, ARK_OPENING_PR_VIEW_URL
from bs4 import BeautifulSoup
import re
import init

def get_jenkins_obj(url=JENKINS_URL, jenkins_user=JENKINS_USER, jenkins_password=JENKINS_PASSWORD):
    return Jenkins(url, jenkins_user, jenkins_password)

def get_scm_dict_by_view(view_url):
    jk = get_jenkins_obj()
    view = jk.get_view_by_url(view_url)
    jobsmap =  view.get_job_dict()
    job_scm_dict = {}
    for k in jobsmap.iterkeys():
        job = jk.get_job(k)
        scm = job.get_vcs_url()
        job_scm_dict[job.name] = scm
    return job_scm_dict

def add_jobs(scm, email):
    for t in job_template_dict.iterkeys():
        jobname_base = get_jobname_from_branch_url(scm)
        jobname = add_job(jobname_base, t, scm, email)
        init.logger.info('build job: %s' % (jobname))
        jk = get_jenkins_obj()
        job = jk.get_job(jobname)
        job.enable()
        #job.invoke()

def add_all_in_one_job(scm, email):
    jobname_base = get_jobname_from_branch_url(scm)

    init.logger.info('create pylint-unittest-webtest-all-in-one job for %s' % scm)    
    port = str(get_avaliable_port())    
    jobname = '%s-pylint-unittest-webtest-all-in-one-%s' % (jobname_base, port)
    jk = get_jenkins_obj()
    new_job = jk.copy_job(job_template_dict['all-in-one'], jobname)
    replace_job_svn(new_job.name, scm)
    update_email(new_job.name, email)

    init.logger.info('build job: %s' % (jobname))
    jk = get_jenkins_obj()
    job = jk.get_job(jobname)
    job.enable()
    #job.invoke()

def add_job(jobname, testtype, scm, email):
    init.logger.info('create %s job for %s' % (testtype, scm))
    if testtype == 'pylint':
        port = ''
    else:
        port = '-' + str(get_avaliable_port())
    jobname = '%s-%s%s' % (jobname, testtype, port)
    jk = get_jenkins_obj()
    new_job = jk.copy_job(job_template_dict[testtype], jobname)
    replace_job_svn(new_job.name, scm)
    update_email(new_job.name, email)
    return jobname

def get_jobname_from_branch_url(scm):
    m = re.search('branches(/.*).*', scm)
    name = m.group(0)
    name = name.replace('/', '-')
    return name

def get_job_list():
    jk = get_jenkins_obj()
    jobs = []
    for job in jk._data['jobs']:
        jobs.append(job['name'])
    return list(set(jobs))

def get_port(jobname):
    lastname = jobname.split('-')[-1]
    if lastname.isdigit():
        return lastname
    else:
        return 'lastname is not port number'

def get_port_list(joblist):
    portlist = []
    for job in joblist:
        port = get_port(job)
        if port.isdigit():
            portlist.append(int(port))
    return list(set(portlist))

def format_port_list(portlist):
    format_portlist = []
    for port in portlist:
        if port%10 ==0:
            format_portlist.append(port)
    portlist = list(set(format_portlist))
    portlist.sort()
    return portlist

def reuse_port(portlist):
    for current, last in zip(portlist[1:], portlist):
        diff = current - last
        if diff != 10:
            port = last + 10
            return port
        else:
            pass
    return 'no port can be reuse,you need a new port'

def get_avaliable_port():
    jk = get_jenkins_obj()
    joblist = get_job_list()
    init.logger.debug('job list : %s' % joblist)
    pl = get_port_list(joblist)
    init.logger.debug('port list : %s' % pl)
    portlist = format_port_list(pl)
    init.logger.debug('format port list : %s' % portlist)
    rp = reuse_port(portlist)
    if isinstance(rp, int):
        return str(rp)
    else:
        max_port = max(portlist)
        avaliable_port = int(max_port) + 10
    return avaliable_port

def replace_job_svn(jobname, scm_url):
    init.logger.info('update job:%s svn %s' % (jobname, scm_url))
    jk = get_jenkins_obj()
    job = jk.get_job(jobname)
    config = job.get_config()

    vcs = job.get_vcs()
    name = dict(svn='remote', git='url', hg='source').get(vcs)
    if not name:
        return 'scm are not hg/git/svn'
    soup = BeautifulSoup(config, 'xml')
    node = soup.project.scm.find(name)
    node.string = scm_url
    new_config = str(soup)

    try:
        job.update_config(new_config)
        return "update scm successful"
    except Exception, e:
        return "update scm failed"

def update_email(jobname, email):
    init.logger.info('update job: %s email: %s' % (jobname, email))
    jk = get_jenkins_obj()
    job = jk.get_job(jobname)
    config = job.get_config()
    soup = BeautifulSoup(config, 'xml')
    emailnode = soup.project.find('recipients')
    if emailnode:
        emailnode.string = email
    new_config = str(soup)

    try:
        job.update_config(new_config)
        return "update email successful"
    except Exception, e:
        return "update email failed"

def delete_jobs_by_view_url(view_url):
    jk = get_jenkins_obj()
    v = jk.get_view_by_url(view_url)
    jobs = v.get_job_dict().keys()
    for job in jobs:
        jk.delete_job(job)
    message = "view: %s and jobs: %s delete successful" % (view_url, (", ".join(jobs)))
    init.logger.info(message)

def delete_job(job_name):
    jk = get_jenkins_obj()
    jk.delete_job(job_name)

def get_job_name_list_from_view(view_url):
    jk = get_jenkins_obj()
    v = jk.get_view_by_url(view_url)
    job_name_list = v.get_job_dict().keys()
    return job_name_list

def _gen_markdown_badge_status(job_name):
    job_url = "%s/job/%s/" % (JENKINS_URL, job_name)
    return "[![Build Status](%sbadge/icon)](%s)" % (job_url, job_url)

def create_ci_suite_for_git_pr(pr_info_dict):
    ##== data prepare ==
    number_of_pr = pr_info_dict['number']
    clone_url_of_pr = pr_info_dict['repo_url']
    branch_of_pr = pr_info_dict['branch']
    email_prefix = pr_info_dict['email_prefix']
    email_of_pr = "%s@douban.com" % (email_prefix)
    ut_job_name = create_ark_opening_pr_ut_job_pair(number_of_pr, clone_url_of_pr, branch_of_pr, email_of_pr)
    wd_job_name = create_ark_opening_pr_wd_job_pair(number_of_pr, clone_url_of_pr, branch_of_pr, email_of_pr)
    comment = "unittest : %s\n\nwebdriver : %s" % (_gen_markdown_badge_status(ut_job_name), _gen_markdown_badge_status(wd_job_name))
    return comment

def update_soup_desc(soup, desc):
    soup.description.string = desc
    return soup

def update_soup_git(soup, repo, branch):
    soup.scm.userRemoteConfigs.url.string = repo
    soup.scm.branches.find(name='name').string = branch
    return soup

def update_soup_shell(soup, shell):
    soup.command.string = shell
    return soup

def update_soup_email(soup, email):
    soup.publishers.find(name='hudson.tasks.Mailer').recipients.string = email
    return soup

JOB_SOUP_UPDATE_DICT = {
        'DESC': update_soup_desc,
        'GIT': update_soup_git,
        'SHELL': update_soup_shell,
        'EMAIL': update_soup_email,
        }

def create_ark_opening_pr_ut_job_pair(number_of_pr, clone_url_of_pr, branch_of_pr, email_of_pr):
    shire_t_job_name = ark_job_template_dict['shire']
    ut_t_job_name = ark_job_template_dict['unittest']
    ##== fake shire for ut ==
    ####port
    ut_shire_port = get_avaliable_port()
    ####job name
    ut_shire_name = "ark-opening-pr-%s-fake-shire-for-ut-%s" % (number_of_pr, ut_shire_port)
    ####job creation
    ut_shire_job = get_jenkins_obj().copy_job(shire_t_job_name, ut_shire_name)
    ##== ut ==
    ####port
    ut_port = get_avaliable_port()
    ####job name
    ut_job_name = "ark-opening-pr-%s-ut-%s" % (number_of_pr, ut_port)
    ####job creation
    ut_job = get_jenkins_obj().copy_job(ut_t_job_name, ut_job_name)
    ut_soup = BeautifulSoup(ut_job.get_config(), 'xml')
    ####git repo/branch
    ut_soup = JOB_SOUP_UPDATE_DICT['GIT'](ut_soup, clone_url_of_pr, branch_of_pr)
    ####shell(port/domain)
    ut_soup = JOB_SOUP_UPDATE_DICT['SHELL'](ut_soup, u'BUILD_ID=dontkillme_$JOB_NAME\nbash tools/ci-scripts/unittest.sh -a %s -s %s -d localhost' % (ut_port, ut_shire_port))
    ####email
    ut_soup = JOB_SOUP_UPDATE_DICT['EMAIL'](ut_soup, email_of_pr)
    ####config update
    try:
        ut_job.update_config(str(ut_soup))
        ut_job.enable()
    except Exception:
        init.logger.info('update job config failed: %s' % (ut_job.id()))
    return ut_job.id()

def create_ark_opening_pr_wd_job_pair(number_of_pr, clone_url_of_pr, branch_of_pr, email_of_pr):
    shire_t_job_name = ark_job_template_dict['shire']
    wd_t_job_name = ark_job_template_dict['webdriver']
    ##== fake shire for wd ==
    ####port
    wd_shire_port = get_avaliable_port()
    ####job name
    wd_shire_name = "ark-opening-pr-%s-fake-shire-for-wd-%s" % (number_of_pr, wd_shire_port)
    ####job creation
    wd_shire_job = get_jenkins_obj().copy_job(shire_t_job_name, wd_shire_name)
    ##== wd ==
    ####port
    wd_port = get_avaliable_port()
    ####job name
    wd_job_name = "ark-opening-pr-%s-wd-%s" % (number_of_pr, wd_port)
    ####job creation
    wd_job = get_jenkins_obj().copy_job(wd_t_job_name, wd_job_name)
    wd_soup = BeautifulSoup(wd_job.get_config(), 'xml')
    ####git repo/branch
    wd_soup = JOB_SOUP_UPDATE_DICT['GIT'](wd_soup, clone_url_of_pr, branch_of_pr)
    ####shell(port/domain)
    wd_soup = JOB_SOUP_UPDATE_DICT['SHELL'](wd_soup, u'BUILD_ID=dontkillme_$JOB_NAME\nhname=`hostname`\nok=`echo $hname | grep ".*\\.intra\\.douban\\.com" | wc -l`\nif [ $ok -eq 1 ]; then\n  domain=$hname\nelse\n  domain="$hname.intra.douban.com"\nfi\n\nbash tools/ci-scripts/webdriver.sh -a %s -s %s -d $domain' % (wd_port, wd_shire_port))
    ####email
    wd_soup = JOB_SOUP_UPDATE_DICT['EMAIL'](wd_soup, email_of_pr)
    ####config update
    try:
        wd_job.update_config(str(wd_soup))
        wd_job.enable()
    except Exception:
        init.logger.info('update job config failed: %s' % (wd_job.id()))
    return wd_job.id()

