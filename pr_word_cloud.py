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
	for orgs in get_org():
		#Specify one repository at a time. You'll need to query the API to get the ID of the repoistory
		repos = [repos for repos in orgs.iter_repos() if repos.id == 24772020]
	return repos

def get_prs():
	pulls = []
	for repo in get_repos():
		for prs in repo.iter_pulls(state='all'):
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
	return comment_deets
			
def filter_words(json_list):
	exclusion_list = [
			"github", 
			"the", 
			"a", 
			"an", 
			"is", 
			"|" 
			"https", 
			"http", 
			"\*", 
			"and", 
			"i", 
			"as", 
			"of", 
			"are", 
			"be", 
			"it", 
			"do", 
			"on", 
			"too", 
			"to",
			"x",
			"xs",
			"git",
			"enterprise",
			"engineering"
			]
	words_list = []
	word_count = {}
	for the_words in json_list:
		the_words = TextBlob(the_words.lower())
		words_list.append(the_words.words)
	for words in words_list:
		#Each comment is a list, cycle through the individual words in each list of lists
		for word in words:
			#print("Debug: word iterable is: ", word)
			if word in exclusion_list:
				words.remove(word)
			#The next several conditionals were added for data-massaging, as the conditionals below them were still evaluating
			#the strings as not in the exclusion list
			elif len(word) <= 2:
				words.remove(word)
			elif '\'' in word:
				words.remove(word)
			elif word == "https": 
				words.remove(word)
			elif word == "http":
				words.remove(word)
			elif "github" in word:
				words.remove(word)
			elif word not in exclusion_list:
				#Now that the word qualifies, write the word as key to a dictionary, and add the count up as we go, as its corresponding value
				word_count[word] = 1
				with open("count.txt", "a+") as f:
					f.write(word + "\n")
			elif word not in exclusion_list and word_count[word]:
				word_count[word] += 1
			else:
				pass

	return word_count

def wordc(input_file):
	d = path.dirname(__file__)
	text = open(path.join(d, input_file)).read()
	wordcloud = WordCloud(width=800, height=600, max_words=300, background_color='gray', max_font_size=96, relative_scaling=1).generate(text)
	image = wordcloud.to_image()
	image.save('wordcloud.png')
	image.show()


datadict = filter_words(get_comment_details())
wc = wordc("count.txt")
