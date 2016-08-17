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

ghe = True
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
		org = [orgs for orgs in gh.iter_orgs() if orgs.id == 195]
	return org

def get_repo():
	for orgs in get_org():
		repo = [repos for repos in orgs.iter_repos() if repos.id == 465]
	return repo

#Intent is to return the member ID to key the repository contributor when we loop through repositories
def get_members():
	for orgs in get_org():
		ids = [members.id for members in orgs.iter_members()]
	return set(ids)

def user_langs():
	sha_list = []
	committer_and_file_type = []
	for repos in get_repo():
		commits = repos.iter_commits()
		for c in commits:
			cj = c.to_json()
			sha_list.append(cj['sha'])
		for shas in sha_list:
			commit = repos.commit(shas)
			cj = commit.to_json()
			try:
				files = cj['files'][0]['filename']
				committer = cj['commit']['author']['name']
				#print(files, committer)
				continue
			except TypeError:
				continue
			except IndexError:
				continue

				
		#committer = cj['committer']['login']
			finally:
				if "/" in files:
					files = files.split("/")[-1]
					extension = files.split(".")[-1]
					committer_and_file_type.append( [committer, extension] ) 
				elif "." in files:
					files = files.split(".")[-1]
					committer_and_file_type.append( [committer, files] )
				else:
					pass
		
	
	return committer_and_file_type


def parse_results(x):
	cc = len(x)
	rdict = {}
	tc = "Total Commits"
	tc_cc = (tc, cc)
	rdict[tc_cc] = 1
	#dataset = type(tuple)
	for ds in x:
		n, ft = ds
		nft = (n, ft)
		if not nft in rdict:
			#name, filetype
			rdict[nft] = 1
		else:
			rdict[nft] += 1
		
	return rdict

commit_data = parse_results(user_langs())

print("DEBUG: commit_data ouput: ", commit_data)
uniq_fts = {}

#Returns the count of commits by file type, regardless of user
for tup, c in commit_data.items():
	#if k != "Total Commits":
	#for tup in k:
	n, ft = tup	
	if n == "Total Commits":
		pass
	
	elif not ft in uniq_fts:
		uniq_fts[ft] = 1
	else:
		uniq_fts[ft] += 1

print(uniq_fts)

