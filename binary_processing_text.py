

def binary_response(text):

    """
    Функция получает текст в обычном виде и возвращает текст в формате двоичного кода.
    Опред-ся соотвестствующий элементу текста номер в юникоде, который далее приводится к бинарному (двоичному) виду.
    """

    bin_text = ''

    for letter in text:
        bin_text = f"{bin_text}{ord(letter):b} "    # цифра переводится в двоичный код с помощью f-строки и опции :b

    return bin_text




def clearing_unnecessary_symbols(bin_text):

    """
    Бинарный текст очищается от элементов, соответствующих \n и \t.
    """

    bin_text_list = bin_text.split(' ')

    for el in reversed(range(len(bin_text.split(' ')))):

        if bin_text_list[el] == '1010' or bin_text_list[el] == '1001' or bin_text_list[el] == '10100000':
            bin_text_list.pop(el)

    bin_text_correct = ''

    for number, el in enumerate(bin_text_list):

        if '1' in el or '0' in el:

            if number != len(bin_text_list) - 1:
                bin_text_correct = f'{bin_text_correct}{el} '

    return bin_text_correct




def text_response(bin_text):

    """
    Функция принимает текст в бинарном виде и возращает в нормальном. 
    """

    text = ''

    for element in bin_text.split(' '):

        if '0' in element or '1' in element:
            text = f"{text}{chr(int(element, 2))}"

    return text


def processing_text(text):
    
    """
    Функция получает текст, через приведение к двоичному коду удаляет символы \n и \t, возвращает к текстовому формату.
    """

    bin_text = binary_response(text)
    bin_text_correct = clearing_unnecessary_symbols(bin_text)
    text = text_response(bin_text_correct)

    return text


if __name__ == '__main__':
    text = processing_text('100\xa0ч')
    print(text)


