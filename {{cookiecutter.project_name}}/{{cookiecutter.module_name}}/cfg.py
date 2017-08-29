import logging
from os import path as os_path

import configparser


LOG = logging.getLogger(__name__)
_load = False
_CFG = configparser.ConfigParser(allow_no_value=True)


def _get_etc_dir():
    """The root directory of project, such as `/home/{{cookiecutter.project_name}}/etc`"""
    return os_path.join(os_path.dirname(os_path.abspath(__file__)),
                        os_path.pardir, 'etc')


def load_config(path=None, default=False):
    '''
    Optional function for load config file in specific path.

    This function is usually called in first place i.e. before any
    one calling config()
    '''
    global _load
    if not default:
        path = path or os_path.join(_get_etc_dir(), '{{cookiecutter.module_name}}.conf')
        _CFG.read(path)
    _load = True


def config(section='DEFAULT'):
    """Get an section from configuration"""
    global _load
    if _load:
        return _CFG[section]
    else:
        raise Exception("Config not load")


def register(section, name, value, comment=None):
    """
    All default configuration must be declared here before using it.
    """
    if section != 'DEFAULT' and not _CFG.has_section(section):
        _CFG.add_section(section)

    if comment:
        _CFG.set(section, '# %s' % comment)
    _CFG.set(section, name, value)


def dump_example_config():
    path = os_path.join(_get_etc_dir(), '{{cookiecutter.module_name}}.conf.sample')
    with open(path, 'w') as configfile:
        _CFG.write(configfile)
    LOG.info("Generate sample config file: %s successfully." % path)


register('DEFAULT', 'debug', 'False', comment='whether enable debug logging')
register('API', 'host', '127.0.0.1', comment='The host which api will bind')
register('API', 'port', '8888', comment='The port which api will bind')
register('API', 'workers', '4', comment='The number of gunicorn workers')
register('DB', 'sql_connection', 'mysql://root@localhost/{{cookiecutter.module_name}}',
         comment='sql connection for {{cookiecutter.module_name}}')
