import urllib.request as urllib
from urllib.parse import quote
from bs4 import BeautifulSoup
import lxml
import requests
from .models import Domain, SearchObject, VailidValues, SchemaParsing, Expression, Credentials, RequestHeaders, SessionData, CredentialsData, ResumeLink, SearchResult
from random import random
from re import findall

class LoginServer(object):
    def __init__(self, domain):
        self.domain = domain
        self.authSession = requests.Session()
        self.__credentialsOrigen__ = None
        self.__authData__ = None
        self.__sessionHeaders__ = None
        self.__sessinCookies__ = None

    def __nullCookies__(self):
        if(not self.__sessinCookies__):
            self.__sessinCookies__ = SessionData.objects.filter(credentials=self.__credentialsOrigen__)
        if(len(self.__sessinCookies__) <= 0):
            return False
        else:
            for cookie in self.__sessinCookies__:
                if(cookie.cookieValue):
                    return False
            return True

    def __notCookies__(self):
        if(not self.__sessinCookies__):
            self.__sessinCookies__ = SessionData.objects.filter(credentials=self.__credentialsOrigen__)

        if(len(self.__sessinCookies__) <= 0):
            return True
        else:
            return False

    def connect(self):
        pass    
        #preRequest = requests.Request("POST", self.__credentialsOrigen__.testLink)
        #requestSession= self.authSession.prepare_request(preRequest)
        #testRequest = self.authSession.send(requestSession)
        #if(testRequest.status_code == 200):
        #   return True
        #else:
        #   return False

    def authOut(self):
        SessionData.objects.all().delete()
        #if(not self.__sessinCookies__):
        #    self.__sessinCookies__ = SessionData.objects.filter(credentials=self.__credentialsOrigen__)
        #else:
        #    for cookie in self.__sessinCookies__:
        #        cookie.cookieValue = None
        #        cookie.save()

    def cookiesDell(self):
        sessionDat = SessionData.objects.filter(credentials=self.__credentialsOrigen__)##.delete()
        for item in sessionDat:
            item.delete()
        ##return True 

    def authLogin(self):
        self.__credentialsOrigen__ = Credentials.objects.get(domain=self.domain)
        self.__sessionHeaders__ = RequestHeaders.objects.filter(credentials=self.__credentialsOrigen__)

        self.authSession.headers = {item.sectionName : item.body for item in self.__sessionHeaders__}

        if(self.__nullCookies__() or self.__notCookies__()):
            ##Рассмотреть случай, когда не входим в условие
            loginGet = requests.Request("GET", self.__credentialsOrigen__.loginLink)
            preRequest = self.authSession.prepare_request(loginGet)
            loginRequest = self.authSession.send(preRequest)

            if(loginRequest.status_code != 200):
                raise ValueError("Bad Credentials!")

            securityTokin = self.authSession.cookies.get_dict()
            self.__authData__ = CredentialsData.objects.filter(credentials=self.__credentialsOrigen__)

            for itemAuth in self.__authData__:
                if(not itemAuth.value):
                    itemAuth.value = securityTokin.get(itemAuth.name)

            authData = {item.name : item.value for item in self.__authData__}
            loginPost = requests.Request("POST", self.__credentialsOrigen__.loginLink, data=authData)
            authPreReguest = self.authSession.prepare_request(loginPost)
            authRequest = self.authSession.send(authPreReguest)

            if(authRequest.status_code != 200):
                raise ValueError("Bad authData!")

            authCookies = self.authSession.cookies.get_dict()
            for cookie in authCookies:
                SessionData.objects.update_or_create(cookieName=cookie, credentials=self.__credentialsOrigen__, defaults={'cookieValue': authCookies[cookie]},)
        if(not (self.__nullCookies__() and self.__notCookies__())):
            sessionCookies = SessionData.objects.filter(credentials=self.__credentialsOrigen__)
            for cookie in sessionCookies:
                self.authSession.cookies.set(cookie.cookieName, cookie.cookieValue)

            ##if(not self.connect()): 
                ##self.cookiesDell()
                ##self.authOut()
                ##self.authLogin()

class ResumeMeta(object):
    def __init__(self, domain,**kwargs):
        self.domain = domain
        self.pay = kwargs.get('pay')
        self.age = kwargs.get('age')
        self.jobExp = kwargs.get('jobExp')
        self.lastJob = kwargs.get('lastJob')
        self.jobTitle = kwargs.get('jobTitle')
        self.gender = kwargs.get('gender')
        self.link = kwargs.get('link')              # в системе
        self.origenLink = kwargs.get('origen')      # на сайте источнике локальная
        self.previewLink = kwargs.get('preview')    # предварительный просмотр из системы на источнике

    def setAttr(self, attrName, attrVal):
        if(attrName in self.__dict__):
            self.__dict__[attrName] = attrVal

    def createLink(self):
        if(not self.origenLink):
            return
        else:
            self.previewLink = self.domain.rootUrl + self.origenLink
            self.link = '/search/result/resume/' + self.previewLink

    #def __str__(self):
    #    format = '\n'
    #    for attrName in self.__dict__:
    #        row = '%s = %s\n' %(attrName, self.__dict__[attrName])
    #        format += row
    #    return format

class ResumeData(object):
    def __init__(self, domain, **kwargs):
        self.domain = domain
        self.firstName = kwargs.get('firstName')
        self.lastName = kwargs.get('lastName')
        self.middleName = kwargs.get('middleNam')
        self.phone = kwargs.get('phone')
        self.email = kwargs.get('email')
        self.location = kwargs.get('location')
        self.education = kwargs.get('education')
        self.experience = kwargs.get('expJob')
        self.gender = kwargs.get('gender')

    def get(self, attrName):
        if(attrName not in self.__dict__):
            return None
        else:
            return self.__dict__[attrName]

    def __str__(self):
        format = '\n'
        for attrName in self.__dict__:
            row = '%s = %s\n' %(attrName, self.__dict__[attrName])
            format += row
        return format

    def setAttr(self, attrName, attrVal):
        if(attrName in self.__dict__):
            self.__dict__[attrName] = attrVal

    def validGender(self):
        validValueList = VailidValues.objects.filter(domain=self.domain, context="RESUME")
        validValueDict = {item.rawValue : item.validValue for item in validValueList}
        ##print('validValueDict>>',validValueDict)
        ##print('self.gender>>',self.gender)
        self.gender = validValueDict.get(self.gender)

class OrigenUrl(object):
    def __init__(self,domain=None, url=None):
        self.__domain__ = domain
        self.__url__ = url
        self.__iterNum__ = 0
        self.pattern = None

    def setDomain(self, domainName=None):
        if((not self.__url__) and domainName):
            self.__domain__ = Domain.objects.get(domainName=domainName)
        if(self.__url__ and (not domainName)):
            domainName = findall(r'\w{0,4}\.?\w+\.ru', self.__url__)
            self.__domain__ = Domain.objects.get(domainName=domainName)
        else:
            raise TypeError("can not specify Domain and Url at the same time!")

    def getDomain(self, isObject=False):
        if(isObject):
            return self.__domain__
        else:
            return self.__domain__.domainName

    def setUrlOrPattern(self, url=None, **kwargs):
        if((not url) and self.__domain__):
            #Load Pattern
            self.pattern = SearchObject().getPattern(domain=self.__domain__,mode=kwargs.get('mode'),ageFrom=kwargs.get('ageFrom'),ageTo=kwargs.get('ageTo'),salaryFrom=kwargs.get('salaryFrom'),salaryTo=kwargs.get('salaryTo'),gender=kwargs.get('gen'))
        if(url and self.__domain__):
            domainName = findall(r'\w{0,4}\.?\w+\.ru', url)[0]
            if(domainName != self.__domain__.domainName):
                ##print('doaminName>>',domainName,'__domain__.domainName>>',self.__domain__.domainName)
                raise ValueError("A link can be reinstalled within the same domain")
            else:
                self.__url__ = url

    def getUrl(self):
        return self.__url__

    def getIterationNum(self):
        if(not self.pattern):
            raise ValueError("Patern link is not defained")
        return self.__iterNum__

    def setIterationNum(self, iterationNum=0):
        if(not self.pattern):
            raise ValueError("Pattern link is not defained")
        self.__iterNum__ = iterationNum

    def createLink(self, dataParm):
        if(not self.pattern):
            raise ValueError("Pattern link is not defained")

        self.__iterNum__ = self.pattern.startPosition
        listParamtrs = self.pattern.parametrs.split(',')
        link = self.pattern.link
        ##print(dataParm)
        ##print(self.pattern.parametrs.split(','))
        ##print(self.pattern.domain.domainName)
        ##print('>>',dataParm['ageto'])
        for parametr in listParamtrs:
            ##print('233 >>', len(listParamtrs))
            ##print('===>',parametr,parametr.lower(),dataParm.get(parametr.strip().lower()))
            link = link.replace(parametr, dataParm.get(parametr.strip().lower()))

        ##print('237 >>', link)
        self.__url__ = link 

    def createSearchLink(self, dataParm, data):
        dataParm.setdefault('heash_search', str(int(random()*10**15)))
        valList = VailidValues.objects.filter(domain=self.__domain__, context='SEARCH')
        for item in valList:
            if((data.get('gender') == item.rawValue) and item.criterionName == 'gender'):
                data['gender'] = item.validValue
            if((data.get('ageFrom') == item.rawValue) and item.criterionName == 'ageFrom'):
                data['ageFrom'] = item.validValue
            if((data.get('ageTo') == item.rawValue) and item.criterionName == 'ageTo'):
                 data['ageTo'] = item.validValue

        self.setUrlOrPattern(mode=data.get('searchMode'),ageFrom=data.get('ageFrom'),ageTo=data.get('ageTo'),salaryFrom=data.get('salaryFrom'),salaryTo=data.get('salaryTo'),gen=data.get('gender'))
        self.createLink(dataParm)

    def nextOrStartIteration(self):
        ##print('Enter>>')
        if((not self.pattern) and self.__url__):
            raise TypeError("Object url have is not iteration")
        else:
            link = self.__url__.replace(self.pattern.iterator, str(self.__iterNum__))
            self.__iterNum__ += self.pattern.iterStep
            ##print('link>>', link)
            ##print('self.__iterNum__>>',self.__iterNum__)

        return link

class OrigenRequest(object):
    def __init__(self,domain=None, linkObj=None):
        self.domain = domain 
        self.link = linkObj
        self.__auth__ = None

    def getLink(self, isObject=False):
        if(isObject):
            return self.link
        else:
            return self.link.getUrl()

    def setLink(self,domain=None,url=None):
        if(not url and not domain):
            return None
        else:
            self.link = OrigenUrl(domain, url)

    def setLinkObj(self, linkObj):
        if(linkObj):
            self.link = linkObj

    def request(self):
        if(not self.__auth__):
            self.__auth__ = LoginServer(self.domain)
            try:
                self.__auth__.authLogin()
            except ValueError:
                self.__auth__.authOut()
                self.__auth__.authLogin()
        ##else:
            ##if(not self.__auth__.connect()):
            ##    self.__auth__.authLogin()
            ##    print('------------------')
            ##    print('self.__auth__.connect()>>',self.__auth__.connect())
            ##    print('>>Not connect!!<<')
        if(self.link.pattern):
            searchLink = self.link.nextOrStartIteration()
        else:
            searchLink = self.link.getUrl()

        try:
            connectRequest = requests.Request('GET',searchLink)
            connectSession = self.__auth__.authSession.prepare_request(connectRequest)
            content = self.__auth__.authSession.send(connectSession)
            outContent = content.text
            content.close()
        except UnboundLocalError:
            outContent = None

        return outContent

class OriginParsing(object):
    def __init__(self, domain, limit, context, search_card=None):
        self.domain = domain
        self.context = context
        self.search_card = search_card
        self.__limit__ = int(limit)
        self.countResume = 0
        self.__notFound__ = None
        self.__bodyResponse__ = None
        self.__schema__ = None

    def createResumeLink(self, url):
        self.link.setUrlOrPattern(url)

    def generalSchem(self):
        prserSchem = []
        parserList = SchemaParsing.objects.filter(domain=self.domain, context=self.context, inactive=False)##,parSchemaParsing__isnull=False)
        for item in parserList:
            if(item.target == 'error' or item.target == 'bodyResponse'):
                pass
            else:
                row = []
                expression = Expression.objects.filter(SchemaParsing=item).order_by('seqOper')
                row.append(item)
                if(expression):                        
                    for expItem in expression:
                        row.append(expItem)
                prserSchem.append(row)
        self.__schema__ =  prserSchem

    def setErrorTarget(self):
        self.__notFound__ = SchemaParsing.objects.get(domain=self.domain, context=self.context, target='error')

    def setBodyResponceTarget(self):
        self.__bodyResponse__ = SchemaParsing.objects.get(domain=self.domain, context=self.context, target='bodyResponse')

    def parser(self, schema_parsing, tree):
        ##Вот эту дерминку не мешало бы переписать по человечески
        ##без дублирования кода, а то это какая-то кантуженная рекурсия
        if(schema_parsing.parSchemaParsing):
            tree = self.parser(schema_parsing.parSchemaParsing, tree)
            if(tree):
                if(schema_parsing.notAttr):
                    listTags = tree.findAll(schema_parsing.tagName)
                    for itemTag in listTags:
                        if(not itemTag.attrs):
                            return itemTag

                elif(schema_parsing.sequens):
                    listTags = tree.findAll(schema_parsing.tagName, {schema_parsing.attrName : schema_parsing.attrVal})
                    if(len(listTags) > schema_parsing.sequens - 1): ##изменил >= на >
                        return listTags[schema_parsing.sequens - 1]
                    else:
                        return None
                else:
                    return tree.find(schema_parsing.tagName, {schema_parsing.attrName : schema_parsing.attrVal})
        else:
            if(tree):
                if(schema_parsing.notAttr):
                    listTags = tree.findAll(schema_parsing.tagName)
                    for itemTag in listTags:
                        if(not itemTag.attrs):
                            return itemTag

                elif(schema_parsing.sequens):
                    listTags = tree.findAll(schema_parsing.tagName, {schema_parsing.attrName : schema_parsing.attrVal})
                    if(len(listTags) > schema_parsing.sequens - 1): ##изменил >= на >
                        return listTags[schema_parsing.sequens - 1]
                    else:
                        return None
                else:
                    return tree.find(schema_parsing.tagName, {schema_parsing.attrName : schema_parsing.attrVal})

    def executeExpression(self, expression_parsing, parameter):
        if(not parameter):
            return None

        if((expression_parsing.split)):
            parameter = parameter.split(expression_parsing.split)

        if((expression_parsing.shearTo or expression_parsing.shearFrom) and type(parameter) is not dict):
            parameter = parameter[expression_parsing.shearFrom  : expression_parsing.shearTo]

        if((expression_parsing.regexp) and type(parameter) is str):
            parameter = findall(expression_parsing.regexp, parameter)

        if(expression_parsing.sequence):## or expression_parsing.split):
            ##Так как сделана дружественная индексация от 1 до N
            seque = expression_parsing.sequence - 1
            if(seque < len(parameter)):
                parameter = parameter[seque]

        if((expression_parsing.join) and type(parameter) is list):
            parameter = expression_parsing.join.join(parameter)

        return parameter

    def parsingResume(self, responseContent):
        if responseContent is None:
            return None

        tree = BeautifulSoup(responseContent,'html.parser')
        resultList = []  
        pastRecord = 0 #Счетчик просмотренных резюме
        notFound = tree.find(self.__notFound__.tagName, {self.__notFound__.attrName : self.__notFound__.attrVal})
        if(not notFound):
            resumes = tree.findAll(self.__bodyResponse__.tagName,{self.__bodyResponse__.attrName : self.__bodyResponse__.attrVal})
            for resumeItem in resumes:
                record = {}
                for rowParse in self.__schema__:
                    for itemOper in rowParse:
                        if(type(itemOper) is SchemaParsing):
                            parameter = self.parser(itemOper, resumeItem)
                            if((itemOper.target != 'origenLink')and parameter):
                                parameter = parameter.get_text()
                            elif(parameter):
                                parameter = parameter['href']
                        if(type(itemOper) is Expression):
                            parameter = self.executeExpression(itemOper,                                   parameter)

                    if(type(itemOper) is SchemaParsing):
                        record.setdefault(itemOper.target, parameter)
                    else:

                        record.setdefault(itemOper.SchemaParsing.target, parameter)
                    ##resumeRecord.setAttr(itemOper.target, parameter)

                    if(type(itemOper) is SchemaParsing):
                        ##resumeRecord.setAttr(itemOper.target, parameter)
                        ##print('itemOper.target>>',itemOper.target)
                        record.setdefault(itemOper.target, parameter)
                    else:
                        ##resumeRecord.setAttr(itemOper.SchemaParsing.target, parameter)
                        record.setdefault(itemOper.SchemaParsing.target, parameter)
                previewLink = self.domain.rootUrl + record.get('origenLink')
                record.setdefault('URL', previewLink)

                check_result = SearchResult.objects.filter(url=record.get(                                          'URL')).count()

                if not check_result:
                    print('self.search_card>>', self.search_card)
                    search_record = SearchResult.objects.create(search_card=self.search_card, domain=self.domain, pay=record.get('pay'), age=record.get('age'), 
                    jobExp=record.get('jobExp'), lastJob=record.get('lastJob'), jobTitle=record.get('jobTitle'), gender=record.get('gender'), url=record.get('URL'))

                    search_record.save()
                else:
                    search_record = SearchResult.objects.get(url=record.get('URL'))

                check_link = ResumeLink.objects.filter(url=search_record.url).count()

                if not check_link:
                    resultList.append(search_record)
                    self.countResume += 1
                else:
                    print('>>',record)
                pastRecord += 1

                if(pastRecord == self.domain.itemRecord or self.countResume == self.__limit__):
                    return resultList
        else:
            return None


    def parserResume(self, responseContent):
        tree = BeautifulSoup(responseContent,'html.parser')
        notFound = tree.find(self.__notFound__.tagName, {self.__notFound__.attrName : self.__notFound__.attrVal})
        if(not notFound):
            resumeRecord = ResumeData(self.domain)
            for rowParse in self.__schema__:
                ##Перебор по строкам схемы парсера
                for itemOper in rowParse:
                    if(type(itemOper) is SchemaParsing):
                        parameter = self.parser(itemOper, tree)
                        if(parameter):
                            parameter = parameter.get_text()

                    if(type(itemOper) is Expression):
                        parameter = self.executeExpression(itemOper, parameter)

                if(type(parameter) is str):
                    parameter = parameter.strip()

                if(type(itemOper) is SchemaParsing):
                    resumeRecord.setAttr(itemOper.target, parameter)
                else:
                    resumeRecord.setAttr(itemOper.SchemaParsing.target, parameter)
        ##print('resumeRecord line-473>>',resumeRecord)
        resumeRecord.validGender()
        ##print('resumeRecord line-475>>',resumeRecord)
        return resumeRecord