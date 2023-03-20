import logging

from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import class_mapper

from wxcloudrun import db
from wxcloudrun.model import Counters ,Application

# 初始化日志
logger = logging.getLogger('log')


def query_counterbyid(id):
    """
    根据ID查询Counter实体
    :param id: Counter的ID
    :return: Counter实体
    """
    try:
        return Counters.query.filter(Counters.id == id).first()
    except OperationalError as e:
        logger.info("query_counterbyid errorMsg= {} ".format(e))
        return None


def delete_counterbyid(id):
    """
    根据ID删除Counter实体
    :param id: Counter的ID
    """
    try:
        counter = Counters.query.get(id)
        if counter is None:
            return
        db.session.delete(counter)
        db.session.commit()
    except OperationalError as e:
        logger.info("delete_counterbyid errorMsg= {} ".format(e))


def insert_counter(counter):
    """
    插入一个Counter实体
    :param counter: Counters实体
    """
    try:
        db.session.add(counter)
        db.session.commit()
    except OperationalError as e:
        logger.info("insert_counter errorMsg= {} ".format(e))


def update_counterbyid(counter):
    """
    根据ID更新counter的值
    :param counter实体
    """
    try:
        counter = query_counterbyid(counter.id)
        if counter is None:
            return
        db.session.flush()
        db.session.commit()
    except OperationalError as e:
        logger.info("update_counterbyid errorMsg= {} ".format(e))

def query_application_by_uuid(uuid):
    """
    根据UUID查询Application实体
    :param UUID: Application的UUID
    :return: Application实体
    """
    try:
        app = Application.query.filter(Application.uuid == uuid).first()
        app_dict = dict((col.name, getattr(app, col.name)) for col in class_mapper(Application).mapped_table.c)
        return app_dict
    except OperationalError as e:
        logger.info("query_counterbyid errorMsg= {} ".format(e))
        return None


def list_application():
    try:
        res = Application.query.with_entities(Application.name, Application.description, Application.uuid,Application.eg).all()
        serialized_result = [{
            'name': row[0],
            'description': row[1],
            'uuid': str(row[2]),
            'eg':row[3]
        } for row in res]

        return serialized_result
    except OperationalError as e:
        logger.info("insert_counter errorMsg= {} ".format(e))


def insert_application(application):
    try:
        db.session.add(application)
        db.session.commit()
    except OperationalError as e:
        logger.info("insert_counter errorMsg= {} ".format(e))


def update_application_by_uuid(application):
    """
    根据ID更新Application的值
    :param Application实体
    """
    try:
        application = query_application_by_uuid(application.uuid)
        if application is None:
            return
        db.session.flush()
        db.session.commit()
    except OperationalError as e:
        logger.info("update_counterbyid errorMsg= {} ".format(e))
