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
		pr = repo.iter_pulls(state='closed', number=25)
		for prs in pr:
			pulls.append(prs)
	return pulls


def check_if_merged():
	prs = get_prs()
	prs_tot = len(prs)
	merged = 0
	nmerged = 0
	for pulls in prs:
		if pulls.is_merged():
			print("found a merged PR")
			merged += 1
		else:
			nmerged += 1
	return "Total of %s PRs, of which %s were merged, %s were not merged" % (prs_tot, merged, nmerged)


print(check_if_merged())


