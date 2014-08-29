# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import init
from jenkinsapi.api import Jenkins
from config import JENKINS_USER, JENKINS_PASSWORD, JENKINS_URL

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

def add_job(jobname, copy_from, **kw):
    init.logger.info('create %s job copy from %s with params %s' % (jobname, copy_from, kw))
    jk = get_jenkins_obj()
    new_job = jk.copy_job(copy_from, jobname)
    soup = BeautifulSoup(new_job.get_config(), 'xml')
    for k in kw.keys():
        updater = JOB_SOUP_UPDATE_DICT.get(str(k).upper(), None)
        if updater:
            soup = updater(soup, kw[k])
    try:
        new_job.update_config(str(soup))
        new_job.enable()
    except Exception:
        init.logger.info('update job config failed: %s' % (new_job.id()))
    return jobname

def get_all_job_list():
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
    portlist = (get_port(job) for job in joblist)
    portlist = (int(port) for port in portlist if port.isdigit())
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
    #TODO 这里的jk没用上？
    jk = get_jenkins_obj()
    joblist = get_all_job_list()
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

def get_markdown_badge_status(job_name):
    job_url = "%s/job/%s/" % (JENKINS_URL, job_name)
    return "[![Build Status](%sbadge/icon)](%s)" % (job_url, job_url)

def update_soup_desc(soup, desc):
    soup.description.string = desc
    return soup

def update_soup_svn(soup, repo):
    soup.project.scm.remote.string = repo
    return soup

def update_soup_git_repo(soup, repo):
    soup.scm.userRemoteConfigs.url.string = repo
    return soup

def update_soup_git_branch(soup, branch):
    soup.scm.branches.find(name='name').string = branch
    return soup

def update_soup_shell(soup, shell):
    soup.find_all('command')[-1].string = shell
    return soup

def update_soup_email(soup, email):
    soup.publishers.find(name='hudson.tasks.Mailer').recipients.string = email
    return soup

JOB_SOUP_UPDATE_DICT = {
        'DESC': update_soup_desc,
        'SVN': update_soup_svn,
        'GITREPO': update_soup_git_repo,
        'GITBRANCH': update_soup_git_branch,
        'SHELL': update_soup_shell,
        'EMAIL': update_soup_email,
        }

