#SEARCH VIA KEYWORD FUNCTIONALITY v 1.1

from bs4 import BeautifulSoup
import webbrowser
import urllib
import subprocess
import pyperclip

opener = urllib.FancyURLopener({})
f=open('iwant.txt','r')
g=open('links.txt','w')

def linkfromkeyword(keyword):
   # "function_docstring"
   # function_suite
   # return [expression]
   	keyword=(keyword.strip()).replace(' ','+')
	print "The keyword you looked for is: "+keyword
	query="https://www.youtube.com/results?search_query=%s" % (keyword)
	# print query
	openerFile = opener.open(query)
	htmlFile = openerFile.read()
	soup = BeautifulSoup(htmlFile,"html.parser")
	link = soup.find_all("a", "yt-uix-tile-link")
	# here is where the refining should happen for v 1.2
	link= "https://www.youtube.com"+str(link[2]['href'])
	link= (link.split('&list'))[0]
	print "This is the most relevant link we found on youtube: "+link
	g.write(link+"\n")

for line in f.readlines():
	checkcomment=line.find("///")
	checklink=line.find("https://www.youtube.com")
	checkboard=line.find("billboardchart100")
	checkgaana=line.find("gaana50")
	# was it a link or a search term
	if not checkcomment==-1:
		print "Booting up..."
	elif not checklink==-1:
		g.write(line)
		print "We found a link in your search file and have directly appended it to the download file"
	elif not checkboard==-1:
		maxsongs=((line.split(' '))[1])
		check=((line.split(' '))[2])
		print "Gathering "+maxsongs+" top songs from the billboard charts"
		chartlink= "http://www.billboard.com/charts/hot-100" 
		openerFile = opener.open(chartlink)
		htmlFile = openerFile.read()
		soup = BeautifulSoup(htmlFile,"html.parser")
		hits = soup.find_all("div", "row-title", limit=int(maxsongs))
		hitcount=0
		for hit in hits:
			song_name=str(hits[hitcount].h2)
			artist_name= str(hits[hitcount].h3)
			hitcount=hitcount+1
			song_name=song_name.replace('<h2>','').replace('</h2>','').replace('Traceback (most recent call last):','').strip()
			artist_name=artist_name.split('>')[2].replace('</a','').strip()
			if check=='c':
				yesorno=raw_input('Would you like to download: '+song_name+"-"+artist_name+"\n")
				if yesorno=='y':
					key=song_name+" "+artist_name
					linkfromkeyword(key)
			else:
				key=song_name+" "+artist_name
				linkfromkeyword(key)
	elif not checkgaana==-1:
		maxsongs=((line.split(' '))[1])
		check=((line.split(' '))[2])
		print "Gathering "+maxsongs+" top 50 bollywood songs"
		chartlink= "http://gaana.com/topcharts/gaana-dj-bollywood-top-20" 
		openerFile = opener.open(chartlink)
		htmlFile = openerFile.read()
		soup = BeautifulSoup(htmlFile,"html.parser")
		hits = soup.find_all("hgroup", limit=int(2+int(maxsongs)))
		hits.pop(0)
		hits.pop(0)
		hitcount=0
		for hit in hits:
			print hitcount
			song_name=str(hits[hitcount].h2.a['title'])
			print song_name
			album_name= str(hits[hitcount].h3.a['title'])
			print album_name
			artist_name= str(hits[hitcount].h3.a['title'])
			print artist_name
			hitcount=hitcount+1
			if check=='c':
				yesorno=raw_input('Would you like to download: '+song_name+"-"+artist_name+"\n")
				if yesorno=='y':
					key=song_name+" "+artist_name
					linkfromkeyword(key)
			else:
				key=song_name+" "+artist_name
				linkfromkeyword(key)

	else:
		key=str(line)
		linkfromkeyword(key)

f.close()
g.close()

menu= int(input("The download file is ready. Press 1 to download automatically but with no progress updates, Press 2 to download manually(one step) with updates\n"))
command='youtube-dl --extract-audio --audio-format mp3 -o "D:/Utility/cool stuff/youtube downloads/songs/%(title)s.%(ext)s" -a links.txt --no-cache-dir'
if (menu==1):
	# download command
	bashCommand = command
	process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
	output=process.communicate()[0]
	print output
elif (menu==2):
	# command for bash
	print "Enter the following command in the root folder bash terminal, it has been copied to the clipoard for your convenience"
	print command
	pyperclip.copy(command)
