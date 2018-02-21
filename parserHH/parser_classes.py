import re
import time
import json
import datetime
import urllib.request as urllib
import requests

from requests import HTTPError
from urllib.error import HTTPError, URLError
from random import random
from bs4 import BeautifulSoup
from bs4 import NavigableString


class BaseException(Exception):
    def __init__(self, message):
        self.message = message


class ParserError(BaseException):
    pass


class SearchError(BaseException):
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
    root_url = None

    container_title_resume = None
    container_url = None
    container_last_update = None
    container_body = None

    target_title_resume = Expression()
    target_url = Expression()
    target_last_update = Expression()
    target_body = Expression()

    def _get_container(self, container_name, html):
        """Base container getter.
        Takes name of container element and html tree node
        """
        #html_tree = BeautifulSoup(html, 'html.parser')
        container_attr = getattr(self, 'container_' + container_name, None)
        if container_attr:
            container_html = html.find(
                container_attr.tag,
                {container_attr.attribute: container_attr.value}
            )
        else:
            container_html = html
        return container_html

    def _get_more_target(self, target_name, html):
        """Base targets getter.
        Takes name of target element
        Returned HTML nodes
        """
        target_attr = getattr(self, 'target_' + target_name, None)
        
        if not target_attr:
            raise ExpressionError("No goal %s specified" % target_name)
        
        if html: 
            elements = html.findAll(
                target_attr.tag,
                {target_attr.attribute: target_attr.value}
            )
        else:
            elements = None
            
        return elements    

    def get_container_title_resume(self, html):
        return self._get_container('title_resume', html)

    def get_container_url(self, html):
        return self._get_container('url', html)

    def get_container_last_update(self, html):
        return self._get_container('last_update', html)

    def get_container_body(self, html):
        html_tree = BeautifulSoup(html, 'html.parser')
        return self._get_container('body', html_tree)

    def _get_target(self, target_name, html, return_html_node=False):
        """Base target getter.
        Takes name of target element and html tree node
        """
        target_attr = getattr(self, 'target_' + target_name, None)

        if not target_attr:
            raise ExpressionError("No goal %s specified" % target_name)
        
        if html: 
            element = html.find(
                target_attr.tag,
                {target_attr.attribute: target_attr.value}
            )
        else:
            element = None

        if element:
            if not return_html_node:
                result = element.get_text()
            else:
                result = element
        else:
            result = None

        return result

    def get_body(self, html):
        return self._get_more_target('body', html)

    def get_title_resume(self, html):
        return self._get_target('title_resume', html)

    def get_url(self, html):
        element_html = self._get_target('url', html, return_html_node=True)
        root = self.root_url
        
        if element_html:
            if root:
                url = root + element_html['href']
            else:
                url = element_html['href']
        else:
            url = None
        return url

    def get_last_update(self, html):
        return self._get_target('last_update', html)


# Parser for resume
class BaseParserResumeHTML(object):
    find_cache = None##

    container_head = None
    container_gender = None
    container_phone = None
    container_email = None
    container_city = None
    container_metro_station = None
    container_salary = None##
    container_age = None##
    container_lentgh_of_work = None##
    container_experience = None##
    container_degree_of_education = None##
    container_education = None
    container_full_name = None
    container_key_words = None

    target_gender = Expression()
    target_phone = Expression()
    target_email = Expression()
    target_city = Expression()
    target_metro_station = Expression()
    target_salary = Expression()##
    target_age = Expression()##
    target_length_of_work = Expression()##
    target_experience = Expression()##
    target_experience_period = Expression()##
    target_experience_text = Expression()##
    target_last_position = Expression()##
    target_organization_name = Expression()##
    target_degree_of_education = Expression()##
    target_education = Expression()##
    target_education_year = Expression()##
    target_education_name = Expression()##
    target_education_profession = Expression()##
    target_first_name = Expression()
    target_last_name = Expression()
    target_middle_name = Expression()
    target_key_words = Expression()

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
        
    def _get_target(self, target_name, html, return_html_node=False):
        """Base target getter.
        Takes name of target element and html tree node
        """
        target_attr = getattr(self, 'target_' + target_name, None)

        if not target_attr:
            raise ExpressionError("No goal %s specified" % target_name)
        
        if html: 
            element = html.find(
                target_attr.tag,
                {target_attr.attribute: target_attr.value}
            )
        else:
            element = None

        if element:
            if not return_html_node:
                result = element.get_text()
            else:
                result = element
        else:
            result = None

        return result
        
    def _get_more_target(self, target_name, html):
        """Base targets getter.
        Takes name of target element
        Returned HTML nodes
        """
        target_attr = getattr(self, 'target_' + target_name, None)

        if not target_attr:
            raise ExpressionError("No goal %s specified" % target_name)

        if html: 
            elements = html.findAll(
                target_attr.tag,
                {target_attr.attribute: target_attr.value}
            )
        else:
            elements = None

        return elements

    def _get_children_elements(self, html_element):
        """Base method for get children element html_element
        Takes parent HTML - node
        Returned HTML - list children elements  
        """
        child_list = [
                child_item for child_item in html_element.children if
                child_item is not NavigableString
        ]
        return child_list

    def _get_position_element(self, target_name, html, position=0, 
                              hash_flag=False):
        """Base method get element from a given position
        For the case of repeated repetition
        Takes HTML, target_name and Position
        Returned HTML - node
        """
        if not self.find_hash:
            elements_list = self._get_more_target(target_name, html)

            if hash_flag:
                self.find_hash = elements_list

        else:
            elements_list = self.find_hash

        try:
            element = elements_list[position]
        except IndexError:
            element = None
        return element

    def _get_table_value(self, html_table, row=0, column=0):
        """Base method get target position (row, column) for table
        Takes HTML - Table
        Returned target element from a given position
        """
        row_elements = self._get_children_elements(html_table)
        column_elements = [
            self._get_children_elements(item) for item in
            row_elements
        ]
        
        try:
            column_element = column_elements[row][column]
        except IndexError:
            column_element = None

        if column_element:
            value = column_element.get_text()
        else:
            value = None

        return value

    def _get_list_value(self, html_list, siquence_numder=0):
        """Base method get value for HTML - list
        Takes HTML - list
        Returned item-list value
        """
        item_list = self._get_children_elements(html_list)
        try:
            item_list_tag = item_list[siquence_numder]
        except IndexError:
            item_list_tag = None
            
        if item_list_tag:
            value = item_list_tag.get_text()
        else:
            value = None
            
        return value

    def _get_name_part(self, html, target_name, name_index):
        full_name = self._get_target(target_name, html)
        
        if full_name:
            try:
                name = full_name.split(' ')[name_index]
            except IndexError:
                name = None
        else:
            name = None

        return name

    def get_container_degree_of_education(self, html):
        return self._get_container('degree_of_education', html)

    def get_container_salary(self, html):
        return self._get_container('salary', html)

    def get_container_age(self, html):
        return self._get_container('age', html)

    def get_container_length_of_work(self, html):
        return self._get_container('length_of_work', html)

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

    def get_container_key_words(self, html):
        return self._get_container('key_words', html)

    def get_salary(self, html):
        list_numder = self._get_target('salary', html)
        if list_numder:
            salary_list = re.findall(r'\d+', list_numder)
            salary_str = str().join(salary_list)
            salary = salary_str
        else:
            salary = None
        return salary

    def get_age(self, html):
        list_numder = self._get_target('age', html)
        if list_numder:
            age_list = re.findall(r'\d{2}', list_numder)
            age_str = str().join(age_list)
            age = age_str
        else:
            age = None
        return age

    def get_gender(self, html):
        return self._get_target('gender', html)

    def get_phone(self, html):
        phone = self._get_target('phone', html)
        if phone:    
            list_number = re.findall(r'\d{0,11}', phone)
            phone_number = str().join(list_number)
            number = '8' + phone_number[1:11]
        else:
            number = None
        return number

    def get_email(self, html):
        return self._get_target('email', html)

    def get_city(self, html):
        return self._get_target('city', html)

    def get_metro_station(self, html):
        return self._get_target('metro_station', html)

    def get_education(self, html):
        education_bloks = self._get_more_target('education', html)
        education_list = []
        
        if education_bloks:
            for item in education_bloks:
                education_item = {
                    target_name: self._get_target(target_name, item) for
                    target_name in ('education_year', 'education_name',
                                    'education_profession')
                }
                education_list.append(education_item)

        return education_list

    def get_degree_of_education(self, html):
        return self._get_target('degree_of_education', html)

    def get_length_of_work(self, html):
        return self._get_target('length_of_work', html)

    def get_experience(self, html):
        """Method for get all experience data 
        """
        experience_bloks = self._get_more_target('experience', html)
        experience_list = []
        
        if experience_bloks:
            for item in experience_bloks:
                experience_item = {
                    target_name: self._get_target(target_name, item) for
                    target_name in ('experience_text', 'last_position',
                                    'experience_period', 'organization_name')##
                }
                experience_list.append(experience_item)

        return experience_list

    def get_firts_name(self, html):
        return self._get_name_part(html, 'first_name', 1)

    def get_last_name(self, html):
        return self._get_name_part(html, 'last_name', 0)

    def get_middle_name(self, html):
        return self._get_name_part(html, 'middle_name', 2)

    def get_key_words(self, html):    
        elements = self._get_more_target('key_words', html)
        key_words_list = []
        
        if elements:
            for item_element in elements:
                key_word = item_element.get_text()
                key_words_list.append(key_word)
        
        return key_words_list


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

    body_html = cls.get_container_body(html)
    bodys = cls.get_body(body_html)

    if not bodys:
        raise ParserError("End sequence")

    resumes = []
    for body_item in bodys:
        resume = {}
        title_resume_html = cls.get_container_title_resume(body_item)
        title_resume = cls.get_title_resume(title_resume_html)
        resume.setdefault('title_resume', title_resume)
        url_html = cls.get_container_url(body_item)
        url = cls.get_url(url_html)
        resume.setdefault('url', url)
        last_update_html = cls.get_container_last_update(body_item)
        last_update = cls.get_last_update(last_update_html)
        resume.setdefault('last_update', last_update)
        resumes.append(resume)
    return resumes

def parser_resume(cls=None, html=None):
    if (cls is None) or (html is None):
        raise ParserError("Missing parsing class or html body")

    resume_data = {}

    salary_html = cls.get_container_salary(html)
    salary = cls.get_salary(salary_html)
    resume_data.setdefault('salary', salary)

    age_html = cls.get_container_age(html)
    age = cls.get_age(age_html)
    resume_data.setdefault('age', age)

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
    except ExpressionError:
        phone = None
    resume_data.setdefault('phone', phone)

    email_html = cls.get_container_email(html)
    try:
        email = cls.get_email(email_html)
    except ExpressionError:
        email = None
    resume_data.setdefault('email', email)

    degree_of_education_html = cls.get_container_degree_of_education(html)
    degree_of_education = cls.get_degree_of_education(
                                                 degree_of_education_html
    )
    resume_data.setdefault('degree_of_education', degree_of_education)

    education_html = cls.get_container_education(html)
    education = cls.get_education(education_html)
    resume_data.setdefault('education', education)

    lentgh_of_work_html = cls.get_container_length_of_work(html)
    lentgh_of_work = cls.get_length_of_work(lentgh_of_work_html)
    resume_data.setdefault('lentgh_of_work', lentgh_of_work)
    
    experience_html = cls.get_container_experience(html)
    experience = cls.get_experience(experience_html)
    resume_data.setdefault('experience', experience)

    full_name_html = cls.get_container_full_name(html)

    try:
        first_name = cls.get_firts_name(full_name_html)
    except ExpressionError:
        first_name = None
    resume_data.setdefault('first_name', first_name)

    try:
        last_name = cls.get_last_name(full_name_html)
    except ExpressionError:
        last_name = None
    resume_data.setdefault('last_name', last_name)

    try:
        middle_name = cls.get_middle_name(full_name_html)
    except ExpressionError:
        middle_name = None
    resume_data.setdefault('middle_name', middle_name)

    key_words_html = cls.get_container_key_words(html)
    key_words = cls.get_key_words(key_words_html)
    resume_data.setdefault('key_words', key_words)

    return resume_data


# Custom classes for recrut site.
class HhParserSearch(BaseParserSearchHTML):
    root_url = 'https://hh.ru'

    container_body = Expression(tag='table',
                                attribute='data-qa',
                                value='resume-serp__results-search')

    target_title_resume = Expression(tag='a',
                                     attribute='itemprop',
                                     value='jobTitle')
    target_url = Expression(tag='a',
                            attribute='itemprop',
                            value='jobTitle')
    target_last_update = Expression(tag='span',
                                    attribute='class',
                                    value='output__tab m-output__date')
    target_body = Expression(tag='tr',
                             attribute='itemscope',
                             value='itemscope')


class HhParserResume(BaseParserResumeHTML):
    container_education = Expression(tag='div',
                                     attribute='data-qa',
                                     value='resume-block-education')
    container_degree_of_education = Expression(tag='div',
                                        attribute='data-qa',
                                        value='resume-block-education')
    container_experience = Expression(tag='div',
                                      attribute='data-qa',
                                      value='resume-block-experience')
    container_lentgh_of_work = Expression(tag='div',
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
    target_salary = Expression(tag='span',
                               attribute='class',
                               value='resume-block__salary')
    target_age = Expression(tag='span',
                            attribute='data-qa',
                            value='resume-personal-age')
    target_length_of_work = Expression(
                tag='span',
                attribute='class',
                value='resume-block__title-text resume-block__title-text_sub'
    )
    target_degree_of_education = Expression(
                tag='span',
                attribute='class',
                value='resume-block__title-text resume-block__title-text_sub'
    )
    target_education = Expression(tag='div',
                                  attribute='class',
                                  value='resume-block-item-gap')
    target_education_year = Expression(
      tag='div',
      attribute='class',
      value='bloko-column bloko-column_s-2 bloko-column_m-2 bloko-column_l-2'
    )
    target_education_name = Expression(tag='div',
                                       attribute='data-qa',
                                       value='resume-block-education-name')
    target_education_profession = Expression(
                                  tag='div',
                                  attribute='data-qa',
                                  value='resume-block-education-organization'
    )                
    target_experience = Expression(tag='div',
                                   attribute='class',
                                   value='resume-block-item-gap')
    target_experience_period = Expression(
                              tag='div',
                              attribute='class',
                              value='resume-block__experience-timeinterval'
    )
    target_experience_text = Expression(
                                tag='div',
                                attribute='data-qa',
                                value='resume-block-experience-description'
    )
    target_last_position = Expression(
                                    tag='div',
                                    attribute='data-qa',
                                    value='resume-block-experience-position'
    )
    target_organization_name = Expression(tag='div',
                                          attribute='itemprop',
                                          value='name')
    target_first_name = target_middle_name = target_last_name = Expression(
        tag='h1', attribute='itemprop', value='name')
    target_key_words = Expression(
      tag='span',
      attribute='class',
      value='bloko-tag bloko-tag_inline bloko-tag_countable Bloko-TagList-Tag'
    )


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


class SuperjobParserSearch(BaseParserSearchHTML):
    container_last_update = Expression(
                tag='div',
                attribute='class',
                value='sj_block m_b_2 ResumeListElementNew_history'
    )  

    target_title_resume = Expression(tag='a',
                                     attribute='target',
                                     value='_blank')
    target_url = Expression(tag='a',
                            attribute='target',
                            value='_blank')
    target_last_update = Expression(tag='span',
                                    attribute='class',
                                    value='sj_text m_small')
    target_body = Expression(tag='div',
                             attribute='class',
                             value='ResumeListElementNew js-resume-item')
    '''
    def get_salary(self, html):
        if html:
            list_elements = html.findAll(
                    self.target_salary.tag,
                    {self.target_salary.attribute, sself.target_salary}
            )
            if list_elements:
                try:
                    element_salary = list_elements[0]
                    salary_inner = element_salary.get_text()
                    salary_list = re.findall(r'\d+', salary_inner)
                    salary_str = str().join(salary_list)
                    salary = salary_str
                except IndexError:
                    salary = None
            else:
                salary = None

        return salary
    '''

    def get_age(self, html):
        if html:
            list_elements = html.findAll(
                        self.target_age.tag,
                        {self.target_age.attribute, self.target_age.value}
            )
            if list_elements:
                try:
                    element_age = list_elements[1]
                    age_inner = element_age.get_text()
                    age_list = re.findall(r'\d{2}', age_inner)
                    age_str = str().join(age_list)
                    age = age_str
                except IndexError:
                    age = None
            else:
                age = None
                
            return age

    def get_experience(self, html):
        if html:
            list_elements = html.findAll(
              self.target_experience.tag,
              {self.target_experience.attribute, self.target_experience.value}
            )
            if list_elements:
                try:
                    element_experience = list_elements[-1]
                    experience = element_experience.get_text()
                except IndexError:
                    experience = None
            else:
                experience = None
        return experience

    def get_last_position(self, html):
        raw_data = self._get_target('last_position', html)
        if raw_data:
            list_char = re.findall(
                "[^<span class='sj_match_highlight'>][^</span>]",
                raw_data
            )
            last_position = str().join(list_char)
        else:
            last_position = None
         
        return last_position


class SuperjobParserResume(BaseParserResumeHTML):
    container_salary = Expression(tea='div',
                                  attribute='class',
                                  value='ResumeMainHRNew_content')
    container_age =  Expression(tea='div',
                                attribute='class',
                                value='ResumeMainHRNew_content')
    container_degree_of_education = Expression(tea='div',
                                        attribute='class',
                                        value='ResumeMainHRNew_content')
    container_lentgh_of_work = Expression(tag='div',
                                          attribute='class',
                                          value='sj_block m_b_2 sj_h3')
    container_gender = Expression(tea='div',
                                  attribute='class',
                                  value='ResumeMainHRNew_content')
    container_phone = Expression(tea='div',
                                 attribute='class',
                                 value='ResumeMainHRNew_content')
    container_email = Expression(tea='div',
                                 attribute='class',
                                 value='ResumeMainHRNew_content')
    container_city = Expression(tea='div',
                                 attribute='class',
                                 value='ResumeMainHRNew_content')
    container_metro_station = Expression(
                                tea='div',
                                attribute='class',
                                value='ResumeMainHRNew_content'
    )
    container_education = Expression(tea='div',
                                     attribute='class',
                                     value='ResumeMainHRNew_content')
    container_experience = Expression(tea='div',
                                      attribute='class',
                                      value='ResumeDetailsNew_row')
    container_full_name = Expression(tea='div',
                                     attribute='class',
                                     value='ResumeMainHRNew_content')
    container_key_words = None

    target_salary = Expression(tag='span',
                               attribute='class',
                               value='h_font_weight_medium')
    target_age = Expression(tag='div')
    target_gender = Expression(tag='div')
    target_phone = Expression(tag='div',
                              attribute='class',
                              value='m_t_2')
    target_email = Expression(tag='div',
                              attribute='class',
                              value='m_t_0')
    target_city = Expression(tag='div')
    target_metro_station = Expression(tag='div')
    target_degree_of_education = Expression(tag='div',
                                            attribute='class',
                                            value='sj_block m_b_2 sj_h3')
    target_education = Expression(tag='div',
                                  attribute='class',
                                  value='ResumeDetailsNew_row')
    target_education_year = Expression(tag='div',
                                       attribute='class',
                                       value='ResumeDetailsNew_left')
    target_education_name = Expression(tag='div',
                                       attribute='class',
                                       value='h_font_weight_medium')
    target_education_profession = Expression(tag='div')
    target_length_of_work = Expression(tag='div',
                                       attribute='class',
                                       value='sj_block m_b_2 sj_h3')
    target_experience = Expression(tag='div',
                                   attribute='class',
                                   value='sj_block m_b_2')
    target_experience_period = Expression(
                        tag='div',
                        attribute='class',
                        value='ResumeDetailsNew_left h_word_wrap_break_word'
    )
    target_experience_text = Expression(tag='div',
                                        attribute='class',
                                        value='sj_block m_t_2')
    target_last_position = Expression(tag='div',
                                      attribute='class',
                                      value='h_font_weight_medium')
    target_organization_name = Expression(tag='div')
    target_first_name = Expression(tag='div',
                                   attribute='class',
                                   value='sj_h3')
    target_last_name = Expression(tag='div',
                                   attribute='class',
                                   value='sj_h3')
    target_middle_name = Expression(tag='div',
                                   attribute='class',
                                   value='sj_h3')
    target_key_words = Expression(tag='div',
                                  attribute='class',
                                  value='h_word_wrap_break_word')


class AvitoParserSearch(BaseParserSearchHTML):
    root_url = 'https://www.avito.ru'
    
    target_title_resume = Expression(tag='a',
                                     attribute='class',
                                     value='item-description-title-link')

    target_url = Expression(tag='a',
                            attribute='class',
                            value='item-description-title-link')
    target_last_update = Expression(tag='div',
                                    attribute='class',
                                    value='date c-2')
    target_body = Expression(tag='div',
                             attribute='class',
                             value='description item_table-description')

    #def _get_position_target(slf, target_name, html, 
    #                         element_position, target_position):
    #    """
    #        Base method for pars case:
    #        <ul>
    #          <li class="...">...</li>
    #          .......................
    #          <li class="...">...</li>
    #          .......................
    #          <li class="...">...</li>
    #        </ul>
    #    """
    #    elemts = self._get_more_target(target_name, html)
    #    
    #    if elemts:
    #        try:
    #            target_element = elemts[element_position]
    #        except IndexError:
    #            target_element = None
    #        
    #        if target_element:
    #            target_value = target_element.get_text()
    #            list_value = target_value.split(',')
    #            try:
    #                target_data = list_value[target_position]
    #            except IndexError:
    #                target_data = None
    #        else:
    #            target_data = None
    #    else:
    #        target_data = None
    #    
    #    return target_data
        
    #def get_age(self, html):
    #    target_element = self._get_position_target('age', html, 0, 1)
    #        
    #    if target_element:
    #        age_list = re.findall(r'\d{2}', target_element)
    #        age_str = str().join(age_list)
    #        age = age_str
    #    else:
    #        age = None
    #        
    #    return age
        
    #def get_experience(self, html):
    #    target_element = self._get_position_target('experience', html, 0, 2)
    #        
    #    if target_element:
    #        experience_list = re.findall(r'\d{2}', target_element)
    #        experience_str = str().join(experience_list)
    #        experience = experience_str
    #    else:
    #        experience = None
    #        
    #    return experience
    #    
    #def get_url(self, html):    
    #    element_html = self._get_target('url', html, return_html_node=True)
    #    if element_html:
    #        local_url = element_html['href']
    #        url = 'https://www.avito.ru' + local_url
    #    else:
    #        url = None
    #    return url


class AvitoParserResume(BaseParserResumeHTML):
    container_gender = Expression(
                              tag='div',
                              attribute='class',
                              value='item-params item-params_type-one-colon'
    )
    container_phone = Expression(tag='div',
                                 attribute='class',
                                 value='item-view-right')
    container_email = Expression(tag='div',
                                attribute='class',
                                value='item-view-right')
    container_city = Expression(tag='div',
                                attribute='class',
                                value='item-view-right')
    container_metro_station = Expression(tag='div',
                                         attribute='class',
                                         value='item-view-right')
    container_education = Expression(
                            tag='div',
                            attribute='class',
                            value='item-params item-params_type-one-colon'
    )
    container_salary = Expression(tag='div',
                                  attribute='class',
                                  value='item-view-right')
    container_age = Expression(tag='div',
                               attribute='class',
                               value='item-params item-params_type-one-colon')
    container_length_of_work = Expression(
                                tag='div',
                                attribute='class',
                                value='item-params item-params_type-one-colon'
    )
    container_experience = None##
    container_degree_of_education = Expression(
                                tag='div',
                                attribute='class',
                                value='item-params item-params_type-one-colon'
    )
    container_full_name = None
    container_key_words = Expression(tag='div',
                                     attribute='itemprop',
                                     value='description')

    target_gender = Expression(
                        tag='li',
                        attribute='class',
                        value='item-params-list-item'
    )
    target_phone = None
    target_email = None
    target_city = Expression(
                        tag='div',
                        attribute='class',
                        value='seller-info-value')
    target_metro_station = Expression(tag='div',
                                      attribute='class',
                                      value='seller-info-value')
    target_first_name = None
    target_last_name = None
    target_middle_name = None
    target_salary = Expression(
                            tag='span',
                            attribute='class',
                            value='price-value-string js-price-value-string')##
    target_age = Expression(tag='ul',
                            attribute='class',
                            value='item-params-list')
    target_lentgh_of_work = Expression(tag='ul',
                                       attribute='class',
                                       value='item-params-list')
    target_degree_of_education =  Expression(tag='ul',
                                             attribute='class',
                                             value='item-params-list')
    target_experience = Expression(tag='div',
                                   attribute='class',
                                   value='resume-params')##
    target_experience_period = Expression(tag='div',
                                          attribute='class',
                                          value='resume-params-work-date')
    target_experience_text = Expression(tag='p',
                                        attribute='class',
                                        value='resume-params-text')
    target_last_position = Expression(tag='div',
                                      attribute='class',
                                      value='resume-params-title')##
    target_organization_name = Expression(tag='div',
                                      attribute='class',
                                      value='resume-params-title')
    
    target_education = Expression(tag='div',
                                  attribute='class',
                                  value='resume-params')
    target_education_year = Expression(tag='td',
                                       attribute='class',
                                       value='resume-params-left')##
    target_education_name = Expression(tag='div',
                                       attribute='class',
                                       value='resume-params-title')##
    target_education_profession = Expression(tag='p',
                                             attribute='class',
                                             value='resume-params-text')##

    target_key_words = Expression(tag='p')


class RabotaParserSearch(BaseParserSearchHTML):
    container_last_update = Expression(
                                tag='div',
                                attribute='class',
                                value='h-box-wrapper__centercol'
    )

    target_title_resume = Expression(tag='a',
                                     attribute='target',
                                     value='_blank')
    target_url = Expression(tag='a',
                            attribute='target',
                            value='_blank')
    target_last_update = Expression(
                            tag='p',
                            attribute='class',
                            value='box-wrapper__descr_12grey mt_10'
    )
    target_body = Expression(tag='div',
                             attribute='class',
                             value='h-box-wrapper')


class RabotaParserResume(BaseParserResumeHTML):
    container_metro_station = Expression(tag='div',
                                         attribute='id',
                                         value='resume_metro_list')
    container_education = Expression(tag='div',
                                     attribute='class',
                                     value='w100 res-card-tbl')
    container_experience = Expression(tag='div',
                                   attribute='class',
                                   value='b-main-info b-experience-list')
    container_full_name = None
    container_key_words = None
    container_salary = Expression(tag='div',
                                  attribute='class',
                                  value='b-main-info')
    container_age = None##
    container_length_of_work = Expression(tag='div',
                                          attribute='class',
                                          value='b-main-info')
    container_experience = None##
    container_degree_of_education = None##

    target_gender = Expression(tag='p',
                               attribute='class',
                               value='b-sex-age')
    target_phone = None
    target_email = None
    target_city = Expression(tag='p',
                             attribute='class',
                             value='b-city-info mt_10')
    target_metro_station = Expression(tag='span',
                                      attribute='class',
                                      value='name longname')
    target_first_name = None
    target_last_name = None
    target_middle_name = None
    target_key_words = None
    
    target_salary = Expression(tag='span',
                               attribute='class',
                               value='text_24 salary nobr')##
    target_age = Expression(tag='p',
                            attribute='class',
                            value='b-sex-age')
    target_lentgh_of_work = Expression(tag='span',
                                       attribute='class',
                                       value='text_18 bold exp-years')##
    target_experience = Expression(tag='div',
                                   attribute='class',
                                   value='res-card-tbl-row')
    target_experience_period = Expression(tag='span',
                                          attribute='class',
                                          value='gray9_text')##
    target_experience_text = Expression(tag='p',
                                        attribute='class',
                                        value='lh_20 p-res-exp')
    target_last_position = Expression(tag='p',
                                      attribute='class',
                                      value='last-position-name')
    target_organization_name = Expression(tag='p',
                                          attribute='class',
                                          value='company-name')
    target_degree_of_education = Expression(tag='span',
                                            attribute='class',
                                            value='bold edu-type')
    target_education = Expression(tag='div',
                                  attribute='class',
                                  value='res-card-tbl-row')
    target_education_profession = Expression(
                                        tag='div',
                                        attribute='class',
                                        value='mt_5 gray9_text profes-info'
    )
    target_education_year = Expression(tag='div',
                                       attribute='class',
                                       value='edu-year')
    target_education_name = Expression(tag='p',
                                       attribute='class',
                                       value='mt_4 lh_20 school-name')##

    def _get_choice_target(self, target_name, html,
                           psition, separator=','):
        data_str = self._get_target(target_name, html)
        
        if data_str:
            data_list = data_str.split(separator)
            try:
                value = data_list[psition]
            except IndexError:
                value = None
        else:
            value = None
            
        return value
        
    def get_age(self, html):
        age_str = self._get_choice_target('age', html, 0)
        
        if age_str:
            age_list = re.findall('\d{2}', age_str)
            try:
                age = age_list[0]
            except IndexError:
                age = None
        else:
            age = None
            
        return age
        
    def get_gender(self, html):
        gender_str = self._get_choice_target('gender', html, 1)
        
        if gender_str:
            gender_list = re.findall('\S', gender_str)
            gender = str().join(gender_list)
        else:
            gender = None
            
        return gender


class FarpostParserSearch(BaseParserSearchHTML):
    root_url = 'https://www.farpost.ru'

    container_title_resume = Expression(tag='div',
                                        attribute='class',
                                        value='priceCell')
    container_last_update = Expression(tag='div',
                                       attribute='class',
                                       value='priceCell')

    target_title_resume = Expression(tag='a',
                                     attribute='class',
                                     value='bulletinLink')
    target_url = Expression(tag='a',
                            attribute='class',
                            value='bulletinLink')
    target_last_update = Expression(tag='td',
                                    attribute='class',
                                    value='dateCell')
    target_body = Expression(tag='tr',
                             attribute='class',
                             value='bull-item')


class FarpostParserResume(BaseParserResumeHTML):
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
    container_key_words = None

    target_error = Expression(tag='div',
                              attribute='class',
                              value='notificationPlate')
    target_gender = Expression(tag='span',
                               attribute='data-field',
                               value='sex-maritalStatus-hasChildren'
    )
    target_phone = Expression(tag='div',
                              attribute='class',
                              value='new-contacts__td new-contact__phone')
    target_email = Expression(tag='a',
                              attribute='class',
                              value='new-contact__email')
    target_city = Expression(tag='span',
                             attribute='data-field',
                             value='district')
    target_metro_station = Expression()
    target_education = Expression()
    target_experience = Expression()
    target_first_name = None
    target_last_name = None
    target_middle_name = None
    target_key_words = Expression(tag='p',
                                  attribute='data-field',
                                  value='resumeSkills')


class RabotavgorodeParserSearch(BaseParserSearchHTML):
    target_title_resume = Expression(tag='a',
                                     attribute='target',
                                     value='_blank')
    target_url = Expression(tag='a',
                            attribute='target',
                            value='_blank')
    target_last_update = Expression(tag='div',
                                    attribute='class',
                                    value='date')
    target_body = Expression(tag='div',
                             attribute='class',
                             value='info')


class RabotavgorodeParserResume(BaseParserResumeHTML):
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
    container_key_words = None

    target_error = None
    target_gender = Expression(tag='td')
    target_phone = Expression(tag='td')
    target_email = Expression(tag='td')
    target_city = Expression(tag='td')
    target_metro_station = Expression(tag='td')
    target_education = Expression(tag='td')
    target_experience = Expression(tag='td')
    target_first_name = Expression(tag='td')
    target_last_name =Expression(tag='td')
    target_middle_name = Expression(tag='td')
    target_key_words = Expression(tag='td')


class SearchBase(object):
    search_pattern = None
    search_iterator = None
    search_text = None
    search_step = 1
    search_start = 0

    source = None
    preview = False
    search_class = None
    resume_class = None

    def generate_search_url(self, search_str):
        pattern = getattr(self, 'search_pattern', None)
        iterator = getattr(self, 'search_iterator', None)
        search_url = pattern %(search_str)
        search_url += iterator
        return search_url

    def next_step(self, search_url=None, namber_page=0):
        if not search_url:
            raise SearchError("search_url is None")
        return search_url %(namber_page)
    
    def search(self, search_str=None, session=None, resume_list=[], 
               reload_error_flag=False, update_flad=False,
               debug_flag=False):

        if not(reload_error_flag and update_flad):

            if not search_str:
                raise SearchError("Search_str is None")

            search_url = self.generate_search_url(search_str)  
            search_pars = getattr(self, 'search_class', None)
            search_step = getattr(self, 'search_step', None)
            source_name = getattr(self, 'source', None)
            preview_flag = getattr(self, 'preview', None)
            namber_page = getattr(self, 'search_start', None)

            if not session:
                session = requests.Session()

            while True:
                search_speak = self.next_step(search_url, namber_page)
                request_object = requests.Request('GET', search_speak)
                request = session.prepare_request(request_object)
                responce = session.send(request)
                content_html = responce.text
                responce.close()

                if responce.status_code != 200:
                    break

                try:
                    begin_pars = time.time()
                    resumes = parser_search(cls=search_pars, 
                                            html=content_html)
                    end_pars = time.time()
                    spent = end_pars - begin_pars
                except ParserError:
                    break
                resume_list += resumes
                namber_page += search_step
                
                if debug_flag:
                    print('namber_page = %i, spent = %f' %(namber_page, 
                                                           spent))
                    if namber_page >= search_step * 10:
                        break

        resume_data_list = []
        resume_error_list = []

        if len(resume_list) > 0:
            resume_pars =  getattr(self, 'resume_class', None)
            for resume in resume_list:
                resume_url = resume['url']
                resume_reque_obj = requests.Request('GET', resume_url)
                resume_request = session.prepare_request(resume_reque_obj)
                try:
                    resume_responce = session.send(resume_request)
                except HTTPError:
                    resume_error_list += resume
                    continue
                resume_html = resume_responce.text
                resume_responce.close()
                try:
                    resume_data = parser_resume(cls=resume_pars, html=resume_html)
                except ParserError:
                    resume_error_list += resume
                    continue
                resume_data.setdefault('title_resume', resume['title_resume'])
                resume_data.setdefault('url', resume['url'])
                resume_data.setdefault('last_update', resume['last_update'])
                resume_data.setdefault('source', source_name)
                resume_data.setdefault('preview', preview_flag)
                resume_data_list.append(resume_data)

        return resume_data_list, resume_error_list


class SearchHh(SearchBase):
    search_pattern = 'https://hh.ru/search/resume?exp_period=all_time&'
    search_pattern += 'order_by=relevance&text=%s&pos=full_text&logic='
    search_pattern += 'normal&clusters=true'
    search_iterator = '&page=%i'
    search_step = 1
    search_start = 0

    source = 'hh.ru'
    preview = False
    search_class = HhParserSearch()
    resume_class = HhParserResume()


class SearchSj(SearchBase):
    search_pattern = 'https://www.superjob.ru/resume/search_resume.html?'
    search_pattern += 'sbmit=1&c[]=1&keywords[0][srws]=7&keywords[0]'
    search_pattern += '[skwc]=and&keywords[0][keys]=%s'
    search_iterator = '&search_hesh=%i&main=1&page=%i'
    search_step = 1
    search_start = 0

    source = 'www.superjob.ru'
    preview = True
    search_class = SuperjobParserSearch()
    resume_class = SuperjobParserResume()

    def next_step(self, search_url=None, namber_page=0):
        if not search_url:
            raise SearchError("search_url is None")
        random_sequence = random()*10**15
        hesh = int(random_sequence)
        return search_url %(hesh, namber_page)


class SearchAvito(SearchBase):
    search_pattern = 'https://www.avito.ru/rossiya/rezume?p=%i&q=%s'
    search_iterator = None
    search_step = 1
    search_start = 0

    source = 'www.avito.ru'
    preview = True
    search_class = AvitoParserSearch()
    resume_class = AvitoParserResume()

    def generate_search_url(self, search_str):
        self.search_text = search_str
        return getattr(self, 'search_pattern', None)

    def next_step(self, search_url=None, namber_page=0):
        if not search_url:
            raise SearchError("search_url is None")

        search_str = getattr(self, 'search_text', None)
        return search_url %(namber_page, search_str)


'''
def search_sj(search_str, session=None, resume_list=[], 
              reload_error_flag=False, update_flad=False):
    if not(reload_error_flag and update_flad):
        search_url = 'https://www.superjob.ru/resume/search_resume.html?'
        search_url += 'sbmit=1&c[]=1&keywords[0][srws]=7&keywords[0]'
        search_url += '[skwc]=and&keywords[0][keys]=%s'
        search_url = search_url %(search_str)
        search_url += '&search_hesh=%i&main=1&page=%i'
        class_sj_search = SuperjobParserSearch()
        namber_page = 0

        if not session:
            session = requests.Session()

        while True:
            random_sequence = random()*10**15
            hesh = int(random_sequence)
            search_peak = search_url %(hesh, namber_page)
            request_object = requests.Request('GET', search_peak)
            request = session.prepare_request(request_object)
            responce = session.send(request)
            content_html = responce.text
            responce.close()

            if responce.status_code != 200:
                break

            try:
                resumes = parser_search(cls=class_sj_search, html=content_html)
            except ParserError:
                break
            resume_list += resumes
            namber_page += 1

    if len(resume_list) > 0:
        resume_data_list = []
        resume_error_list = []
        class_sj = SuperjobParserResume()
        for resume in resume_list:
            resume_url = resume['url']
            resume_reque_obj = requests.Request('GET', resume_url)
            resume_request = session.prepare_request(resume_reque_obj)
            try:
                resume_responce = session.send(resume_request)
            except HTTPError:
                resume_error_list += resume
                continue
            resume_html = resume_responce.text
            resume_responce.close()
            try:
                resume_data = parser_resume(cls=class_sj, html=html_content)
            except ParserError:
                resume_error_list += resume
                continue
            resume_data.setdefault('title_resume', resume['title_resume'])
            resume_data.setdefault('url', resume['url'])
            resume_data.setdefault('last_update', resume['last_update'])
            resume_data_list += resume_data

    return resume_data_list, resume_error_list  

def search_avito(search_str, session=None, resume_list=[], 
              reload_error_flag=False, update_flad=False):

    if not(reload_error_flag and update_flad):
        search_url = 'https://www.avito.ru/rossiya/rezume?p=%i&q=%s'
        class_avito_search = AvitoParserSearch()
        namber_page = 0

        if not session:
            session = requests.Session()

        while True:
            search_peak = search_url %(namber_page, search_str)
            request_object = requests.Request('GET', search_peak)
            request = session.prepare_request(request_object)
            responce = session.send(request)
            content_html = responce.text
            responce.close()

            if responce.status_code != 200:
                break

            try:
                resumes = parser_search(cls=class_hh_search, 
                                        html=content_html)
            except ParserError:
                break
            resume_list += resumes
            namber_page += 1

    if len(resume_list) > 0:
        resume_data_list = []
        resume_error_list = []
        class_avito =  AvitoParserResume()
        for resume in resume_list:
            resume_url = resume['url']
            resume_reque_obj = requests.Request('GET', resume_url)
            resume_request = session.prepare_request(resume_reque_obj)
            try:
                resume_responce = session.send(resume_request)
            except HTTPError:
                resume_error_list += resume
                continue
            resume_html = resume_responce.text
            resume_responce.close()
            try:
                resume_data = parser_resume(cls=class_avito, html=resume_html)
            except ParserError:
                resume_error_list += resume
                continue
            resume_data.setdefault('title_resume', resume['title_resume'])
            resume_data.setdefault('url', resume['url'])
            resume_data.setdefault('last_update', resume['last_update'])
            resume_data_list += resume_data

    return resume_data_list, resume_error_list

def search_Rabota(search_str, session=None, resume_list=[], 
              reload_error_flag=False, update_flad=False):

    if not(reload_error_flag and update_flad):
        search_url = 'https://www.rabota.ru/v3_searchResumeByParamsResults'
        search_url += '.html?action=search&area=v3_searchResumeByParams'
        search_url += 'Results&p=-2005&w=&qk[0]=%s&qot[0]=1&qsa[0][]=1&sf='
        search_url += '&st=&cu=2&krl[]=3&krl[]=4&krl[]=284&krl[]=25&'
        search_url += 'krl[]=328&krl[]=231&krl[]=248&krl[]=250&krl[]=395&'
        search_url += 'krl[]=299&af=&at=&sex=&eylo=&t2l=&la=&id=22847743'
        search_url = search_url %(search_str)
        search_url += '&start=%i'
        class_rabota_search = RabotaParserSearch()
        namber_page = 0

        if not session:
            session = requests.Session()

        while True:
            search_peak = search_url %(namber_page)
            request_object = requests.Request('GET', search_peak)
            request = session.prepare_request(request_object)
            responce = session.send(request)
            content_html = responce.text
            responce.close()

            if responce.status_code != 200:
                break

            try:
                resumes = parser_search(cls=class_rabota_search, 
                                        html=content_html)
            except ParserError:
                break
            resume_list += resumes
            namber_page += 1

    if len(resume_list) > 0:
        resume_data_list = []
        resume_error_list = []
        class_rabota =  RabotaParserResume()
        for resume in resume_list:
            resume_url = resume['url']
            resume_reque_obj = requests.Request('GET', resume_url)
            resume_request = session.prepare_request(resume_reque_obj)
            try:
                resume_responce = session.send(resume_request)
            except HTTPError:
                resume_error_list += resume
                continue
            resume_html = resume_responce.text
            resume_responce.close()
            try:
                resume_data = parser_resume(cls=class_rabota,
                                            html=resume_html)
            except ParserError:
                resume_error_list += resume
                continue
            resume_data.setdefault('title_resume', resume['title_resume'])
            resume_data.setdefault('url', resume['url'])
            resume_data.setdefault('last_update', resume['last_update'])
            resume_data_list += resume_data

    return resume_data_list, resume_error_list
'''

if __name__ == '__main__':
    '''
    url = 'https://hh.ru/resume/e9bb81ccff0337fea50039ed1f577a68444648'
    connect = urllib.urlopen(url)
    html_content = connect.read()
    connect.close()
    class_hh = HhParserResume()
    data = parser_resume(cls=class_hh, html=html_content)
    print(data)
    #
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
        if namber_page >= 50:
            break
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
    #
    resume_list = []
    class_zp_search = ZarplataParserSearch()
    begin_all_time = time.time()
    date_performance = date.strftime('%d%m%G%H%M')
    PATH_FILE = 'D:\git-project\parserHH\ResumesIdBase'
    search_file = PATH_FILE + '\search_%s.csv' %(date_performance)
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
    file_search = open(search_file, 'bw')
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
    
    PATH_FILE = 'D:\git-project\parserHH\ResumesIdBase'
    namber_page = 0
    resume_list = []
    class_hh_search = SuperjobParserSearch()
    begin_all_time = time.time()
    begin_ = time.time()
    while True:
        random_sequence = random()*10**15
        hesh = int(random_sequence)
        begin_time = time.time()
        searchSpeak = 'https://www.superjob.ru/resume/search_resume.html?sbmit=1&t[]=4&keywords[0][srws]=7&keywords[0][skwc]=and&keywords[0][keys]=Siebel&search_hesh=%i&main=1&page=%i' %(hesh, namber_page)
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
        if namber_page >= 50:
            break
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
    #begin_resumes =  time.time()
    #for resume in resume_list:
        #begin_resume = time.time()
        #try:
        #    connect = urllib.urlopen(resume['url'])
        #except URLError:
        #    error_stak += 1
        #    error_str = '%s;\n' %(resume['url'])
        #    format = error_str.encode('utf-8')
        #    file_error.write(format)
        #    continue
        #html_content = connect.read()
        #connect.close()
        #class_hh = HhParserResume()
        #data = parser_resume(cls=class_hh, html=html_content)
        #resume.setdefault('gender', data['gender'])
        #resume.setdefault('first_name', data['first_name'])
        #resume.setdefault('last_name', data['last_name'])
        #resume.setdefault('middle_name', data['middle_name'])
        #resume.setdefault('phone', data['phone'])
        #resume.setdefault('email', data['email'])
        #resume.setdefault('city', data['city'])
        #resume.setdefault('metro_station', data['metro_station'])
        #resume.setdefault('education', data['education'])
        #resume.setdefault('experience', data['experience'])
        #end_resume = time.time()
        #spant_resume = (end_resume - begin_resume) / 60
        #print('Resume - %i, spent = %f' %(resume_index,
        #                                  spant_resume))
        #resume_index += 1
    #end_resumes = time.time()
    #file_error.close()
    #spent_resumes = (end_resumes - begin_resumes) / 60
    #print('Spent >>', spent_resumes)
    end_ = time.time()
    spent_ = (end_ - begin_) / 60
    print('All spent time = %f' %(spent_))
    file_search = open(search_file, 'bw')
    for record_item in resume_list:
        try:
            data_str = '%s;%s;%s;%s;%s;%s;%s;%s;\n' %(
                                record_item['title_resume'],
                                record_item['salary'],
                                record_item['age'],
                                record_item['experience'],
                                record_item['last_position'],
                                record_item['organization_name'],
                                record_item['url'],
                                record_item['last_update']
            )
            format = data_str.encode('utf-8')
            file_search.write(format)
        except KeyError:
            continue
    file_search.close()
    print('Count error = %i' %(error_stak))
'''
    session = requests.Session()
    '''
    session.headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36', 'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.6,en;q=0.4', 'Host': 'hh.ru', 'Content-Encoding': 'gzip', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8', 'Accept-Encoding': 'gzip, deflate, br', 'Connection': 'keep-alive', 'Cache-Control':'max-age=0', 'DNT':'1', 'Referer':'https://hh.ru/login', 'Upgrade-Insecure-Requests':'1'
    }
    
    session.headers = {
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.6,en;q=0.4',
        'Content-Encoding': 'gzip, deflate, br',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36 OPR/47.0.2631.80',
        'Upgrade-Insecure-Requests': '1',
        'Connection': 'keep-alive',
        'Host': 'www.superjob.ru',
        'Referer': 'https://www.superjob.ru/'
    }
    '''
    session.headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.6,en;q=0.4',
    'Content-Encoding': 'gzip',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'DNT': '1',
    'Origin': 'https://www.avito.ru',
    'Cache-Control': 'no-cache',
    'Host': 'www.avito.ru',
    'Referer': 'https://www.avito.ru/profile/login?next=%2Fprofile',
    'Upgrade-Insecure-Requests': '1'
    }
    #search_hh = SearchHh()
    #search_sj = SearchSj()
    search_avito = SearchAvito()
    #data, error = search_hh.search('Siebel', session=session, debug_flag=True)
    #data, error = search_sj.search('Siebel', session=session, debug_flag=True)
    relod_resume_avito = [
        {
         'title_resume': 'codec',
         'url': 'https://www.avito.ru/moskva/rezume/upravlyayuschiy_menedzher_administrator_1114512030',
         'last_update': '22.01.2018'
        }
    ]
    data, error = search_avito.search('Siebel', session=session,
                                      resume_list=relod_resume_avito,
                                      update_flad=True,
                                      debug_flag=True)
    #print('---------------')
    #print(data)
    #print(error)
    #print('---------------')
    for item in data:
        print('<<<---------->>>')
        print(item)
    #print(data[1]['experience'], error)
