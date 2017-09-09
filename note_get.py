#!/Library/Frameworks/Python.framework/Versions/3.6/bin/python3

from bs4 import BeautifulSoup
import requests
from subprocess import run
import os.path

def make_note(name, body, folder='CS 252'):
    args = ['osascript', 'create_note.scpt', name, body, folder]
    run(args)

def parse_each_file(url, soup):
	for link in soup.find_all('a', href=True):
		link_url = link['href']
		if link.text.endswith('/'):
			print("text: " + link.text)
			print("Entering directory: " + link_url)
			next_url = main_url + link_url
			next_page = requests.get(next_url)
			next_soup = BeautifulSoup(next_page.text, 'html.parser')
			parse_each_file(next_url, next_soup)
		elif link.text.endswith('.txt') and not os.path.exists("notes/" + link.text):
			print("Getting file: " + link_url)
			file_page = url + link_url
			file = requests.get(file_page)
			modify_file(file, link.text)

def modify_file(file, name):
	txt_file = open("/Users/Andrew1/Desktop/git/252Notes/notes/" + name, 'w+')
	note = ''
	lines = file.text.split('\n')
	for line in lines:
		if line == '':
			pass
		else:
			note += '<p>' + line + '<p>'
	txt_file.close()
	make_note(name, note)




main_url = 'https://faculty.cs.byu.edu/~barker/cs252/notes/'
r = requests.get(main_url)
soup = BeautifulSoup(r.text, 'html.parser')
parse_each_file(main_url, soup)