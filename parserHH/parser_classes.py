import re
import time
import json
import datetime
import urllib.request as urllib

from urllib.error import HTTPError, URLError
from bs4 import BeautifulSoup


class BaseException(Exception):
    def __init__(self, message):
        self.message = message


class ParserError(BaseException):
    pass


class EndParserError(BaseException):
    pass


class ExpressionError(BaseException):
    pass


class Expression:
    def __init__(self, **kwargs):
        self.tag = kwargs.get('tag')
        self.attribute = kwargs.get('attribute')
        self.value = kwargs.get('value')

    def __str__(self):
        format_str = '<tag = %s, attribute = %s, value = %s>'  %(
                        self.tag, self.attribute, self.value)
        return format_str


# Parser from search
class BaseParserSearchHTML(object):
    container_error = None
    container_title_resume = None
    container_salary = None
    container_age = None
    container_experience = None
    container_last_position = None
    container_organization_name = None
    container_url = None
    container_last_update = None
    container_body = None

    target_error = Expression()
    target_title_resume = Expression()
    target_salary = Expression()
    target_age = Expression()
    target_experience = Expression()
    target_last_position = Expression()
    target_organization_name = Expression()
    target_url = Expression()
    target_last_update = Expression()
    target_body = Expression()

    def get_container_error(self, html):
        html_tree = BeautifulSoup(html, 'html.parser')
        if self.container_error is not None:
            container_html = html_tree.find(
                                self.container_error.tag,
                                {self.container_error.attribute:
                                self.container_error.value})
        else:
            container_html = html_tree
        return container_html

    def get_container_title_resume(self, html):
        if self.container_title_resume is not None:
            container_html = html.find(
                                self.container_title_resume.tag,
                                {self.container_title_resume.attribute:
                                self.container_title_resume.value})
        else:
            container_html = html
        return container_html

    def get_container_salary(self, html):
        if self.container_salary is not None:
            container_html = html.find(
                                self.container_salary.tag,
                                {self.container_salary.attribute:
                                self.container_salary.value})
        else:
            container_html = html
        return container_html

    def get_container_age(self, html):
        if self.container_age is not None:
            container_html = html.find(
                                self.container_age.tag,
                                {self.container_age.attribute:
                                self.container_age.value})
        else:
            container_html = html
        return container_html

    def get_container_experience(self, html):
        if self.container_experience is not None:
            container_html = html.find(
                                self.container_experience.tag,
                                {self.container_experience.attribute:
                                self.container_experience.value})
        else:
            container_html = html
        return container_html

    def get_container_last_position(self, html):
        if self.container_last_position is not None:
            container_html = html.find(
                                self.container_last_position.tag,
                                {self.container_last_position.attribute:
                                self.container_last_position.value})
        else:
            container_html = html
        return container_html

    def get_container_organization_name(self, html):
        if self.container_organization_name is not None:
            container_html = html.find(
                                self.container_organization_name.tag,
                                {self.container_organization_name.attribute:
                                self.container_organization_name.value})
        else:
            container_html = html
        return container_html

    def get_container_url(self, html):
        if self.container_url is not None:
            container_html = html.find(
                                self.container_url.tag,
                                {self.container_url.attribute:
                                self.container_url.value})
        else:
            container_html = html
        return container_html

    def get_container_last_update(self, html):
        if self.container_last_update is not None:
            container_html = html.find(
                                self.container_last_update.tag,
                                {self.container_last_update.attribute:
                                self.container_last_update.value})
        else:
            container_html = html
        return container_html

    def get_container_body(self, html):
        html_tree = BeautifulSoup(html, 'html.parser')
        if self.container_body is not None:
            container_html = html_tree.find(
                                self.container_body.tag,
                                {self.container_body.attribute:
                                self.container_body.value})
        else:
            container_html = html_tree
        return container_html

    def get_error(self, html):
        error = html.find(
                   self.target_error.tag,
                   {self.target_error.attribute:
                   self.target_error.value})
        #error = element_html.get_text()
        return error

    def get_title_resume(self, html):
        element_html = html.find(
                        self.target_title_resume.tag,
                        {self.target_title_resume.attribute:
                        self.target_title_resume.value})
        title_resume = element_html.get_text()
        return title_resume

    def get_salary(self, html):
        element_html = html.find(
                        self.target_salary.tag,
                        {self.target_salary.attribute:
                        self.target_salary.value})
        list_numder = element_html.get_text()
        salary_list = re.findall(r'\d+', list_numder)
        salary_str = str().join(salary_list)
        salary = salary_str
        return salary

    def get_age(self, html):
        element_html = html.find(
                        self.target_age.tag,
                        {self.target_age.attribute:
                        self.target_age.value})
        list_numder = element_html.get_text()
        age_list = re.findall(r'\d{2}', list_numder)
        age_str = str().join(age_list)
        age = age_str
        return age

    def get_experience(self, html):
        element_html = html.find(
                        self.target_experience.tag,
                        {self.target_experience.attribute:
                        self.target_experience.value})
        experience = element_html.get_text()
        return experience

    def get_last_position(self, html):
        element_html = html.find(
                        self.target_last_position.tag,
                        {self.target_last_position.attribute:
                        self.target_last_position.value})
        last_position = element_html.get_text()
        return last_position

    def get_organization_name(self, html):
        element_html = html.find(
                        self.target_organization_name.tag,
                        {self.target_organization_name.attribute:
                        self.target_organization_name.value})
        organization_name = element_html.get_text()
        return organization_name

    def get_url(self, html):
        element_html = html.find(
                        self.target_url.tag,
                        {self.target_url.attribute:
                        self.target_url.value})
        url = element_html['href']
        return url

    def get_last_update(self, html):
        element_html = html.find(
                        self.target_last_update.tag,
                        {self.target_last_update.attribute:
                        self.target_last_update.value})
        last_update = element_html.get_text()
        return last_update

    def get_body(self, html):
        element_html = html.findAll(
                        self.target_body.tag,
                        {self.target_body.attribute:
                        self.target_body.value})
        #body = element_html.get_text()
        return element_html


# Parser for resume
class BaseParserResumeHTML(object):
    container_error = None
    container_head = None
    container_gender = None
    container_phone = None
    container_email = None
    container_city = None
    container_metro_station = None
    container_education = None
    container_experience = None
    container_full_name = None

    target_error = Expression()
    #target_head = Expression()
    target_gender = Expression()
    target_phone = Expression()
    target_email = Expression()
    target_city = Expression()
    target_metro_station = Expression()
    target_education = Expression()
    target_experience = Expression()
    target_first_name = Expression()
    target_last_name = Expression()
    target_middle_name = Expression()

    def _get_container(self, container_name, html):
        """Base container getter.
        Takes name of container element and html tree node
        """
        html_tree = BeautifulSoup(html, 'html.parser')
        container_attr = getattr(self, 'container_' + container_name, None)
        if container_attr:
            container_html = html_tree.find(
                container_attr.tag,
                {container_attr.attribute: container_attr.value}
            )
        else:
            container_html = html_tree
        return container_html

    def get_container_error(self, html):
        return self._get_container('error', html)

    def get_container_head(self, html):
        return self._get_container('head', html)

    def get_container_gender(self, html):
        return self._get_container('gender', html)

    def get_container_phone(self, html):
        return self._get_container('phone', html)

    def get_container_email(self, html):
        return self._get_container('email', html)

    def get_container_city(self, html):
        return self._get_container('city', html)

    def get_container_metro_station(self, html):
        return self._get_container('metro_station', html)

    def get_container_education(self, html):
        return self._get_container('education', html)

    def get_container_experience(self, html):
        return self._get_container('experience', html)

    def get_container_full_name(self, html):
        return self._get_container('full_name', html)

    def _get_target(self, target_name, html, return_html_node=False):
        """Base target getter.
        Takes name of target element and html tree node
        """
        target_attr = getattr(self, 'target_' + target_name, None)

        if not target_attr:
            raise ExpressionError("No goal %s specified" % target_name)

        element = html.find(
            target_attr.tag,
            {target_attr.attribute: target_attr.value}
        )

        if element:
            if not return_html_node:
                result = element.get_text()
            else:
                result = element
        else:
            result = None

        return result

    def get_error(self, html):
        return self._get_target('error', html, return_html_node=True)

    #def get_head(self, html):
    #    html_tree = BeautifulSoup(html, 'html.parser')
    #    element_html = html_tree.find(
    #               self.target_head.tag,
    #               {self.target_head.attribute:
    #               self.target_head.value})
    #    head = element_html.get_text()
    #    return head

    def get_gender(self, html):
        return self._get_target('gender', html)

    def get_phone(self, html):
        phone = self._get_target('phone', html)

        list_number = re.findall(r'\d{0,11}', phone)
        phone_number = str().join(list_number)
        number = '8' + phone_number[1:11]
        return number

    def get_email(self, html):
        return self._get_target('email', html)

    def get_city(self, html):
        return self._get_target('city', html)

    def get_metro_station(self, html):
        return self._get_target('metro_station', html)

    def get_education(self, html):
        return self._get_target('education', html)

    def get_experience(self, html):
        return self._get_target('experience', html)

    def _get_name_part(self, html, target_name, name_index):
        full_name = self._get_target(target_name, html)
        try:
            name = full_name.split(' ')[name_index]
        except IndexError:
            name = None

        return name

    # TODO: fix typo (firts -> first)
    def get_firts_name(self, html):
        return self._get_name_part(html, 'first_name', 1)

    def get_last_name(self, html):
        return self._get_name_part(html, 'last_name', 0)

    def get_middle_name(self, html):
        return self._get_name_part(html, 'middle_name', 2)


class BaseParserSearchAPI(object):
    container_error = None
    container_body = None
    container_title_resume = None
    container_salary = None
    container_age = None
    container_experience = None
    container_last_position = None
    container_organization_name = None
    container_url = None
    container_last_update = None

    target_error = None
    target_body = None
    target_title_resume = None
    target_salary = None
    target_age = None
    target_experience = None
    target_last_position = None
    target_organization_name = None
    target_url = None
    target_last_update = None

    def get_container_error(self, json_contant):
        json_data = json.loads(json_contant)
        if self.container_error is not None:
            container = json_data[self.container_error]
        else:
            container = json_data
        return container

    def get_container_body(self, json_contant):
        json_data = json.loads(json_contant)
        if self.container_body is not None:
            container = json_data[self.container_body]
        else:
            container = json_data
        return container

    def get_container_title_resume(self, json_contant):
        if self.container_title_resume is not None:
            container = json_contant[self.container_title_resume]
        else:
            container = json_contant
        return container

    def get_container_salary(self, json_contant):
        if self.container_salary is not None:
            container = json_contant[self.container_salary]
        else:
            container = json_contant
        return container

    def get_container_age(self, json_contant):
        if self.container_age is not None:
            container = json_contant[self.container_age]
        else:
            container = json_contant
        return container

    def get_container_experience(self, json_contant):
        if self.container_experience is not None:
            container = json_contant[self.container_experience]
        else:
            container = json_contant
        return container

    def get_container_last_position(self, json_contant):
        if self.container_last_position is not None:
            container = json_contant[self.container_last_position]
        else:
            container = json_contant
        return container

    def get_container_organization_name(self, json_contant):
        if self.container_organization_name is not None:
            container = json_contant[self.container_organization_name]
        else:
            container = json_contant
        return container

    def get_container_url(self, json_contant):
        if self.container_url is not None:
            container = json_contant[self.container_url]
        else:
            container = json_contant
        return container

    def get_container_last_update(self, json_contant):
        if self.container_last_update is not None:
            container = json_contant[self.container_last_update]
        else:
            container = json_contant
        return container

    def get_error(self, json_contant):
        if self.target_error is not None:
            error = json_contant[self.target_error]
        else:
            error = None
        return error

    def get_body(self, json_contant):
        body = json_contant[self.target_body]
        return body

    def get_title_resume(self, json_contant):
        title_resume = json_contant[self.target_title_resume]
        return title_resume

    def get_salary(self, json_contant):
        salary = json_contant[self.target_salary]
        return salary

    def get_age(self, json_contant):
        age = json_contant[self.target_age]
        return age

    def get_experience(self, json_contant):
        experience = json_contant[self.target_experience]
        return experience

    def get_last_position(self, json_contant):
        last_position = json_contant[self.target_last_position]
        return last_position

    def get_organization_name(self, json_contant):
        organization_name = json_contant[self.target_organization_name]
        return organization_name

    def get_url(self, json_contant):
        url = json_contant[self.target_url]
        return url

    def get_last_update(self, json_contant):
        last_update = json_contant[self.target_last_update]
        return last_update


#class BaseParserResumeAPI(object):
def parser_search(cls=None, html=None):
    if (cls is None) or (html is None):
        raise ParserError("Missing parsing class or html body")
    error_html = cls.get_container_error(html)
    error = cls.get_error(error_html)
    if error is not None:
        raise ParserError("Page not found")
    body_html = cls.get_container_body(html)
    try:
        bodys = cls.get_body(body_html)
    except AttributeError:
        raise ParserError("End sequence")
    resumes = []
    for body_item in bodys:
        resume = {}
        title_resume_html = cls.get_container_title_resume(body_item)
        try:
            title_resume = cls.get_title_resume(title_resume_html)
        except AttributeError:
            title_resume = None
        resume.setdefault('title_resume', title_resume)
        salary_html = cls.get_container_salary(body_item)
        try:
            salary = cls.get_salary(salary_html)
        except AttributeError:
            salary = None
        resume.setdefault('salary', salary)
        age_html = cls.get_container_age(body_item)
        try:
            age = cls.get_age(age_html)
        except AttributeError:
            age = None
        resume.setdefault('age', age)
        experience_html = cls.get_container_experience(body_item)
        try:
            experience = cls.get_experience(experience_html)
        except AttributeError:
            experience = None
        resume.setdefault('experience', experience)
        last_position_html = cls.get_container_last_position(body_item)
        try:
            last_position = cls.get_last_position(last_position_html)
        except AttributeError:
            last_position = None
        except IndexError:
            last_position = None
        resume.setdefault('last_position', last_position)
        organization_name_html = cls.get_container_organization_name(
                                    body_item)
        try:
            organization_name = cls.get_organization_name(
                                  organization_name_html)
        except AttributeError:
            organization_name = None
        except IndexError:
            organization_name = None
        resume.setdefault('organization_name', organization_name)
        url_html = cls.get_container_url(body_item)
        try:
            url = cls.get_url(url_html)
        except AttributeError:
            url = None
        resume.setdefault('url', url)
        last_update_html = cls.get_container_last_update(body_item)
        try:
            last_update = cls.get_last_update(last_update_html)
        except AttributeError:
            last_update = None
        resume.setdefault('last_update', last_update)
        resumes.append(resume)
    return resumes

def parser_resume(cls=None, html=None):
    if (cls is None) or (html is None):
        raise ParserError("Missing parsing class or html body")
    error_html = cls.get_container_error(html)
    error = cls.get_error(error_html)
    if error is not None:
        raise ParserError("Page not found")
    resume_data = {}
    #head_html = cls.get_container_head(html)
    #head = cls.get_head(html)

    gender_html = cls.get_container_gender(html)
    gender = cls.get_gender(gender_html)
    resume_data.setdefault('gender', gender)

    city_html = cls.get_container_city(html)
    city = cls.get_city(city_html)
    resume_data.setdefault('city', city)

    metro_station_html = cls.get_container_metro_station(html)
    metro_station = cls.get_metro_station(metro_station_html)
    resume_data.setdefault('metro_station', metro_station)

    phone_html = cls.get_container_phone(html)
    try:
        phone = cls.get_phone(phone_html)
    except IndexError:
        phone = None
    resume_data.setdefault('phone', phone)

    email_html = cls.get_container_email(html)
    email = cls.get_email(email_html)
    resume_data.setdefault('email', email)

    education_html = cls.get_container_education(html)
    education = cls.get_education(education_html)
    resume_data.setdefault('education', education)

    experience_html = cls.get_container_experience(html)
    experience = cls.get_experience(experience_html)
    resume_data.setdefault('experience', experience)

    full_name_html = cls.get_container_full_name(html)

    first_name = cls.get_firts_name(full_name_html)
    resume_data.setdefault('first_name', first_name)

    last_name = cls.get_last_name(full_name_html)
    resume_data.setdefault('last_name', last_name)

    middle_name = cls.get_middle_name(full_name_html)
    resume_data.setdefault('middle_name', middle_name)
    return resume_data


# Custom classes for recrut site.
class HhParserSearch(BaseParserSearchHTML):
    container_last_position = Expression(tag='div',
                                         attribute='class',
                                         value='output__indent')
    container_organization_name = Expression(tag='div',
                                             attribute='class',
                                             value='output__indent')
    container_body = Expression(tag='table',
                                attribute='data-qa',
                                value='resume-serp__results-search')

    target_error = Expression(tag='div',
                              attribute='class',
                              value='error')
    target_title_resume = Expression(tag='a',
                                     attribute='itemprop',
                                     value='jobTitle')
    target_salary = Expression(tag='span',
                               attribute='class',
                               value='output__compensation')
    target_age = Expression(tag='span',
                            attribute='class',
                            value='output__age')
    target_experience = Expression(
                            tag='div',
                            attribute='data-qa',
                            value='resume-serp__resume-excpirience-sum')
    target_last_position = Expression(
                      tag='span',
                      attribute='class',
                      value='bloko-link-switch bloko-link-switch_inherited')
    target_organization_name = Expression(tag='strong')
    target_url = Expression(tag='a',
                            attribute='itemprop',
                            value='jobTitle')
    target_last_update = Expression(tag='span',
                                    attribute='class',
                                    value='output__tab m-output__date')
    target_body = Expression(tag='tr',
                            attribute='itemscope',
                            value='itemscope')

    def get_url(self, html):
        element_html = html.find(
                        self.target_url.tag,
                        {self.target_url.attribute:
                        self.target_url.value})
        local_url = element_html['href']
        url = 'https://hh.ru' + local_url
        return url


class HhParserResume(BaseParserResumeHTML):
    container_education = Expression(tag='div',
                                     attribute='data-qa',
                                     value='resume-block-education')
    container_experience = Expression(tag='div',
                                      attribute='data-qa',
                                      value='resume-block-experience')
    container_full_name = Expression(tag='div',
                                     attribute='class',
                                     value='resume-header-name')
    container_gender = Expression(tag='div',
                                  attribute='class',
                                  value='resume-header-block')
    container_phone = Expression(tag='div',
                                 attribute='itemprop',
                                 value='contactPoints')
    container_email = Expression(tag='div',
                                 attribute='itemprop',
                                 value='contactPoints')
    container_city = Expression(tag='span',
                                attribute='itemprop',
                                value='address')
    container_metro_station = Expression(tag='span',
                                         attribute='itemprop',
                                         value='address')
    target_error = Expression(tag='div',
                              attribute='class',
                              value='error-content-wrapper')
    target_gender = Expression(tag='span',
                               attribute='itemprop',
                               value='gender')
    target_phone = Expression(tag='span',
                              attribute='itemprop',
                              value='telephone')
    target_email = Expression(tag='a',
                              attribute='itemprop',
                              value='email')
    target_city = Expression(tag='span',
                             attribute='itemprop',
                             value='addressLocality')
    target_metro_station = Expression(tag='span',
                             attribute='data-qa',
                             value='resume-personal-metro')
    target_education = Expression(
                tag='span',
                attribute='class',
                value='resume-block__title-text resume-block__title-text_sub'
                )
    target_experience = Expression(
                tag='span',
                attribute='class',
                value='resume-block__title-text resume-block__title-text_sub'
                )
    target_first_name = target_middle_name = target_last_name = Expression(
        tag='h1', attribute='itemprop', value='name')


class ZarplataParserSearch(BaseParserSearchAPI):
    container_experience = 'work_time_total'
    container_last_position = 'jobs'
    container_organization_name = 'jobs'

    target_body = 'resumes'
    target_title_resume = 'header'
    target_salary = 'wanted_salary_rub'
    target_age = 'age'
    target_experience = 'year'
    target_last_position = 'title'
    target_organization_name = 'title'
    target_url = 'url'
    target_last_update = 'mod_date'

    def get_last_position(self, json_contant):
        container = json_contant[0]['position']
        last_position = container[self.target_last_position]
        return last_position

    def get_organization_name(self, json_contant):
        container = json_contant[0]['company']
        organization_name = container[self.target_organization_name]
        return organization_name

    def get_url(self, json_contant):
        local_url = json_contant[self.target_url]
        url = 'https://www.zarplata.ru' + local_url
        return url


if __name__ == '__main__':
    '''
    url = 'https://hh.ru/resume/e9bb81ccff0337fea50039ed1f577a68444648'
    connect = urllib.urlopen(url)
    html_content = connect.read()
    connect.close()
    class_hh = HhParserResume()
    data = parser_resume(cls=class_hh, html=html_content)
    print(data)
    '''
    PATH_FILE = 'D:\git-project\parserHH\ResumesIdBase'
    namber_page = 0
    resume_list = []
    class_hh_search = HhParserSearch()
    begin_all_time = time.time()
    begin_ = time.time()
    while True:
        begin_time = time.time()
        searchSpeak = "https://hh.ru/search/resume?text=SQL&logic=normal&pos=full_text&exp_period=all_time&order_by=relevance&area=1&clusters=true&page=%i" %(namber_page)
        try:
            connect = urllib.urlopen(searchSpeak)
        except HTTPError:
            content_html = connect.read()
            connect.close()
            break
        content_html = connect.read()
        connect.close()
        try:
            resumes = parser_search(cls=class_hh_search, html=content_html)
        except ParserError:
            break
        resume_list += resumes
        end_time = time.time()
        spent = end_time - begin_time
        print('namber_page = %i, spent = %f' %(namber_page, spent))
        #if namber_page >= 50:
        #    break
        namber_page += 1
    end_all_time = time.time()
    spent_all = (end_all_time - begin_all_time) / 60
    print('spent >>', spent_all)
    print('Count = ', len(resume_list))
    resume_index = 0
    error_stak = 0
    date = datetime.datetime.utcnow()
    date_performance = date.strftime('%d%m%G%H%M')
    search_file = PATH_FILE + '\search_%s.csv' %(date_performance)
    error_file = PATH_FILE + '\error_%s.csv' %(date_performance)
    file_error = open(error_file, 'bw')
    begin_resumes =  time.time()
    for resume in resume_list:
        begin_resume = time.time()
        try:
            connect = urllib.urlopen(resume['url'])
        except URLError:
            error_stak += 1
            error_str = '%s;\n' %(resume['url'])
            format = error_str.encode('utf-8')
            file_error.write(format)
            continue
        html_content = connect.read()
        connect.close()
        class_hh = HhParserResume()
        data = parser_resume(cls=class_hh, html=html_content)
        resume.setdefault('gender', data['gender'])
        resume.setdefault('first_name', data['first_name'])
        resume.setdefault('last_name', data['last_name'])
        resume.setdefault('middle_name', data['middle_name'])
        resume.setdefault('phone', data['phone'])
        resume.setdefault('email', data['email'])
        resume.setdefault('city', data['city'])
        resume.setdefault('metro_station', data['metro_station'])
        resume.setdefault('education', data['education'])
        resume.setdefault('experience', data['experience'])
        end_resume = time.time()
        spant_resume = (end_resume - begin_resume) / 60
        print('Resume - %i, spent = %f' %(resume_index,
                                              spant_resume))
        resume_index += 1
    end_resumes = time.time()
    file_error.close()
    spent_resumes = (end_resumes - begin_resumes) / 60
    print('Spent >>', spent_resumes)
    end_ = time.time()
    spent_ = (end_ - begin_) / 60
    print('All spent time = %f' %(spent_))
    file_search = open(search_file, 'bw')
    for record_item in resume_list:
        try:
            data_str = '%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;\n' %(
                                record_item['title_resume'],
                                record_item['salary'],
                                record_item['age'],
                                record_item['experience'],
                                record_item['last_position'],
                                record_item['organization_name'],
                                record_item['url'],
                                record_item['last_update'],
                                record_item['gender'],
                                record_item['first_name'],
                                record_item['last_name'],
                                record_item['middle_name'],
                                record_item['phone'],
                                record_item['email'],
                                record_item['city'],
                                record_item['metro_station'],
                                record_item['education'])
            format = data_str.encode('utf-8')
            file_search.write(format)
        except KeyError:
            continue
    file_search.close()
    print('Count error = %i' %(error_stak))
    '''
    resume_list = []
    class_zp_search = ZarplataParserSearch()
    begin_all_time = time.time()
    searchSpeak ="https://api.zp.ru/v1/resumes/?geo_id=1177&limit=100&q=Siebel&state=1"
    connect = urllib.urlopen(searchSpeak)
    content_html = connect.read()
    connect.close()
    resumes = parser_search(cls=class_zp_search, html=content_html)
    resume_list += resumes
    end_all_time = time.time()
    spent_all = (end_all_time - begin_all_time) / 60
    print('spent >>', spent_all)
    print('Count = ', len(resume_list))
    file_search = open(
                    'D:\git-project\parserHH\ResumesIdBase\search_zp.txt',   'bw')
    for record_item in resume_list:
        print(record_item['age'])
        data_str = '%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' %(
                                record_item['title_resume'],
                                record_item['salary'],
                                record_item['age'],
                                record_item['experience'],
                                record_item['last_position'],
                                record_item['organization_name'],
                                record_item['url'],
                                record_item['last_update'])
        format = data_str.encode('utf-8')
        file_search.write(format)
    file_search.close()
    '''
