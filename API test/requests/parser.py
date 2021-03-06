import json, os, requests, datetime, logging

logging.basicConfig(level=logging.DEBUG, format='[%(asctime)s] %(filename)s[line:%(lineno)d] %(levelname)s: %(message)s',
    datefmt = '%a, %d %b %Y %H:%M:%S',
    filename = 'test.log',
    filemode = 'a')

def readConfig(filename):
    try:
        file = open(os.path.join(os.path.abspath('.'), filename), 'r')
        data = json.load(file)
        return data
        file.close()
    except IOError:
        logging.debug("cannot find the config json file")
    

#readConfig('config.json')
def handleException(name, valueFromOtherAPI=0):
    try:
        loadParameter(name, valueFromOtherAPI)
    except Exception, e:
        writeLog(name, e)

def loadParameter(name, valueFromOtherAPI=0):
    try:
        data = readConfig('config.json')
        content = data[name]
    #    print content
        logging.debug(content['method'])
        if content['method'] == 'POST':
            dataPath = content['content'][0]['valid']
            if (valueFromOtherAPI != 0 ):
                logging.debug(valueFromOtherAPI)
                data1 = loadPostData(dataPath,content['replace'],valueFromOtherAPI)
            else:
                data1 = loadPostData(dataPath)
            logging.debug(content['validation'])
            response = postAPI(content['url'], data1)
            logging.debug('response text is '+ response.text)

        elif content['method'] == 'GET': 
            getUrl = content['url'].encode('utf-8')
            if (valueFromOtherAPI != 0):
                getUrl = getUrl.replace('[ReplaceTag]', valueFromOtherAPI)
            response = getAPI(getUrl)
       
        elif content['method'] == 'DELETE':
            getUrl = content['url'].encode('utf-8')
            if (valueFromOtherAPI != 0):
                getUrl = getUrl.replace('[ReplaceTag]', valueFromOtherAPI)
                logging.debug(getUrl)
            response = deleteAPI(getUrl)
            logging.debug(response.status_code)
        else:
            print "Wrong method in Config file"
        
        if response.status_code == 200:
            if validationRes(response.text, content['validation']):
                writeLog(name,'Success')
            else:
                writeLog(name, 'Failed')
        else:
            writeLog(name, 'Failed')
            writeLog(response.status_code, 'error code')
        if 'return' in data[name].keys():
            logging.debug(saveReturnValue(response.text,data[name]['return']))
            return saveReturnValue(response.text,data[name]['return'])
        else:
            logging.debug('No need to save return data')
    except Exception, e:
        writeLog(name, e)

def saveReturnValue(data, param):
    #print 'data is '+data
    print data
    data = json.loads(data)
    print 'param is '+ param
    print type(data)
    if isinstance(data, list):
        print "response text is list"
        print data
        for i in data:
            if i.has_key(param):
                print 'param inside'
                print i[param]
                return i[param]
    if isinstance(data, dict):
        if param in data:
            print 'key in dict is'
            print data[param]
            return data[param]
        



def validationRes(param, validationData):
    print "validationRes**** "
    print validationData
    logging.debug(param)
    param = json.loads(param)
    if isinstance(validationData, dict) and isinstance(param, dict):
        print "validationData.text is dict"
        # print isinstance(validationData, dict)
        # print isinstance(param, dict)
        # print param
        # if set(validationData.items()).issubset(param.items()):
            # print "success!!"
            # return True
        # else:
            # print "not subset"
            # return False
        
        for (k,v) in validationData.items():
            if param.has_key(k) and param[k] == v:
                print "success"
                return True
    elif isinstance(param, list):
        print "response is list"
        for i in param:
        #    print i
            for (k,v) in validationData.items():
            #    print isinstance(i, dict)
                if i.has_key(k) and i[k] == v:
                    print "list inside sucess"
                    return True
        
    else:
#        print param
        print "response.text is not dict"
        return False
    return False
    #print param.status_code


def loadPostData(path,replace=0,valueFromOtherAPI=0):
#    print os.path.join(os.path.abspath('.'), path)
    try:
        postFile = open(os.path.join(os.path.abspath('.'), path), 'r')
        postData = json.load(postFile)
        if (valueFromOtherAPI != 0):
            for (k,v) in postData.items():
                if k == replace:
                    postData[k] = valueFromOtherAPI
                    tempFile = open(os.path.join(os.path.abspath('.'), path), 'w')
                    json_str = json.dumps(postData)
                    print json_str
                    tempFile.write(json_str)
                    tempFile.close()
        
        postFile.close()
        return postData
    except IOError:
        print "cannot find the config json file"


def postAPI(url, file):
    r = requests.post(url, json=file)
    return r

def getAPI(url):
	r = requests.get(url)
	return r

def deleteAPI(url):
    print '&&&&&'
    print url
    r = requests.delete(url)
    return r
    
def writeLog(name, string):
    file = open('result.log', 'a')
    file.write('%s: API: %s   test result is %s \n' %(datetime.datetime.now(),name,string))
    file.close()
    



loadParameter('addDefaultPolicyForProduct')
# loadParameter('list')
# #loadParameter('upsertDpTemplate')
# #loadParameter('upsertDpExpression')
# #loadParameter('upsertDpKeyword')
# #loadParameter('cloneExpression',loadParameter('upsertDpExpression'))
# #loadParameter('cloneKeyword',loadParameter('upsertDpKeyword'))
# #loadParameter('cloneTemplate',loadParameter('upsertDpTemplate'))
loadParameter('getDpTemplate')
loadParameter('getDpKeyword')
loadParameter('getDpExpression')
loadParameter('getEOpolicy')
loadParameter('getODpolicy')
loadParameter('getSOpolicy')
loadParameter('clone',loadParameter('list'))
loadParameter('details', loadParameter('list'))
loadParameter('addPolicy')
loadParameter('updatePolicy', loadParameter('addPolicy'))

# # #loadParameter('import')
# # loadParameter('export')
loadParameter('matchCAS')
loadParameter('getPolicy', loadParameter('list'))
loadParameter('policyEnabledInfo', loadParameter('list'))
loadParameter('getScanTarget')
loadParameter('serverStatus')
loadParameter('throttlingRatio')
loadParameter('throttlingRatioType')
loadParameter('taskStatus')
loadParameter('Validation')


loadParameter('deleteTemplate', loadParameter('cloneTemplate',loadParameter('upsertDpTemplate')))

loadParameter('deleteKeyword', loadParameter('cloneKeyword',loadParameter('upsertDpKeyword')))
loadParameter('deleteExpression', loadParameter('cloneExpression',loadParameter('upsertDpExpression')))
loadParameter('deletePolicy', loadParameter('clone',loadParameter('list')))    
    

#loadParameter('addDefaultPolicyForProduct')
loadParameter('policyList')
loadParameter('policyContent', loadParameter('list'))

loadParameter('deletePolicyByType')
