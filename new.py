import random
import proxy_connection as pc
from avito_parameters import AvitoObject
import aux_functions as af
import time
from list_technic import list_technic



class AvitoResearchOneRequest():

    current_reference = None
    research_dom = None
    reference_research = None
    reference_end = None
    last_page = None
    # number_current_page = None

    # attributes gives possibility to stop parsing when necessary equipment is absent in search list
    must_stop = False
    check_count_ad = 0
    status_check = 0


    def __init__(self, region_research, type_technic, name_maker, model_technic):

        self.region_research = region_research.lower()

        # research english version of region_research for input in sentence of research reference
        self.detection_region()

        self.type_technic = type_technic
        self.model_technic = model_technic
        self.name_maker = name_maker

        # Method make part of research reference
        self.set_reference_research()

        # Make loop in wich every time makes object AvitoObject for
        # research parameters for each object of total search
        self.loop_research_page()


    def set_reference_research(self):

        """ Method must make part of future research reference in Avito """
        self.reference_end = ''

        if self.type_technic is not None:
            self.reference_end = self.aux_set_reference_research(self.type_technic, self.reference_end)

        if self.model_technic is not None:
            self.reference_end = self.aux_set_reference_research(self.model_technic, self.reference_end)

        if self.name_maker is not None:
            self.reference_end = self.aux_set_reference_research(self.name_maker, self.reference_end)

        self.reference_research = f'https://www.avito.ru/{self.region_research}?q={self.reference_end}'


    def detection_region(self):

        """ Method gets name of region in russian and return english variant for input in reference """
        dict_region = {'rossiya': ['россия']}

        for key, val in dict_region.items():
            for el in val:

                if el == self.region_research:
                    self.region_research = key

    def set_dom_research(self):

        """ Method returns dom of research page of user request """
        # own
        # self.research_dom = pc.connection_own_ip(self.reference_research)

        # proxy
        mobile_proxy = pc.MobileProxy(self.reference_research)
        self.research_dom = mobile_proxy.get_dom()

    def set_last_search_page(self):

        """ Method takes number of last search page for making next requests """

        if self.research_dom.xpath("//span[@class='pagination-item-1WyVp']"):

            for el in self.research_dom.xpath("//span[@class='pagination-item-1WyVp']"):
                temp_number = el.xpath("./text()")[0]

                if temp_number.isdigit():
                    self.last_page = int(temp_number)
        else:
            self.last_page = 1

    def set_check_correct(self, text_header):

        """ For stopping parsing when necessary equipment
        is absent in search list have to set check_correct """

        self.check_count_ad = 0

        self.init_check_correct(self.type_technic, text_header)
        self.init_check_correct(self.model_technic, text_header)
        self.init_check_correct(self.name_maker, text_header)

        # check_count_ad is necessary for check only current ad, but
        # in that time program counts count of wrong ad. And when count
        # of wrong ads is 3, it means avito has gave wrong list of objects.
        # In this case we finish parsing of current model.

        if self.check_count_ad < 2:
            self.status_check += 1
        else:
            self.status_check = 0

    def init_check_correct(self, input_text, text_header):

        """ Test availability of input_text in text_header """

        if input_text is not None:
            if input_text.lower() in text_header.lower():
                self.check_count_ad += 1

    def loop_research_page(self):

        """
        Method unites methods of setting self.research_dom and doing loop
        for getting dom_current_ad and taking data from them.
        """

        self.set_dom_research()
        self.set_last_search_page()

        if self.last_page != 1:
            for el in range(1, self.last_page + 1):

                # # Set self.number_current_page
                # self.number_current_page = el

                if el != 1:
                    self.reference_research = f'https://www.avito.ru/{self.region_research}?p={el}&q={self.reference_end}'
                    self.set_dom_research()

                self.loop_into_research_page()

                # Next condition let finish parsing, when all ads was done.
                if self.must_stop is True:
                    break

        else:
            self.loop_into_research_page()

            # Set self.number_current_page
            self.number_current_page = 1

    def loop_into_research_page(self):

        """ Loop by ads in current search page """

        for el_ad in self.research_dom.xpath("//div[@class='iva-item-content-m2FiN']"):
            try:

                # wait random time before next research
                self.time_wait()

                # test wrong data in search result
                self.set_check_correct(el_ad.xpath(".//h3[@itemprop='name']/text()")[0])

                if self.status_check == 3:
                    # self.delete_wrong_collection()
                    self.must_stop = True
                    break

                # If check_count_ad = 1, it may mean that a title text
                # is short and name of model in parameters into ad.
                # And we try to check ad again then.

                if self.check_count_ad > 0:
                    # for search correct name of model, except el_ad, i give name of model in user's text request
                    avito = AvitoObject(el_ad, self.name_maker, self.model_technic, self.region_research, self.check_count_ad)
                    af.do_log(self.reference_research,
                              el_ad.xpath(".//div[@class='iva-item-titleStep-2bjuh']/a/@href")[0])

            except Exception as error:

                # leave log about mistakes
                af.print_error(el_ad.xpath(".//div[@class='iva-item-titleStep-2bjuh']/a/@href")[0], error)
                af.save_errors(el_ad.xpath(".//div[@class='iva-item-titleStep-2bjuh']/a/@href")[0], error)


    @staticmethod
    def time_wait():

        """ Do stop parsing during random time """
        time_wait = random.randint(10, 15)
        time.sleep(time_wait)

    @staticmethod
    def aux_set_reference_research(sentence, temp_text):

        """ aux method for insert in research reference """
        if sentence is not None:
            for el in sentence.split(' '):

                if temp_text != "":
                    temp_text = temp_text + '+' + el
                else:
                    temp_text = el

        return temp_text

    def __str__(self):

        """ temp method for testing made self.reference_research """
        return self.reference_research

if __name__ == '__main__':

    # avito_research_one_request = AvitoResearchOneRequest('Россия', 'трактор', 'ростсельмаш', '320')

    for el in list_technic:
        avito_research_one_request = AvitoResearchOneRequest('Россия', el[0], el[1], el[2])


