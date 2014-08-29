# -*- coding: utf-8 -*-
###jenkins
JENKINS_URL = 'http://YOURJENKINSURL'
JENKINS_USER = ''
JENKINS_PASSWORD = ''

###svn
SVN_ROOT_URL = "http://YOURSVNURL"

###github
GITHUB_API_BASE_URL = 'http://GITHUB-ENT/api/v3'
GITHUB_USER = ''
GITHUB_PASSWORD = ''
GITHUB_PR_DESC_TEMPLATE = "<a href='http://GITHUB-ENT/%s/pull/%s'>pull requests#%s from %s BRANCH %s</a>"

###code https://github.com/douban/code
CODE_API_BASE_URL = 'http://CODE/api'
CODE_PR_DESC_TEMPLATE = "<a href='http://CODE/%s/newpull/%s/'>for %s pull requests#%s</a>"

###shire
VIEW_URL = JENKINS_URL + '/view/shire-branches/'
job_template_dict = {
        'unittest':'shire-branch-template-unittest-10280',
        'pylint':'shire-branch-template-pylint',
        'webtest':'shire-branch-template-webtest-10290',
        'all-in-one': 'shire-branches-pylint-unittest-webtest-all-in-one-template',
}

ark_job_template_dict = {
        'shire' : 'ark-opening-pr-template-shire-11000',
        'suite': 'ark-open-pr-template-suite-31060',
        }

ark_job_shell_template_dict = {
        'suite' : u'BUILD_ID=dontkillme_$JOB_NAME\nhname=`hostname`\nok=`echo $hname | grep ".*\\.intra\\.douban\\.com" | wc -l`\nif [ $ok -eq 1 ]; then\n  domain=$hname\nelse\n  domain="$hname.intra.douban.com"\nfi\nPR_NUM=`echo "${JOB_NAME}"|awk -F \'-\' \'{print $4}\'`\nDISPLAY=:90 bash tools/ci-scripts/suite.sh -a %s -s %s -d $domain -n $PR_NUM',
        }


try:
    from local_config import *
except ImportError:
    pass


ARK_OPENING_PR_VIEW_URL = JENKINS_URL + '/view/ark-forks/'
