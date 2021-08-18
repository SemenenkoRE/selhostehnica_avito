import compare_model_words as cmw
import proxy_connection as pc
import set_datetime as sd
import hashlib
from pymongo import MongoClient
from use_db import SqlAddAvitoTechnic, SqlDataBaseQuery
import binary_processing_text as bpt


class AvitoObject:

    name_data_base = 'data_base_avito_new'
    data_base = None
    check_id = None
    current_ad_dom = None
    title_text = None
    reference_ad = None
    unique_id = None
    offer_date_time = None
    address = None
    price = None
    model_aux = None
    model_research = None
    model_exact = None
    type_technic = None

    year = None
    condition = None
    maker = None
    moto_hours = None
    documentation = None


    def __init__(self, header_ad, maker_text_request, model_text_request, area, test_count):

        # Set area of search
        self.area = area

        # Object with data about object from research page
        self.header_ad = header_ad

        # Make attribute, which contains value of text of requested maker.
        # Use only for adding to data base
        self.maker_text_request = maker_text_request

        # Make attribute, which contains value of text of requested maker
        self.model_text_request = model_text_request

        # Make attribute, which is necessary for check this ad.
        self.test_count = test_count

        # Activate data base Mongod
        self.set_data_base()

        # Main method, which unites other methods
        self.get_parameters()


    def set_data_base(self):

        """ Make object with data base of MongoDB """
        client = MongoClient('localhost', 27017)
        db = client[self.name_data_base]
        self.data_base = db.data_base

    def check_mongodb(self):

        """ Method compares hex_id current object an other hex_id from data_base """
        for n in self.data_base.find({'hex_id': self.unique_id}):
            self.check_id = 'stop'

    def add_object_sql(self, last_id):

        """ Add collection of parameters to SQL """
        sql_add = SqlAddAvitoTechnic(id=last_id,
                                        hex_id=self.unique_id,
                                        reference_ad=self.reference_ad,
                                        title_text=self.title_text,
                                        type_technic=self.type_technic,
                                        price=self.price,
                                        offer_datetime=self.offer_date_time,
                                        address=self.address,
                                        area=self.area,
                                        model_request=self.model_text_request,
                                        model_research=self.model_research,
                                        model_exact=self.model_exact,
                                        year=self.year,
                                        condition=self.condition,
                                        maker=self.maker,
                                        maker_request=self.maker_text_request,
                                        moto_hours=self.moto_hours,
                                        document=self.documentation)



    def add_object_mongodb(self, last_id):

        """ Add collection of parameters to MongoDB """
        self.data_base.insert_one(
            {'_id': last_id, 'hex_id': self.unique_id, 'reference_ad': self.reference_ad,
             'title_text: ': self.title_text, 'type_technic': self.type_technic, 'price': self.price,
             'offer_datetime': self.offer_date_time, 'address': self.address, 'area': self.area,
             'model_request': self.model_text_request, 'model_research': self.model_research,
             'model_exact': self.model_exact, 'year': self.year, 'condition': self.condition,
             'maker': self.maker, 'maker_request': self.maker_text_request, 'moto_hours': self.moto_hours,
             'document': self.documentation})

    def add_parameters_sql_mongod(self):

        """ Method gives values of parameters to sql and mongo db """
        if self.check_id != 'stop':

            # Get number of last id in sql data base
            sql_query = SqlDataBaseQuery()
            last_id = sql_query.query_get_last_id()

            if last_id is None:
                last_id = 1

            # Add values of parameters to data bases
            self.add_object_sql(last_id)
            self.add_object_mongodb(last_id)

    def get_data_header(self):

        """ Getting init data from self.header_ad, which has come from research page. """

        # Get data about price, maybe not exactly yet

        self.price = self.header_ad.xpath(
            ".//div[@class='iva-item-priceStep-2qRpg']//span[@class='price-text-1HrJ_ text-text-1PdBw text-size-s-1PUdo']/text()")[0]
        self.aux_header_price()

        # Get name of model for use in search in data base and for user.

        text_header_ad = self.header_ad.xpath(".//div[@class='iva-item-titleStep-2bjuh']//h3/text()")[0]
        self.get_names_model(text_header_ad)

        # Get reference of ad

        self.reference_ad = self.header_ad.xpath(".//div[@class='iva-item-titleStep-2bjuh']/a/@href")[0]
        self.reference_ad = f'https://www.avito.ru{self.reference_ad}'

        # Get address
        self.address = self.header_ad.xpath(
                                ".//span[@class='geo-address-9QndR text-text-1PdBw text-size-s-1PUdo']/span/text()")[0]



    def aux_header_price(self):

        """ Method tests title with price and then decides how to use that. """

        if self.price != 'Цена не указана':
            self.price = float(bpt.processing_text(self.price).replace(' ', ''))
            # self.price = float(self.price.replace(' ', ''))

        else:
            self.price = None

    def get_names_model(self, text_header_ad):

        """ Method researches data about object of technic before transfer to ad """

        if self.model_text_request is not None:

            text_header_ad = self.processing_word_symbol(text_header_ad)
            index_first, index_second = cmw.compare_models(text_header_ad, self.model_text_request)

            if index_first is not None and index_second is not None:

                self.model_aux = self.make_model_for_user(self.model_aux, text_header_ad.split(' ')[index_first])
                self.model_aux = self.make_model_for_user(self.model_aux, text_header_ad.split(' ')[index_second])
                self.make_model_for_research()
                self.set_model_research()

            elif index_first is not None:

                self.model_aux = self.make_model_for_user(self.model_aux, text_header_ad.split(' ')[index_first])
                self.make_model_for_research()
                self.set_model_research()

            else:

                for element in text_header_ad.split(' '):
                    status_symbol_model, status_digit_model = None, None

                    # Because of symbol is a feature of model then,
                    # we find them in word and use like model

                    status_symbol_model = self.test_symbol_model(element)

                    if status_symbol_model is False:

                        # Like with symbol as a feature of model
                        # we find digit in word and use like model.

                        status_digit_model = self.test_digit(element)

                    if status_symbol_model is True or status_symbol_model is True:
                        self.model_aux = self.make_model_for_user(self.model_aux, element)

                # Because these names will use in search requests, so we have to make
                # this work more simple and so we change symbols in name model on "_".

                self.make_model_for_research()
                self.set_model_research()


    def research_ad(self):

        """
        Method research one ad
        """

        # own
        # self.current_ad_dom = rp.connection_own_ip(self.reference_ad)

        # proxy
        mobile_proxy = pc.MobileProxy(self.reference_ad)
        self.current_ad_dom = mobile_proxy.get_dom()

        self.title_text = self.current_ad_dom.xpath("//span[@class='title-info-title-text']/text()")[0]
        self.offer_date_time = sd.set_time_ad(self.current_ad_dom.xpath(
                                                    "//div[@class='title-info-metadata-item-redesign']/text()")[0])

        for page_ad in self.current_ad_dom.xpath("//ul[@class='item-params-list']/li"):

            if page_ad.xpath(".//span/text()")[0] == 'Тип техники: ':
                self.type_technic = page_ad.xpath("./text()")[1].lower()

            elif page_ad.xpath(".//span/text()")[0] == 'Год выпуска: ':
                self.year = int(page_ad.xpath("./text()")[1].lower())

            elif page_ad.xpath(".//span/text()")[0] == 'Состояние: ':
                self.condition = page_ad.xpath("./text()")[1].lower()

            elif page_ad.xpath(".//span/text()")[0] == 'Марка: ':
                self.maker = page_ad.xpath("./text()")[1].lower()

            elif page_ad.xpath(".//span/text()")[0] == 'Модель: ':
                self.model_exact = page_ad.xpath("./text()")[1].lower()

            elif page_ad.xpath(".//span/text()")[0] == 'Моточасы: ':
                self.moto_hours = int(self.del_letters_moto_hours(bpt.processing_text(page_ad.xpath("./text()")[1].
                                                                                      split(' ')[0])))

            elif page_ad.xpath(".//span/text()")[0] == 'ПТС или ПСМ: ':
                self.documentation = page_ad.xpath("./text()")[1].lower()

        # get address
        # self.address = bpt.processing_text(self.current_ad_dom.xpath("//span[@class='item-address__string']/text()")[0])

        # make self.unique_id
        self.get_cript_id()


    def get_parameters(self):

        self.get_data_header()
        self.research_ad()

        # This test is last step of more global checking the correctness of the current ad

        if self.model_exact is not None and self.model_text_request is not None:

            if self.test_count > 1 or (self.test_count == 1 and self.model_text_request in self.model_exact):
                self.show_result()
                self.check_mongodb()
                self.add_parameters_sql_mongod()

        else:
            if self.test_count > 2:
                self.show_result()
                self.check_mongodb()
                self.add_parameters_sql_mongod()



    def get_cript_id(self):

        """ Method make special unique ID """

        if self.year is not None and self.model_exact is not None:
            self.unique_id = hashlib.sha1(f'{self.price}{self.year}{self.title_text}{self.model_exact}{self.address}'
                                          .encode('utf-8')).hexdigest()

        elif self.year is None and self.model_exact is not None:
            self.unique_id = hashlib.sha1(f'{self.price}{self.title_text}{self.model_exact}{self.address}'
                                          .encode('utf-8')).hexdigest()

        elif self.model_exact is None and self.year is not None:
            self.unique_id = hashlib.sha1(f'{self.price}{self.title_text}{self.model_exact}{self.address}'
                                          .encode('utf-8')).hexdigest()

        elif self.model_exact is None and self.year is None:
            self.unique_id = hashlib.sha1(f'{self.price}{self.title_text}{self.address}'.encode('utf-8')).hexdigest()

    def show_result(self):

        print('reference_ad: ', self.reference_ad)
        print('unique_id: ', self.unique_id)
        print('address: ', self.address)
        print('type_technic: ', self.type_technic)
        print('price: ', self.price)
        print('offer_datetime: ', self.offer_date_time)
        print('model_request', self.model_text_request)
        print('model_research: ', self.model_research)
        print('model_exact: ', self.model_exact)
        print('year: ', self.year)
        print('condition: ', self.condition)
        print('maker: ', self.maker)
        print('maker_text_request: ', self.maker_text_request)
        print('moto_hours: ', self.moto_hours)
        print('documentation: ', self.documentation)

    @staticmethod
    def test_digit(word):

        """ Method test availability of digit in incoming word, because digits usually can be in word of model. """
        status = False

        if len(word) > 1:
            for el in word:

                if el.isdigit():
                    status = True

        return status

    @staticmethod
    def test_symbol_model(word):

        """ Method test availability of symbol in word of header part, because of model then. """
        symbols_model = ['-', '.', '_', '/', '—', '(', ')', ' ']

        status = False
        for el in symbols_model:

            if el in word:
                status = True

        return status

    @staticmethod
    def del_letters_moto_hours(word):

        """ Method delete letters in word of attribute moto_hours """
        temp_word = ''
        for el in word:

            if el.isdigit():
                temp_word = temp_word + el

        return temp_word

    @staticmethod
    def processing_word_symbol(header_ad):

        """
        Method:
            1. delete point in the end of sentence
            2. delete excess symbols from text of title (header) like , or ) ...
            3. delete expressions like "л.с." or "л.с"
            4. delete year from text, because then program can confuse it with a name of model
        """

        # 1.

        if header_ad[-1] == ".":
            header_ad = header_ad[:-1]

        # 2.

        symbols_delete = ['"', '(', ')']

        for el in symbols_delete:

            if el in header_ad:
                header_ad = header_ad.replace(el, '')

        # 3.

        if "л.с." in header_ad:
            header_ad = header_ad.replace("л.с.", '')

        if "л.с" in header_ad:
            header_ad = header_ad.replace("л.с", '')

        # 4.

        years = ['2021', '2020', '2019', '2018', '2017', '2016', '2015', '2014', '2013', '2012', '2011', '2010', '2009',
                 '2008', '2007', '2006', '2005', '2004', '2003', '2002', '2001', '2000', '1999', '1998', '1997', '1996',
                 '1995', '1994', '1993', '1992', '1991', '1990', '1989', '1988', '1987', '1986', '1985', '1984', '1983',
                 '1982']

        for year in years:

            if year in header_ad:
                header_ad = header_ad.replace(year, '')

        return header_ad

    def make_model_for_research(self):

        """ Method form value of model_for_research. """

        symbols_model_research = ['-', '.', '_', '/', '—', '(', ')', ' ']

        if self.model_aux is not None:
            self.model_research = self.model_aux[:]

            for letter in self.model_research:
                for el in symbols_model_research:

                    if letter == el:
                        self.model_research = self.model_research.replace(letter, '_')

    def set_model_research(self):

        """ Change capital letters in word of model_for_research. """

        if self.model_research is not None:
            model_for_research_new = ''

            for el in self.model_research:

                if el.isupper():
                    model_for_research_new = f'{model_for_research_new}{el.lower()}'
                else:
                    model_for_research_new = f'{model_for_research_new}{el}'

            self.model_research = model_for_research_new

    @staticmethod
    def make_model_for_user(model_for_user, element_header):

        """ Method form value model_for_user """

        if model_for_user is None:
            model_for_user = element_header

        else:
            model_for_user = f'{model_for_user} {element_header}'

        return model_for_user


# if __name__ == '__main__':
#
#     processing_page_technic('трактор')

