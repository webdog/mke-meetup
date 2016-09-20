#!/usr/bin/env python3
import github3
import sys
sys.path.append('./lib')
from github3 import GitHubEnterprise
from getpass import getpass, getuser
import re
from wordcloud import WordCloud
from os import path
from GHLogin import Login
from textblob import TextBlob

ghe = False
user = input("Please enter your username\n>")
token = getpass("please enter your P.A.T. for authentication\n>")
reqs_max = 5000
org_search = False
user_search = False
pub_search = True

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

def get_repos():
	if org_search:
		for orgs in get_org():
			#Specify one repository at a time. You'll need to query the API to get the ID of the repoistory
			repos = [repos for repos in orgs.iter_repos() if repos.id == 24772020]
		return repos
	elif user_search:
		repo = [r.refresh() for r in gh.iter_user_repos(user) if r.id == 68479364]
		return repo
	else:
		repo = [r.refresh() for r in gh.iter_user_repos('angular') if r.name == 'angular']
		return repo


def get_prs():
	pulls = []
	for repo in get_repos():
		pr = repo.iter_pulls(state='all', number=25)
		pr.refresh()
		for prs in pr:
			pulls.append(prs)
	return pulls


def check_if_merged():
	net_neg = 0
	net_pos = 0
	net_eq = 0
	for pulls in get_prs():
		pulls = pulls.refresh()

		#adds = 0
		#negs = 0
		if pulls.additions is None:
			pulls.additions = 0

		if pulls.deletions is None:
			pulls.deletions = 0

		print("val add: val: delete: ", pulls.additions, pulls.deletions)
		total = pulls.additions - pulls.deletions
		print("This PR had a value of %s" % total)
		if total < 0:
			net_neg += 1

		elif total > 0:
			net_pos += 1
		else:
			net_eq += 1



	return "Total of %s PRs, of which %s were net negative to the repo, and %s were net_positive" % (25, net_neg, net_pos)


print(check_if_merged())


