import time
import datetime

# 9 августа в 10:56
# Вчера в 20:37
# 2021-08-10 01:55:00
# untreated_time_offer = self.current_ad_dom.xpath("//div[@class='title-info-metadata-item-redesign']/text()")[0]

months_dict_en = {'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6, 'Jul': 7, 'Aug': 8, 'Sep': 9,
                      'Oct': 10, 'Nov': 11, 'Dec': 12}

months_dict_rus = {'января': 1, 'февраля': 2, 'марта': 3, 'апреля': 4, 'мая': 5, 'июня': 6, 'июля': 7, 'августа': 8,
                   'сентября': 9, 'октября': 10, 'ноября': 11, 'декабря': 12}


def set_time_ad(text_time):
    """
        Определение даты и времени объявления.
        Особенности: метод приводит дату к виду формата sql -- datetime
    """

    day, month, year, hh, mm, ss = None, None, None, None, None, None

    if 'сегодня' in text_time:
        day = int(time.ctime().split(' ')[2])
        year = int(time.ctime().split(' ')[4])

        for key, val in months_dict_en.items():

            if time.ctime().split(' ')[1] == key:
                month = val

        # set time
        hh, mm, ss = set_time(text_time)


    elif 'вчера' in text_time:

        day = int(time.ctime(time.time() - 24 * 3600).split(' ')[2])
        year = int(time.ctime(time.time() - 24 * 3600).split(' ')[4])

        for key, val in months_dict_en.items():

            if time.ctime(time.time() - 24 * 3600).split(' ')[1] == key:
                month = val

        # set time
        hh, mm, ss = set_time(text_time)

    else:

        # set correct day
        day = int(text_time.split()[0])

        # set correct month
        month = None
        for key, val in months_dict_rus.items():

            if key == text_time.split()[1]:
                month = val

        # set correct year
        year = 2021

        # set time
        hh, mm, ss = set_time(text_time)

    return datetime.datetime(year, month, day, hh, mm, ss)


def set_time(untreated_time_offer):

    # set hours
    hh = int(untreated_time_offer.split()[-1].split(":")[0])

    # set minutes
    mm = int(untreated_time_offer.split()[-1].split(":")[1])

    # set seconds
    ss = 0

    return hh, mm, ss


if __name__ == '__main__':
    print(set_time_ad('Вчера в 10:56'))