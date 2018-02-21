import os
import codecs
import re
import xml.etree.ElementTree as etree


PATH_DIR_EVENTS_SOURCE = r'D:\git-project\parser_xml\events'

PATH_DIR_CNDIDATES_SOURCE = r'D:\git-project\parser_xml\canditates'

PATH_SAVE_EVENTS = r'D:\git-project\parser_xml\flet_events'

PATH_SAVE_CANDIDATES = r'D:\git-project\parser_xml\flet_candidates'


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
        data = data_raw.replace('\r\n', ' ')
        data = data.replace(';', ',')
        return data

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
        return self._get_target('homme_phone', xml_content)

    def get_phone(self, xml_content):
        return self._get_target('phone', xml_content)

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
    file = codecs.open(PATH_SAVE_EVENTS + '\\' +'event_result.csv', 
                       mode='bw', encoding='Windows-1251')
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
        #data = data_str.encode('Windows-1251')
        file.write(data_str)
    file.close()

def event_scan():
    event_xml_parser = EventParse()
    event_list = []
    for path_dir, dirs, files in os.walk(PATH_DIR_EVENTS_SOURCE):
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

    return candidate

def candidate_save(candidate_list):
    file = codecs.open(PATH_SAVE_CANDIDATES + '\\' +
                       'candidate_result.csv',
                       mode='bw', encoding='Windows-1251')
    format_str = "%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;"
    format_str += "%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s\n"
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
                                candidate['main_vacancy_id']
        )
        #data = data_str.encode('Windows-1251')
        file.write(data_str)
    file.close()

def clear_attachments(file_source):
    file_in = codecs.open(file_source, mode='br')
    data = file_in.read()
    file_in.close()
    file_out = codecs.open(file_source, mode='bw')
    reg_exp = b'<attachments>.+</attachments>'
    attachments = re.findall(reg_exp, data)
    try:
        attachments_sub_str = attachments[0]
    except IndexError:
        attachments_sub_str = None

    if attachments_sub_str:
        data = data.replace(attachments_sub_str, b'')
        execution = True
    else:
        execution = False

    file_out.write(data)
    file_out.close()

    return execution


def candidate_scan():
    candidate_xml_parser = CandidateParser()
    candidate_list = []
    for path_dir, dirs, files in os.walk(PATH_DIR_CNDIDATES_SOURCE):
        for file in files:
            file_source = path_dir + '\\' + file
            try:
                tree = etree.parse(file_source)
            except etree.ParseError:
                execution = clear_attachments(file_source)

                if execution:
                    tree = etree.parse(file_source)
                else:
                    continue

            root = tree.getroot()
            candidate = candidate_parser(candidate_xml_parser, root)
            candidate_list.append(candidate)

    candidate_save(candidate_list)

if __name__ == '__main__':
    print('Event Start')
    event_scan()
    print('Event End')
    print('Candidate Start')
    candidate_scan()
    print('andidate End')