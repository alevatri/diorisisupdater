# Diorisis Corpus Updater
# Made since 2021 by Alessandro Vatri (alessandro.vatri@crs.rm.it)

import zlib, os, requests, json, sys, re, shutil
windowSize = shutil.get_terminal_size().columns

def printNice(variable,fixed,sameLine,sameLineNext):
	init = -1
	sameLine = '\033[1K\033[1G' if sameLine else ''
	returnChar = '' if sameLineNext else '\n'
	while True:
		if len(variable) + len(fixed) < windowSize: break
		variable = variable[:init][:-3]+'...'
		init -= 1
	print('%s%s%s'%(sameLine,variable,fixed), end = returnChar)
	sys.stdout.flush()

dir = '/Volumes/FILES/DiorisisJson' 			#Enter location of Diorisis Corpus (JSON)
destinationDir = '/Users/Alessandro/Desktop' 	#set to = dir if replacing previous version

try:
	register  = json.loads(requests.get('https://www.crs.rm.it/diorisisCorpusupdates/latest.json').text)
except:
	print('Remote server unreachable')
	sys.exit()
for file in os.listdir(dir):
	version = d.group(1) if (d:=re.search('"version": "(.*?)"', open(os.path.join(dir,file), 'r').read())) else "1.0"
	if not register.get(file,None): continue
	printNice('Checking %s'%file, 'version %s'%register[file], False, True)
	if register[file] == version: 
		printNice(file, ' is up to date', True, False)
		continue
	try:
		printNice('Downloading %s'%file, 'version %s'%register[file], True, True)
		rq=requests.post('https://www.crs.rm.it/diorisisCorpusupdates/requestUpdate.php', {'file':file[:-4]+'z'+file[-4:], 's':'YxiidRQCwT'}, stream=True)
		size = rq.headers.get('content-length')
		update = b""
		progress = 0
		for data in rq.iter_content(chunk_size=4096):
			update += data
			progress += len(data)
			printNice('Downloading %s'%file,', version %s | %s%% of %s kb'%( register[file],int(progress*100/int(size)),int(int(size)/1024)), True, True)
	except:
		printNice('Problems with: %s'%file,' - Update download failed',True,False)
		continue
	try:
		json.loads((newData:=zlib.decompress(update).decode('utf-8')))
	except:
		printNice('Problems with: %s'%file,' - Data not valid',True,False)
		continue
	printNice('Updating %s'%file, ' to version %s'%register[file],True, True)
	sys.stdout.flush()
	try:
		newVersion = open(os.path.join(destinationDir,file),'w+')
		newVersion.write(newData)
		newVersion.close()
		printNice(file, ' updated to version %s'%register[file], True, False)
	except:
		printNice('Problems with: %s'%file,' - Could not write to local file', True, False)
	
print('Your copy of the Diorisis Corpus is up to date')