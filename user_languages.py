#!/usr/bin/env python3
import github3
import sys

sys.path.append('./lib')
from github3 import GitHubEnterprise
from getpass import getpass, getuser
import re
from os import path
from GHLogin import Login
import pprint

pp = pprint.PrettyPrinter(indent=4)

# number of reqs per hour allowed by github.com api.
reqs_max = 5000
reqs = 0
ghe = False
user = input("Please enter your username\n>")
token = getpass("please enter your P.A.T. for authentication\n>")
org_search = False

if ghe:
	login = Login(user, token)
	gh = login.authenticate_ghe()
else:
	login = Login(user, token)
	gh = login.authenticate()


def get_org():
	for orgs in gh.iter_orgs():
		# Specify an org at a time. You'll need to query the API to get the org ID
		org = [orgs for orgs in gh.iter_orgs()]
	return org


def get_repo():
	# Get repos by org if org_search flag is set as above. Else statement will search the user account repos
	if org_search:
		for orgs in get_org():
			repo = [repos for repos in orgs.iter_repos()]
		return repo
	else:
		# refresh is needed, otherwise modules returns 'None' array object without the refresh
		repo = [r.refresh() for r in gh.iter_user_repos(user) if r.id == 68479364]
		return repo


# Intent is to return the member ID to key the repository contributor when we loop through repositories
def get_members():
	for orgs in get_org():
		ids = [members.id for members in orgs.iter_members()]
	return set(ids)


def user_langs():
	commit_list = []
	sha_list = []
	committer_and_file_type = []
	repo = [r for r in get_repo()]
	for r in repo:
		commits = r.iter_commits(number=11)
		print(commits)
		for c in commits:
			max_shas = 0
			while max_shas < 10:
				sha = c.sha
				sha_list.append(sha)
				max_shas = max_shas + 1


	for sha in sha_list:
		commit_list.append(r.commit(sha).to_json())

	for cj in commit_list:
		try:
			files = cj['files'][0]['filename']
			committer = cj['commit']['author']['name']
			continue
		except TypeError:
			continue
		except IndexError:
			continue

		finally:
			if "/" in files:
				files = files.split("/")[-1]
				extension = files.split(".")[-1]
				committer_and_file_type.append([committer, extension])
			elif "." in files:
				files = files.split(".")[-1]
				committer_and_file_type.append([committer, files])
			else:
				pass

	return committer_and_file_type


def parse_results(x):
	cc = len(x)
	rdict = {}
	tc = "Total Commits"
	tc_cc = (tc, cc)
	rdict[tc_cc] = 1
	# dataset = type(tuple)
	for ds in x:
		n, ft = ds
		nft = (n, ft)
		if not nft in rdict:
			# name, filetype
			rdict[nft] = 1
		else:
			rdict[nft] += 1

	return rdict


commit_data = parse_results(user_langs())

for k, v in commit_data.items():
	print(k[0], k[1], v)

#print("DEBUG: commit_data ouput: ", commit_data)
uniq_fts = {}

# Returns the count of commits by file type, regardless of user
for tup, c in commit_data.items():
	n, ft = tup
	if n == "Total Commits":
		pass

	elif not ft in uniq_fts:
		uniq_fts[ft] = 1
	else:
		uniq_fts[ft] += 1

#print(uniq_fts)

