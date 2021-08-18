from sqlalchemy import create_engine
from sqlalchemy import and_         # для выполнения объединия WHERE
from sqlalchemy.orm import sessionmaker
from create_db import AvitoTechnic
from sqlalchemy import desc
import datetime


class SqlAddAvitoTechnic:

    """
    Класс отвечает за добавление сведений в таблицу CommecialRealEstate.
    Для каждой таблицы базы данных "data_base_1" должен существовать свой класс.
    """

    engine = create_engine("mysql+pymysql://root:111111@localhost/data_base_avito", echo=True)

    def __init__(self, **kwargs):
        self.filling_data(kwargs)

    def filling_data(self, values_collection):
        session = sessionmaker(bind=self.engine)
        session = session()
        session.add(AvitoTechnic(id=values_collection['id'],
                                    hex_id=values_collection['hex_id'],
                                    reference_ad=values_collection['reference_ad'],
                                    title_text=values_collection['title_text'],
                                    type_technic=values_collection['type_technic'],
                                    price=values_collection['price'],
                                    offer_datetime=values_collection['offer_datetime'],
                                    address=values_collection['address'],
                                    area=values_collection['area'],
                                    model_request=values_collection['model_request'],
                                    model_research=values_collection['model_research'],
                                    model_exact=values_collection['model_exact'],
                                    year=values_collection['year'],
                                    condition=values_collection['condition'],
                                    maker=values_collection['maker'],
                                    maker_request=values_collection['maker_request'],
                                    moto_hours=values_collection['moto_hours'],
                                    document=values_collection['document']))
        session.commit()


class SqlDataBaseQuery:

    """
    Класс отвечает за выполнение запросов к базе данных data_base_1.
    """

    engine = create_engine("mysql+pymysql://root:111111@localhost/data_base_avito", echo=True)

    def __init__(self):
        self.session = sessionmaker(bind=self.engine)
        self.session = self.session()

    def query_get_all(self):

        """
        Получение всех сведений сведений из базы данных
        """

        result = self.session.query(AvitoTechnic).all()

        for row in result:
            print("Id: ", row.id, "\nhex_id: ", row.hex_id, "\nreference_ad: ", row.reference_ad,
                  "\ntitle_text: ", row.title_text, "\ntype_technic: ", row.type_technic, "\nprice: ", row.price,
                  "\noffer_datetime: ", row.offer_datetime, "\naddress: ", row.address, "\narea: ", row.area,
                  "\nmodel_request: ", row.model_request, "\nmodel_research: ", row.model_research,
                  "\nmodel_exact: ", row.model_exact, "\nyear: ", row.year, "\ncondition: ", row.condition,
                  "\nmaker: ", row.maker, "\nmaker_request: ", row.maker_request, "\nmoto_hours: ", row.moto_hours,
                  "\ndocument: ", row.document, "\n************")


    def query_get_data_id(self, research_id):

        """
        Получение сведений о коллекции определенного id.
        """

        result = self.session.query(AvitoTechnic).all()

        for row in result:
            if row.id == research_id:
                print("Id: ", row.id, "\nhex_id: ", row.hex_id, "\nreference_ad: ", row.reference_ad,
                      "\ntitle_text: ", row.title_text, "\ntype_technic: ", row.type_technic, "\nprice: ", row.price,
                      "\noffer_datetime: ", row.offer_datetime, "\naddress: ", row.address, "\narea: ", row.area,
                      "\nmodel_request: ", row.model_request, "\nmodel_research: ", row.model_research,
                      "\nmodel_exact: ", row.model_exact, "\nyear: ", row.year, "\ncondition: ", row.condition,
                      "\nmaker: ", row.maker, "\nmaker_request: ", row.maker_request, "\nmoto_hours: ", row.moto_hours,
                      "\ndocument: ", row.document, "\n************")

    def query_delete_row(self, research_id):

        """
        Удаление коллекции с выбранным id.

        DELETE FROM commercial_objects WHERE id = 3;
        """

        result = self.session.query(AvitoTechnic).all()

        for row in result:
            if row.id == research_id:
                self.session.delete(row)
                self.session.commit()


    def query_get_last_id(self):

        """
        Получение унркального id для добавляемой строки.
        """
        last_id = None
        result = self.session.query(AvitoTechnic).order_by(desc(AvitoTechnic.id))

        for row in result:
            last_id = row.id + 1
            break

        return last_id


if __name__ == '__main__':

    sql_query = SqlDataBaseQuery()
    sql_query.query_get_all()
    # sql_query.query_get_data_id(45)
    # sql_query.query_delete_row(45)
    # print(sql_query.query_get_last_id())

