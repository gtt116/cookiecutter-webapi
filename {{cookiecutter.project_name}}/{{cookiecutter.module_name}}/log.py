import logging

from {{cookiecutter.module_name}} import cfg


def setup():
    logging.basicConfig(
        format=(u'%(asctime)s %(levelname)-8s [%(name)s] %(message)s')
    )
    root_logger = logging.getLogger()

    if cfg.config()['debug']:
        root_logger.setLevel(logging.DEBUG)
    else:
        root_logger.setLevel(logging.INFO)

    for l in ['requests', 'urllib3']:
        log = logging.getLogger(l)
        log.setLevel(logging.WARN)

    for l in ['PIL']:
        log = logging.getLogger(l)
        log.setLevel(logging.INFO)
