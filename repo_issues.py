#!/Users/christianweber/anaconda/bin/python
import github3
from github3 import GitHubEnterprise
from getpass import getpass, getuser
import re
from os import path
from GHLogin import Login
import pprint

pp = pprint.PrettyPrinter(indent=4)

ghe = False
user = input("Please enter your username\n>")
token = getpass("please enter your P.A.T. for authentication\n>")

if ghe:
	login = Login(user, token)
	gh = login.authenticate_ghe()
else:
	login = Login(user, token)
	gh = login.authenticate()

def get_org():
	for orgs in gh.iter_orgs():
		#Specify an org at a time. You'll need to query the API to get the org ID
		org = [orgs for orgs in gh.iter_orgs() if orgs.id == 9919]
	return org

def get_repo():
	for orgs in get_org():
		repo = [repos for repos in orgs.iter_repos() if repos.id == 24772020]
	return repo

#Intent is to return the member ID to key the repository contributor when we loop through repositories
def get_members():
	for orgs in get_org():
		ids = [members.id for members in orgs.iter_members()]
	return set(ids)

def get_issues():
	for repos in get_repo():
		issues = [issue for issue in repos.iter_issues(state='all')]
	return issues


issue_author_count = {}
unlabeled_issues = {}
for issues in get_issues():
	issues = issues.to_json()
	author = issues['user']['login']
	label = issues['labels']
	for i in label:
		for k, v in i.items():
			print(i['name'])
	
	print(label)

	#if label == False:
	#	unlabeled_issues[author] = 1
	#elif label is None and author:
	#	unlabeled_issues[author] += 1
	#elif label is not None:
	#	pass

	#if author not in issue_author_count:
	#	issue_author_count[author] = 1
	#else:
	#	issue_author_count[author] += 1


#print(issue_author_count)

print(unlabeled_issues)


