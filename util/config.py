import configparser


def _read_config():
    """加载配置文件"""
    config_name = r"config.ini"
    config = configparser.ConfigParser()
    config.read(config_name, "utf-8")
    return config


def get_config(section, option):
    """获取配置信息"""
    config = _read_config()
    return config.get(section, option)
