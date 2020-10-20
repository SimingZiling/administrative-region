import configparser

from dao import administrative_level_dao, administrative_type_dao, administrative_division_dao
from gather import ministry_of_civil_affairs_of_china
from model.administrative_division import AdministrativeDivision
from model.administrative_level import AdministrativeLevel
from model.administrative_type import AdministrativeType


def _init_table():
    """
    初始化表
    """
    print("初始化行政级别表...")
    administrative_level_dao.create_table()
    print("初始化行政类型表...")
    administrative_type_dao.create_table()
    print("初始化行政区划表...")
    administrative_division_dao.create_table()


def _init_state():
    print("初始化国家(此处只初始化中国)...")
    # 获取中国的行政类型区域id 如果没有则添加
    administrative_division_name = "中华人民共和国"
    administrative_division = administrative_division_dao.find_administrative_division_by_name(
        administrative_division_name)
    if administrative_division is not None:
        administrative_division_id = administrative_division.id
    else:
        # 获取国的行政级别id 如果没有则添加
        administrative_level_name = "国"
        administrative_level = administrative_level_dao.find_administrative_level_by_name(administrative_level_name)
        # 当该行政级别不存在时添加
        if administrative_level is not None:
            administrative_level_id = administrative_level.id
        else:
            administrativeLevel = AdministrativeLevel()
            administrativeLevel.name = administrative_level_name
            administrative_level_id = administrative_level_dao.save(administrativeLevel).id
        # 获取国家的行政类型id 如果没有则添加
        administrative_type_name = "国家"
        administrative_type = administrative_type_dao.find_administrative_type_by_name(administrative_type_name)
        # 当该行政类型不存在时添加
        if administrative_type is not None:
            administrative_type_id = administrative_type.id
        else:
            administrativeType = AdministrativeType()
            administrativeType.name = administrative_type_name
            administrative_type_id = administrative_type_dao.save(administrativeType).id
        administrativeDivision = AdministrativeDivision(0, administrative_division_name,administrative_level_id, administrative_type_id, '00')
        administrative_division_id = administrative_division_dao.save(administrativeDivision).id
    return administrative_division_id


def _start():
    print("开始初始化表！")
    _init_table()
    _state_id = _init_state()
    ministry_of_civil_affairs_of_china.start(_state_id)


if __name__ == '__main__':
    _start()
