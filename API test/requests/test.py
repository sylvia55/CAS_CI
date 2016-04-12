import requests, time

def getAPI(url):
	r = requests.get(url)
	return r
count = 0

while count < 5:
    if getAPI("http://localhost:8080/policy/serverStatus").status_code != 200:
        print "need to break"
        break
    else:
        count = count + 1
        time.sleep(5)
        print "hello %d" %count