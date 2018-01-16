import datetime

from random import random


def generate_dtata(default_str, pattern_data_str,
                   path_file='D:\git-project\load_card\card_file',
                   len_card_num=16,
                   len_phone_num=11,
                   emission_type='6062',
                   unequ_phone=True,
                   default_phone='88005553535',
                   count_card=100):
    count = 0
    date = datetime.datetime.utcnow()
    date_performance = date.strftime('%G%m%d%H%M%S')
    file_name = path_file + '\ext_contact_%s.dat' %(date_performance)
    card_file = open(file_name, 'bw')
    default_str += '\r\n'
    data_str = default_str.encode('utf-8')
    card_file.write(data_str)

    while True:
        unequ_float = random()*10**5
        unequ_id = int(unequ_float)
        person_name = 'PERSON_%i' %(unequ_id)
        length_number = len_card_num - len(emission_type)
        num_card_float = random()*10**length_number
        num_card_int = int(num_card_float)
        num_card_str = emission_type + str(num_card_int)
        
        if len(num_card_str) < len_card_num:
            ofset = len_card_num - len(num_card_str)
            num_card_str += date_performance[:ofset]
        
        if unequ_phone:       
            num_phone_float = random()*10**len_phone_num
            num_phone_int = int(num_phone_float)
            num_phone_str = str(num_phone_int)
        
            if len(num_phone_str) < len_phone_num:
                ofset = len_phone_num - len(num_phone_str)
                num_phone_str += date_performance[:ofset]
                
        else:
            num_phone_str = default_phone
            
        data = pattern_data_str %(num_card_str, 
                                  person_name, 
                                  person_name, 
                                  person_name, 
                                  num_phone_str)
        data += '\r\n'
        data_str = data.encode('utf-8')
        card_file.write(data_str)
        
        if count >= count_card:
            break

        count += 1
    card_file.close()
    return True

if __name__ == '__main__':
    default_str = ('#№ карты|Фамилия|Имя|Отчество|Пол|Дата рождения|Индекс|' +
                   'Область|Населенный пункт|Улица|Дом|Корпус|Квартира|' +
                   'Номер телефона|e-mail|Согласие на рассылку|' +
                   'Дата заполнения анкеты|Хэш|EAN|Название партнера')
    pattern_data_str = ('%s|%s|%s|%s|1|23/12/1988||||||||' + 
                        '%s|777@MAIL.RU|1|16/01/2018|?||Газпромбанк')
    complit_flag = generate_dtata(default_str, pattern_data_str, 
                                  emission_type='6821', unequ_phone=False)