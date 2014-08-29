vasks
=====
[Peteris](https://github.com/jollychang/peteris) [Vasks](https://github.com/jollychang/vasks)的vasks    
auto fetch svn branch/git pull request to assign jenkins job     
根据Jenkins job template和Jenkins view自动创建/删除 subversion branch和Git Pull Request Jenkins job    

#### shire-branches  
 
`crontab -l`  
`0 * * * *  python /home/jenkins/vasks/vasks.py --create-job >> /home/jenkins/vasks/vasks.log 2>&1`  
`0 2 * * *  python /home/jenkins/vasks/vasks.py --delete-jobs-by-view-url >> /home/jenkins/vasks/vasks.log 2>&1`  

#### github-ent
`python gasks.py -d -a`

#### code
`python code_vasks.py -d -r erebor -v http://YOURJENKINSURL/view/adp/view/erebor-opening-pr/ `  
`python code_vasks.py -a -r erebor -v http://YOURJENKINSURL/view/adp/view/erebor-opening-pr/ -t erebor-openingPR-template-suite-11080`


[Pēteris Vasks](http://en.wikipedia.org/wiki/P%C4%93teris_Vasks) is a Latvian composer.