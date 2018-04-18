import urllib.request as urllib


from bs4 import BeautifulSoup


def getSearchingResults(searchText):
    countRecord = 0
    namberPage = 0
    listOfResumesId = []
    while True:
        searchSpeak = "https://hh.ru/search/resume?area=1&clusters=true&text=%s&pos=full_text&logic=normal&exp_period=all_time&order_by=relevance&area=1&clusters=true&page=%i" %(searchText,namberPage)
        
        connect = urllib.urlopen(searchSpeak)
        content = connect.read()
        soupTree = BeautifulSoup(content, 'html.parser')
        connect.close()
        notFound = soupTree.find('div', {'class': 'error-content-wrapper'})
        if(notFound == None):
            formPersons = soupTree.findAll('tr',{'itemscope': 'itemscope'})
            for item in formPersons:
                listOfResumesId.append(item.find('a',{'itemprop':'jobTitle'}))##['data-hh-resume-hash'])
                countRecord += 1
            # for debag
            if(countRecord >= debugeSize):
                break
        else:
            break
        namberPage += 1
    
    return listOfResumesId
    
    
        
        
if __name__ == '__main__':
    
    debugeSize = 200
    listId = getSearchingResults("Siebel")
    print(listId)