#!/usr/bin/env python3
import sys
sys.path.append('./lib')
import github3
from getpass import getpass, getuser
import re
from wordcloud import WordCloud
from os import path
from GHLogin import Login
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer

user = input("Please enter your username\n>")
token = getpass("please enter your P.A.T. for authentication\n>")

login = Login(user, token)
gh = login.authenticate()

#Regex function to remove punctuation
def rpunc(text):
	return re.sub(r"\p{P}+", "", text)

#Regex to remove http links:
def rhttp(text):
	http_pat = 'http[s]?:\/\/(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'	
	return re.sub(http_pat, "", text)

def get_org():
	for orgs in gh.iter_orgs():
		#Specify an org at a time. You'll need to query the API to get the org ID
		org = [orgs for orgs in gh.iter_orgs() if orgs.id == 9919]
	return org

def get_repos():
	for orgs in get_org():
		#Specify one repository at a time. You'll need to query the API to get the ID of the repoistory
		repos = [repos for repos in orgs.iter_repos() if repos.id == 24772020]
	return repos

def get_prs():
	pulls = []
	for repo in get_repos():
		for prs in repo.iter_pulls():
			pulls.append(prs)
	return pulls

def get_comments():
	comments = []
	for pulls in get_prs():
		for comms in pulls.iter_comments():
			comments.append(comms)
	return comments

def get_comment_details():
	comment_deets = []
	for comments in get_comments():
		comments = comments.to_json()
		comment_deets.append(comments['body'])
	#Returns a list of json objects
	print("The list count of comment details is", len(comment_deets))
	return comment_deets
			
def filter_words(json_list):
	http_reg = "http[s].+?"
	#md_url_reg = "\[.+?\]\(.+?\)"
	exclusion_list = [ "githubcom" "github","the", "a", "an", "is", "|" "https", "http", "\*", "and", "i", "as", "of", "are", "be", "it", "do", "on", "too", "to"]
	awesome_list = []
	word_count = {}
	for the_words in json_list:
		http_pat = 'http[s]?:\/\/(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
		puncs = r"\p{P}+"
		the_words = re.sub(puncs, "", the_words)
		the_words = re.sub(http_pat, "", the_words)
		the_words = the_words.split(" ")
		awesome_list.append(the_words)
	for comments in awesome_list:
		count = 1 
		#Each comment is a list, cycle through the individual words in each list of lists
		for word in comments:
			if word not in exclusion_list and word != "":
				#Now that the word qualifies, write the word as key to a dictionary, and add the count up as we go, as its corresponding value
				word_count[word] = count
				with open("count.txt", "a+") as f:
					f.write(word + "\n")
			else:
				count = count + 1
	return word_count

def sentiment_analyzer(x):
	pos = []
	for comments in x:
		blob = TextBlob(comments, analyzer=NaiveBayesAnalyzer())
		for sentences in blob.sentences:
			print("Analyzing this sentence:\n ", sentences)
			print(sentences.sentiment)
			pos_val = sentences.sentiment[1]
			#print(type(pos_val))
			#Append the positivity scale here
			pos.append(pos_val)
	return pos

print(sentiment_analyzer(get_comment_details()))
