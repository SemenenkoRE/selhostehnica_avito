import time

def print_error(reference_ad, exception):

    """
    Выводит на экран ошибку.
    """

    print(f'ссылка: {reference_ad}\n')
    print(f'ошибка: {exception}')


def save_errors(reference_ad, exception):

    """
    Функция переодически может встречаться с ошибки, необходимые для дальнейшего анализа.
    Для их сохранения применяется функция записи текста ошибки в отдельный текстовый файл.
    """

    with open('errors', 'a', encoding='utf-8') as er:
        er.write(f'ссылка: {reference_ad}\n')
        er.write(f'ошибка: {exception}\n\n')


def do_log(reference_search, reference_ad):

    """
    Функция переодически может встречаться с ошибки, необходимые для дальнейшего анализа.
    Для их сохранения применяется функция записи текста ошибки в отдельный текстовый файл.
    """

    with open('report_ref', 'a', encoding='utf-8') as rep:
        rep.write(f'время: {time.ctime()}\t')
        rep.write(f'общая_ссылка: {reference_search}\t')
        rep.write(f'объяв_ссылка: {reference_ad}\n\n')

    print(f'Сделан лог ___ время: {time.ctime()} \n___ общая_ссылка: {reference_search} ___ '
          f'объяв_ссылка: https://www.avito.ru{reference_ad}')



if __name__ == '__main__':
    do_log('111', '222')
