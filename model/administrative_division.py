class AdministrativeDivision(object):
    """行政区域"""

    def __init__(self, id=0, name="", administrative_level_id=0, administrative_type_id=0, administrative_code="",
                 parent_administrative_division_id=0):
        self.id = id
        self.name = name  # 区域名称
        self.administrative_level_id = administrative_level_id  # 行政级别
        self.administrative_type_id = administrative_type_id  # 行政类型
        self.administrative_code = administrative_code  # 行政代码
        self.parent_administrative_division_id = parent_administrative_division_id  # 父级行政区域id


