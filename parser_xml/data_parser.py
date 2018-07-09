import os
import sys
import codecs
import datetime
import re
import xml.etree.ElementTree as etree
import argparse
import threading


PATH_EVENTS_SOURCE = r'D:\git-project\parser_xml\events'

PATH_CNDIDATES_SOURCE = r'D:\git-project\parser_xml\candidates'

PATH_SAVE_EVENTS = r'D:\git-project\parser_xml\flet_events'

PATH_SAVE_CANDIDATES = r'D:\git-project\parser_xml\flet_candidates'

PATH_VACANCY_SOURCE = r'D:\git-project\parser_xml\vacancy'

PATH_VACANCY_SAVE = r'D:\git-project\parser_xml\flet_vacancy'

PATH_DIVISION_SOURCE = r'D:\git-project\parser_xml\division'

PATH_DIVIVISION_SAVE = r'D:\git-project\parser_xml\flet_division'

PATH_VACANCY_CAND_SAVE = r'D:\git-project\parser_xml\flet_candidate_vacanct'


class BaseException(Exception):
    def __init__(self, message):
        self.message = message


class ParserError(BaseException):
    pass


class BaseParserXML(object):

    def _get_target(self, target_name, xml_content, 
                    return_xml_element=False):
        """Find target value or element in xml tree
        Takes xml tree and target_name
        Returned value
        """
        target_attr = getattr(self, 'target_' + target_name, None)

        if not target_attr:
            raise ParserError("No goal %s specified" % target_name)

        if xml_content:
            target_tag = xml_content.find(target_attr)
        else:
            target_tag = ''

        if target_tag is not None:
            if return_xml_element:
                result = target_tag
            else:
                result = target_tag.text
        else:
            result = ''

        return result

    def _get_more_target(self, target_name, xml_content,
                         returned_xml_elements=False):
        """Find all target value
        Takes target name and xml content
        Returned list values
        """
        target_attr = getattr(self, 'target_' + target_name, None)

        if not target_attr:
            raise ParserError("No goal %s specified" % target_name)

        if xml_content:
            tag_list = xml_content.findall(target_attr)
        else:
            tag_list = []

        if tag_list:

            if not returned_xml_elements:
                value_list = [
                    tag.text for tag in tag_list
                ]
            else:
                value_list = tag_list
        else:
            value_list = []

        return value_list


class EventParse(BaseParserXML):
    target_id = 'id'
    target_type_id = 'type_id'
    #target_is_derived = 'is_derived'
    target_date = 'date'
    target_vacancy_id = 'vacancy_id'
    target_candidate_id = 'candidate_id'
    target_comment = 'comment'
    target_creation_date = 'creation_date'
    target_contact_phones_desc = 'contact_phones_desc'
    #target_is_rr_poll = 'is_rr_poll'

    def get_id(self, xml_content):
        return self._get_target('id', xml_content)

    def get_type_id(self, xml_content):
        return self._get_target('type_id', xml_content)

    def get_date(self, xml_content):
        return self._get_target('date', xml_content)

    def get_vacancy_id(self, xml_content):
        return self._get_target('vacancy_id', xml_content)

    def get_candidate_id(self, xml_content):
        return self._get_target('candidate_id', xml_content)

    def get_comment(self, xml_content):
        data_raw = self._get_target('comment', xml_content)
        data = data_raw.replace('\r\n', '')
        data = data.replace('\r', '')
        data = data.replace('\n', '')
        data = data.replace('\t', ' ')
        data = re.findall(
                    '[^#\d+][A-Za-zА-ЯЁа-яё\.\d\-\_\:\s]+',
                    data
        )
        data_string = str(' ').join(data)
        data_string = data_string.replace(';', ',')
        return data_string

    def get_creation_date(self, xml_content):
        return self._get_target('creation_date', xml_content)

    def get_contact_phones_desc(self, xml_content):
        data_raw = self._get_target('contact_phones_desc', xml_content)
        data = data_raw.replace(';', ',')
        return data


class CandidateParser(BaseParserXML):
    target_id = 'id'
    target_code = 'code'
    target_first_name = 'firstname'
    target_last_name = 'lastname'
    target_middle_name = 'middlename'
    target_is_candidate = 'is_candidate'
    target_gender = 'gender_id'
    target_birth = 'birth_date'
    target_age = 'age'
    target_homme_phone = 'home_phone'
    target_phone = 'mobile_phone'
    target_email = 'email'
    target_email_2 = 'email2'
    target_creation_date = 'creation_date'
    target_last_mod_date = 'last_mod_date'
    target_entrance = 'entrance_type_id'
    target_source = 'source_id'
    target_city = 'location_id'
    target_salary = 'salary'
    target_uni_salary = 'uni_salary'
    target_vacancy_id = 'vacancy_id'
    target_main_vacancy_id = 'main_vacancy_id'
    target_main_vac_div = 'main_vacancy_division_id'

    def get_id(self, xml_content):
        return self._get_target('id', xml_content)

    def get_code(self, xml_content):
        return self._get_target('code', xml_content)

    def get_first_name(self, xml_content):
        return self._get_target('first_name', xml_content)

    def get_last_name(self, xml_content):
        return self._get_target('last_name', xml_content)

    def get_middle_name(self, xml_content):
        return self._get_target('middle_name', xml_content)

    def get_is_candidate(self, xml_content):
        return self._get_target('is_candidate', xml_content)

    def get_gender(self, xml_content):
        return self._get_target('gender', xml_content)

    def get_birth(self, xml_content):
        return self._get_target('birth', xml_content)

    def get_age(self, xml_content):
        return self._get_target('age', xml_content)

    def get_homme_phone(self, xml_content):
        raw = self._get_target('homme_phone', xml_content)
        data = raw.replace(';', ',')
        return data

    def get_phone(self, xml_content):
        raw = self._get_target('phone', xml_content)
        data = raw.replace(';', ',')
        return data

    def get_email(self, xml_content):
        return self._get_target('email', xml_content)

    def get_email_2(self, xml_content):
        return self._get_target('email_2', xml_content)

    def get_creation_date(self, xml_content):
        return self._get_target('creation_date', xml_content)

    def get_last_mod_date(self, xml_content):
        return self._get_target('last_mod_date', xml_content)

    def get_entrance(self, xml_content):
        return self._get_target('entrance', xml_content)

    def get_source(self, xml_content):
        return self._get_target('source', xml_content)

    def get_city(self, xml_content):
        return self._get_target('city', xml_content)

    def get_salary(self, xml_content):
        return self._get_target('salary', xml_content)

    def get_uni_salary(self, xml_content):
        return self._get_target('uni_salary', xml_content)

    def get_vacancy_id(self, xml_content):
        return self._get_target('vacancy_id', xml_content)

    def get_main_vacancy_id(self, xml_content):
        return self._get_target('main_vacancy_id', xml_content)

    def get_main_vac_div(self, xml_content):
        return self._get_target('main_vac_div', xml_content)


class VacancyParser(BaseParserXML):
    target_id = 'id'
    target_name = 'name'
    target_code = 'code'
    target_division = 'division_id'
    target_created = 'start_date'
    target_final_candidate = 'final_candidate_id'
    target_source = 'final_candidate_source_id'
    target_city = 'location_id'
    target_position_name = 'position_name'
    target_comment = 'comment'
    target_records = 'records'
    target_mass_vacancy = 'is_mass_vacancy'
    target_mp_vacancy = 'is_mp_vacancy'

    target_record = 'record'
    target_event_date = 'date'
    target_type = 'type_id'
    target_status = 'state_id'

    def get_id(self, xml_content):
        return self._get_target('id', xml_content)

    def get_name(self, xml_content):
        return self._get_target('name', xml_content)

    def get_code(self, xml_content):
        return self._get_target('code', xml_content)

    def get_division(self, xml_content):
        return self._get_target('division', xml_content)

    def get_created(self, xml_content):
        return self._get_target('created', xml_content)

    def get_final_candidate(self, xml_content):
        return self._get_target('final_candidate', xml_content)

    def get_source(self, xml_content):
        return self._get_target('source', xml_content)

    def get_city(self, xml_content):
        return self._get_target('city', xml_content)

    def get_position_name(self, xml_content):
        return self._get_target('position_name', xml_content)

    def get_comment(self, xml_content):
        raw = self._get_target('comment', xml_content)
        data = raw.replace('\r\n', '')
        data = data.replace('\r', '')
        data = data.replace('\n', '')
        data = data.replace('\t', ' ')
        data = re.findall(
                    '[^#\d+][A-Za-zА-ЯЁа-яё\.\d\-\_\:\s]+',
                    data
        )
        data_string = str(' ').join(data)
        data_string = data_string.replace(';', ',')
        return data_string

    def get_mass_vacancy(self, xml_content):
        raw = self._get_target('mass_vacancy', xml_content)

        if raw == '':
            data = 0
        else:
            data = raw

        return data

    def get_mp_vacancy(self, xml_content):
        raw = self._get_target('mp_vacancy', xml_content)

        if raw == '':
            data = 0
        else:
            data = raw

        return data

    def get_status(self, xml_content):
        return self._get_target('status', xml_content)

    def get_history(self, xml_content):
        tag_records = self._get_target('records', xml_content,
                                       return_xml_element=True)
        tag_list = self._get_more_target('record', tag_records,
                                         returned_xml_elements=True)
        status_list = []

        for tag in tag_list:
            status_dict = {}
            event_date = self._get_target('event_date', tag)
            type = self._get_target('type', tag)
            status = self._get_target('status', tag)

            status_dict.setdefault('date', event_date)
            status_dict.setdefault('type', type)
            status_dict.setdefault('status', status)

            status_list.append(status_dict)


        return status_list


class VacancyCandidates(BaseParserXML):
    target_vacansie = 'id'
    target_candidate = 'multi_final_candidate_id'

    def get_vacancy(self, xml_content):
        return self._get_target('vacansie', xml_content)

    def get_candidates(self, xml_content):
        return self._get_more_target('candidate', xml_content)


class DivisionParser(BaseParserXML):
    target_id = 'id'
    target_parent_id = 'parent_id'
    target_created = 'creation_date'
    target_last_update = 'last_mod_date'
    target_code = 'code'
    target_name = 'name'
    target_type = 'type_id'
    target_hce = 'hce'
    target_eid = 'eid'

    def get_id(self, xml_content):
        return self._get_target('id', xml_content)

    def get_parent_id(self, xml_content):
        return self._get_target('parent_id', xml_content)

    def get_created(self, xml_content):
        return self._get_target('created', xml_content)

    def get_last_update(self, xml_content):
        return self._get_target('last_update', xml_content)

    def get_code(self, xml_content):
        return self._get_target('code', xml_content)

    def get_name(self, xml_content):
        return self._get_target('name', xml_content)

    def get_type(self, xml_content):
        return self._get_target('type', xml_content)

    def get_hce(self, xml_content):
        return self._get_target('hce', xml_content)

    def get_eid(self, xml_content):
        return self._get_target('eid', xml_content)


def save_error(error_list):
    file = codecs.open(PATH_SAVE_CANDIDATES + '\\' +
                       'error_log.csv',
                       mode='bw', encoding='Windows-1251')
    for error in error_list:
        data_str = '%s\n' %(error)
        file.write(data_str)
    file.close()

def event_parser(cls, xml_content):
    if not cls:
        raise ParserError("Required argument is None")

    if not xml_content:
        raise ParserError("XML is None")

    event = {}

    event_id = cls.get_id(xml_content)
    event.setdefault('id', event_id)

    type_id =cls.get_type_id(xml_content)
    event.setdefault('type_id', type_id)

    date = cls.get_date(xml_content)
    event.setdefault('date', date)

    vacancy_id = cls.get_vacancy_id(xml_content)
    event.setdefault('vacancy_id', vacancy_id)

    candidate_id = cls.get_candidate_id(xml_content)
    event.setdefault('candidate_id', candidate_id)

    comment = cls.get_comment(xml_content)
    event.setdefault('comment', comment)

    creation_date = cls.get_creation_date(xml_content)
    event.setdefault('creation_date', creation_date)

    contact_phones_desc = cls.get_contact_phones_desc(xml_content)
    event.setdefault('contact_phones_desc', contact_phones_desc)

    return event

def event_save(event_list):
    date = datetime.datetime.utcnow()
    date_performance = date.strftime('%d_%m_%G')
    name = 'event_result_%s.csv' %(date_performance)
    file = codecs.open(PATH_SAVE_EVENTS + '\\' + name, 
                       mode='bw', encoding='Windows-1251')
    file.write("id;type;date;vacancy_id;candidate_id;creation_date;" +
               "contact_phones_desc;comment\n")
    for event in event_list:
        data_str = "%s;%s;%s;%s;%s;%s;%s;%s\n" %(
                                            event['id'],
                                            event['type_id'],
                                            event['date'],
                                            event['vacancy_id'],
                                            event['candidate_id'],
                                            event['creation_date'],
                                            event['contact_phones_desc'],
                                            event['comment']
        )
#        if len(event['comment']) > 300:
#            print(data_str)
        #data = data_str.encode('Windows-1251')
        file.write(data_str)
    file.close()

def event_scan():
    event_xml_parser = EventParse()
    event_list = []
    for path_dir, dirs, files in os.walk(PATH_EVENTS_SOURCE):
        for file in files:
            file_source = path_dir + '\\' + file
            tree = etree.parse(file_source)
            root = tree.getroot()
            event = event_parser(event_xml_parser, root)
            event_list.append(event)

    event_save(event_list)

def candidate_parser(cls, xml_content):
    if not cls:
        raise ParserError("Required argument is None")

    if not xml_content:
        raise ParserError("XML is None")

    candidate = {}

    candidate_id = cls.get_id(xml_content)
    candidate.setdefault('id', candidate_id)

    candidate_code = cls.get_code(xml_content)
    candidate.setdefault('code', candidate_code)

    candidate_first_name = cls.get_first_name(xml_content)
    candidate.setdefault('first_name', candidate_first_name)

    candidate_last_name = cls.get_last_name(xml_content)
    candidate.setdefault('last_name', candidate_last_name)

    candidate_middle_name = cls.get_middle_name(xml_content)
    candidate.setdefault('middle_name', candidate_middle_name)

    candidate_gender = cls.get_gender(xml_content)
    candidate.setdefault('gender', candidate_gender)

    candidate_flag = cls.get_is_candidate(xml_content)
    candidate.setdefault('is_candidate', candidate_flag)

    candidate_birth = cls.get_birth(xml_content)
    candidate.setdefault('birth', candidate_birth)

    candidate_age = cls.get_age(xml_content)
    candidate.setdefault('age', candidate_age)

    candidate_homme_phone = cls.get_homme_phone(xml_content)
    candidate.setdefault('homme_phone', candidate_homme_phone)

    candidate_phone = cls.get_phone(xml_content)
    candidate.setdefault('phone', candidate_phone)

    candidate_email = cls.get_email(xml_content)
    candidate.setdefault('email', candidate_email)

    candidate_email_2 = cls.get_email_2(xml_content)
    candidate.setdefault('email_2', candidate_email_2)

    candidate_create = cls.get_creation_date(xml_content)
    candidate.setdefault('creation_date', candidate_create)

    candidate_last_mod = cls.get_last_mod_date(xml_content)
    candidate.setdefault('last_mod_date', candidate_last_mod)

    candidate_entrance = cls.get_entrance(xml_content)
    candidate.setdefault('entrance', candidate_entrance)

    candidate_source = cls.get_source(xml_content)
    candidate.setdefault('source', candidate_source)

    candidate_city = cls.get_city(xml_content)
    candidate.setdefault('city', candidate_city)

    candidate_salary = cls.get_salary(xml_content)
    candidate.setdefault('salary', candidate_salary)

    candidate_uni_salary = cls.get_uni_salary(xml_content)
    candidate.setdefault('uni_salary', candidate_uni_salary)

    candidate_vacancy = cls.get_vacancy_id(xml_content)
    candidate.setdefault('vacancy_id', candidate_vacancy)

    candidate_main_vacancy = cls.get_main_vacancy_id(xml_content)
    candidate.setdefault('main_vacancy_id', candidate_main_vacancy)

    candidate_main_vac_div = cls.get_main_vac_div(xml_content)
    candidate.setdefault('main_vac_div', candidate_main_vac_div)

    return candidate

def candidate_save(candidate_list):
    date = datetime.datetime.utcnow()
    date_performance = date.strftime('%d_%m_%G')
    name = 'candidate_result_%s' %(date_performance)
    file = codecs.open(PATH_SAVE_CANDIDATES + '\\' + name,
                       mode='bw', encoding='Windows-1251')
    format_str = "%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;"
    format_str += "%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s\n"
    file.write("id;code;first_name;last_name;middle_name;gender;" +
               "is_candidate;birth;age;homme_phone;phone;email;" +
               "email_2;creation_date;last_mod_date;entrance;" +
               "source;city;salary;uni_salary;vacancy_id;" +
               "main_vacancy_id;main_vacancy_division_id\n")
    for candidate in candidate_list:
        data_str = format_str %(
                                candidate['id'],
                                candidate['code'],
                                candidate['first_name'],
                                candidate['last_name'],
                                candidate['middle_name'],
                                candidate['gender'],
                                candidate['is_candidate'],
                                candidate['birth'],
                                candidate['age'],
                                candidate['homme_phone'],
                                candidate['phone'],
                                candidate['email'],
                                candidate['email_2'],
                                candidate['creation_date'],
                                candidate['last_mod_date'],
                                candidate['entrance'],
                                candidate['source'],
                                candidate['city'],
                                candidate['salary'],
                                candidate['uni_salary'],
                                candidate['vacancy_id'],
                                candidate['main_vacancy_id'],
                                candidate['main_vac_div']
        )
        #data = data_str.encode('Windows-1251')
        file.write(data_str)
    file.close()

def clear_attachments(file_source):
    file_in = codecs.open(file_source, mode='br')
    data = file_in.read()
    file_in.close()
    reg_exp = b'<attachments>.+</attachments>'
    attachments = re.findall(reg_exp, data)
    try:
        attachments_sub_str = attachments[0]
    except IndexError:
        attachments_sub_str = None

    if attachments_sub_str:
        data = data.replace(attachments_sub_str, b'')
        file_out = codecs.open(file_source, mode='bw')
        file_out.write(data)
        file_out.close()
        execution = True
    else:
        execution = False

    return execution

def candidate_scan():
    candidate_xml_parser = CandidateParser()
    candidate_list = []
    error_list = []
    for path_dir, dirs, files in os.walk(PATH_CNDIDATES_SOURCE):
        for file in files:
            file_source = path_dir + '\\' + file
            try:
                tree = etree.parse(file_source)
            except etree.ParseError:
                execution = clear_attachments(file_source)

                if execution:
                    tree = etree.parse(file_source)
                else:
                    error_list.append(file)

            root = tree.getroot()
            candidate = candidate_parser(candidate_xml_parser, root)
            candidate_list.append(candidate)

    candidate_save(candidate_list)
    save_error(error_list)

def vacancy_parser(cls, xml_content):
    if not cls:
        raise ParserError("Required argument is None")

    if not xml_content:
        raise ParserError("XML is None")

    id = cls.get_id(xml_content)
    name = cls.get_name(xml_content)
    code = cls.get_code(xml_content)
    division = cls.get_division(xml_content)
    created = cls.get_created(xml_content)
    final_candidate = cls.get_final_candidate(xml_content)
    source = cls.get_source(xml_content)
    city = cls.get_city(xml_content)
    position_name = cls.get_position_name(xml_content)
    comment = cls.get_comment(xml_content)
    is_mass_vacancy = cls.get_mass_vacancy(xml_content)
    is_mp_vacancy = cls.get_mp_vacancy(xml_content)

    history = cls.get_history(xml_content)

    if len(history) < 1:
        #print("Allert! vacancy_id = %s" %(id))
        status = cls.get_status(xml_content)
        create_history = {}
        create_history.setdefault('date', created)
        create_history.setdefault('status', status)
        create_history.setdefault('type', '')
        history.append(create_history)

    for item in history:
        item.setdefault('id', id)
        item.setdefault('name', name)
        item.setdefault('code', code)
        item.setdefault('division', division)
        item.setdefault('created', created)
        item.setdefault('final_candidate', final_candidate)
        item.setdefault('source', source)
        item.setdefault('city', city)
        item.setdefault('position_name', position_name)
        item.setdefault('comment', comment)
        item.setdefault('mass_vacancy', is_mass_vacancy)
        item.setdefault('mp_vacancy', is_mp_vacancy)

    return history

def vacancy_save(vacancy_list):
    date = datetime.datetime.utcnow()
    date_performance = date.strftime('%d_%m_%G')
    name = 'vacancy_result_%s.csv' %(date_performance)
    file = codecs.open(PATH_VACANCY_SAVE + '\\' + name,
                       mode='bw', encoding='Windows-1251')
    file.write("id;name;code;division;created;final_candidate;" +
               "source;city;position_name;status;date;type;" +
               "comment;mass_vacancy;mp_vacancy\n")
    for vacancy in vacancy_list:
        data_str = "%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s\n" %(
                                        vacancy['id'],
                                        vacancy['name'],
                                        vacancy['code'],
                                        vacancy['division'],
                                        vacancy['created'],
                                        vacancy['final_candidate'],
                                        vacancy['source'],
                                        vacancy['city'],
                                        vacancy['position_name'],
                                        vacancy['status'],
                                        vacancy['date'],
                                        vacancy['type'],
                                        vacancy['comment'],
                                        vacancy['mass_vacancy'],
                                        vacancy['mp_vacancy']
        )
        #data = data_str.encode('Windows-1251')
        file.write(data_str)
    file.close()

def vacancy_scan():
    vacancy_xml_parser = VacancyParser()
    vacancy_candidate_xmal_parser = VacancyCandidates()
    vacancy_list = []
    vacancy_candidates_list = []
    for path_dir, dirs, files in os.walk(PATH_VACANCY_SOURCE):
        for file in files:
            file_source = path_dir + '\\' + file
            tree = etree.parse(file_source)
            root = tree.getroot()
            vacancy = vacancy_parser(vacancy_xml_parser, root)
            vacancy_candidates = vacancy_candidates_parser(
                                        vacancy_candidate_xmal_parser,
                                        root
            )
            vacancy_list += vacancy
            vacancy_candidates_list += vacancy_candidates

    vacancy_save(vacancy_list)
    vacancy_candidates_save(vacancy_candidates_list)

def vacancy_candidates_parser(cls, xml_content):
    if not cls:
        raise ParserError("Required argument is None")

    if not xml_content:
        raise ParserError("XML is None")

    vacabcy_candidates_list = []
    vacancy = cls.get_vacancy(xml_content)
    candidates_list = cls.get_candidates(xml_content)
    for candidate in candidates_list:
        vacancy_candidates = {}
        vacancy_candidates.setdefault('vacancy', vacancy)
        vacancy_candidates.setdefault('candidate', candidate)
        vacabcy_candidates_list.append(vacancy_candidates)
    return vacabcy_candidates_list

def vacancy_candidates_save(vacancy_candidates_list):
    date = datetime.datetime.utcnow()
    date_performance = date.strftime('%d_%m_%G')
    name = 'vacancy_candidates_result_%s.csv' %(date_performance)
    file = codecs.open(PATH_VACANCY_CAND_SAVE + '\\' + name, 
                       mode='bw', encoding='Windows-1251')
    file.write("vacancy;candidate\n")
    for vacancy in vacancy_candidates_list:
        data_str = "%s;%s\n" %(vacancy['vacancy'], vacancy['candidate'])
        #data = data_str.encode('Windows-1251')
        file.write(data_str)
    file.close()

def division_parser(cls, xml_content):
    if not cls:
        raise ParserError("Required argument is None")

    if not xml_content:
        raise ParserError("XML is None")

    division = {}

    id = cls.get_id(xml_content)
    division.setdefault('id', id)

    parent_id = cls.get_parent_id(xml_content)
    division.setdefault('parent_id', parent_id)

    created = cls.get_created(xml_content)
    division.setdefault('created', created)

    last_update = cls.get_last_update(xml_content)
    division.setdefault('last_update', last_update)

    code = cls.get_code(xml_content)
    division.setdefault('code', code)

    name = cls.get_name(xml_content)
    division.setdefault('name', name)

    type = cls.get_type(xml_content)
    division.setdefault('type', type)

    hce = cls.get_hce(xml_content)
    division.setdefault('hce', hce)

    eid = cls.get_eid(xml_content)
    division.setdefault('eid', eid)

    return division

def division_save(division_list):
    date = datetime.datetime.utcnow()
    date_performance = date.strftime('%d_%m_%G')
    name = 'division_result_%s.csv' %(date_performance)
    file = codecs.open(PATH_DIVIVISION_SAVE + '\\' + name,
                        mode='bw', 
                        encoding='Windows-1251')
    file.write("id;parent_id;created;last_update;code;name;type;" +
               "hce;eid\n")
    for division in division_list:
        data_str = "%s;%s;%s;%s;%s;%s;%s;%s;%s\n" %(
                                            division['id'],
                                            division['parent_id'],
                                            division['created'],
                                            division['last_update'],
                                            division['code'],
                                            division['name'],
                                            division['type'],
                                            division['hce'],
                                            division['eid']
        )
        file.write(data_str)
    file.close()

def division_scan():
    division_xml_parser = DivisionParser()
    division_list = []
    for path_dir, dirs, files in os.walk(PATH_DIVISION_SOURCE):
        for file in files:
            file_source = path_dir + '\\' + file
            try:
                tree = etree.parse(file_source)
            except etree.ParseError:
                continue
            root = tree.getroot()
            division = division_parser(division_xml_parser, root)
            division_list.append(division)

    division_save(division_list)

def correction_files():
    error_log = codecs.open(PATH_SAVE_CANDIDATES + '\\' +
                            'error_log.csv',
                            mode='br', encoding='Windows-1251')
    data_error_log = error_log.read()
    errors = data_error_log.split('\n')
    for error_file in errors:
        #execution = clear(PATH_CNDIDATES_SOURCE + '\\' +
        #                  error_file)
        execution = add_heder_xml(PATH_CNDIDATES_SOURCE + '\\' +
                                  error_file)
        print(error_file, '-', execution)

def clear(file_source):
    file_in = codecs.open(file_source, mode='br')
    data = file_in.read()
    file_in.close()
    reg_exp_1 = (#b' +
            b'<candidate SPXML-FORM="x-app://rcr/rcr_candidate.xmd">' +
            b'.+<attachments>'
    )
    reg_exp_2 = b'</attachments>.+</candidate>'
    data_1 = re.findall(reg_exp_1, data)
    data_2 = re.findall(reg_exp_2, data)
    
    if data_1 and data_2:
        data_list = data_1 + data_2
        data = b''.join(data_list)
        file_out = codecs.open(file_source, mode='bw')
        file_out.write(data)
        file_out.close()
        execution = True
    else:
        execution = False

    return execution

def add_heder_xml(file_source):
    file_in = open(file_source, 'br')
    data_in = file_in.read()
    file_in.close()
    header_str = b'<?xml version="1.0" encoding="windows-1251"?>\n'
    file_out = open(file_source, 'bw')
    file_out.write(header_str + data_in)
    file_out.close()
    return True

def get_files_path():
    PATH_EVENTS_SOURCE = os.getenv('PATH_EVENTS_SOURCE')
    PATH_CNDIDATES_SOURCE = os.getenv('PATH_CNDIDATES_SOURCE')
    PATH_SAVE_EVENTS = os.getenv('PATH_SAVE_EVENTS')
    PATH_SAVE_CANDIDATES = os.getenv('PATH_SAVE_CANDIDATES')
    PATH_VACANCY_SOURCE = os.getenv('PATH_VACANCY_SOURCE')
    PATH_VACANCY_SAVE = os.getenv('PATH_VACANCY_SAVE')
    PATH_DIVISION_SOURCE = os.getenv('PATH_DIVISION_SOURCE')
    PATH_DIVIVISION_SAVE = os.getenv('PATH_DIVIVISION_SAVE')
    PATH_VACANCY_CAND_SAVE = os.getenv('PATH_VACANCY_CAND_SAVE')

if __name__ == '__main__':
    sys_args_parse = argparse.ArgumentParser(
        description=('This utility parsing xml-files from '+
                     'e-staff and convert to csv-files')
    )
    sys_args_parse.add_argument(
        '-usp', '--using_system_preference',
        help='Utility using path define in system preference',
        default=False,
        action='store_true'
    )
    sys_args_parse.add_argument(
        '-all', '--all',
        help ='Utility parsing all categorie source files',
        default=False,
        action='store_true'
    )
    sys_args_parse.add_argument(
        '-can', '--candidates',
        help='Utility only parsing canditate files',
        default=False,
        action='store_true'
    )
    sys_args_parse.add_argument(
        '-e', '--event',
        help='Utility only parsing event files',
        default=False,
        action='store_true'
    )
    sys_args_parse.add_argument(
        '-v', '--vacancy',
        help='Utility only parsing vacancy files',
        default=False,
        action='store_true'
    )
    sys_args_parse.add_argument(
        '-d', '--division',
        help='Utility only parsing division files',
        default=False,
        action='store_true'
    )
    sys_args_parse.add_argument(
        '-cor', '--correct',
        help='Utility only correct source files',
        default=False,
        action='store_true'
    )
    cmd_arg = sys_args_parse.parse_args(sys.argv[1:])

    if cmd_arg.using_system_preference:
        get_files_path()

    if cmd_arg.all:
        thread_1 = threading.Thread(target=vacancy_scan)
        thread_2 = threading.Thread(target=event_scan)
        thread_3 = threading.Thread(target=candidate_scan)
        ##thread_4 = threading.Thread(target=division_scan)

        thread_1.daemon = True
        thread_2.daemon = True
        thread_3.daemon = True
        ##thread_4.daemon = True

        thread_1.start()
        thread_2.start()
        thread_3.start()
        ##thread_4.start()

        ##correction_files()

    if cmd_arg.candidates and not cmd_arg.all:
        candidate_scan()
    if cmd_arg.event and not cmd_arg.all:
        event_scan()
    if cmd_arg.vacancy and not cmd_arg.all:
        vacancy_scan()
    if cmd_arg.division:
        division_scan()
    if cmd_arg.correct:
        correction_files()