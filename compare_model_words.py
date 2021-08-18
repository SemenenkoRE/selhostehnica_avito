


def compare_models_init(header_text, user_model, index_compare):

    """
    Method searches places of words of name model in text of header.
    """

    index_first, index_second = None, None
    user_model_expr = None

    # Make whole sentence of header words.

    if len(user_model.split(' ')) == 2:
        user_model_expr = f"{user_model.split(' ')[0]}{user_model.split(' ')[1]}"
    elif len(user_model.split(' ')) == 1:
        user_model_expr = user_model
    
    # Make dict with word of text of ad's header
    
    i = 0
    dict_word_ad = {}

    for el in header_text.split(' '):
        dict_word_ad[i] = el
        i += 1

    # value status will check
    status = None

    # in first procedure find word of name of model. It
    # works if only name of model consist of one word.
    for key, val in dict_word_ad.items():
        i = 0

        if status is not True:
            user_model_list = []

            # Make list of words of user name model
            for letter in user_model_expr:
                user_model_list.append(letter)

            # Make list of words of next word in list of val of dict_word_ad
            val_list = []
            for letter in val:
                val_list.append(letter)

            for n, el in enumerate(val_list):
                for n_, el_ in enumerate(user_model_list):

                    if el == el_:
                        val_list[n] = '*'
                        user_model_list[n_] = '*'
                        i += 1

            # После выполнения перебора всех элементов val_list сравнивается значение
            # количесва уникальный совпадений i и количесво символов в выражениях user_model_list и val_list.
            # В случае если отношение значений i и длины выражений соответствует необходимому,
            # то status меняется на True, переменные index_first, index_second получают необходимые значения

            if i / len(user_model_list) >= index_compare and i / len(val_list) >= index_compare:
                index_first, index_second = key, None
                status = True
                break

    # in second way find words of name if model does not consist of one word.

    if index_first is None:
        for key, val in dict_word_ad.items():
            status = None

            for key_again, val_again in dict_word_ad.items():

                if status is not True:

                    # Not to do extra work use condition
                    if val != val_again:
                        i = 0
                        user_model_list = []

                        for letter in user_model_expr:
                            user_model_list.append(letter)

                        val_list = []

                        for letter in f'{val}{val_again}':
                            val_list.append(letter)

                        for n, el in enumerate(val_list):
                            for n_, el_ in enumerate(user_model_list):

                                if el == el_:
                                    val_list[n] = '*'
                                    user_model_list[n_] = '*'
                                    i += 1

                        if i / len(user_model_list) >= index_compare and i / len(val_list) >= index_compare:
                            index_first, index_second = min(key, key_again), max(key, key_again)
                            status = True
                            break

    return index_first, index_second


def compare_models(header_text, user_model):

    """
    Procedure look at count of concurrence in text of header and text of user_model.
    For accuracy, in first use count of concurrence like 90% and in second 80%.
    """

    index_first, index_second = compare_models_init(header_text, user_model, 0.9)

    if index_first is None:
        compare_models_init(header_text, user_model, 0.8)

    return index_first, index_second


if __name__ == '__main__':

    result = compare_models('продается модель 20800 800', '800')
    print(result)
