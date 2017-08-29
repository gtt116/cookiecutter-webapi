import logging
import multiprocessing

from gevent.wsgi import WSGIServer
import gunicorn.app.base

from {{cookiecutter.module_name}}.api import app
from {{cookiecutter.module_name}} import cfg
from {{cookiecutter.module_name}} import log

LOG = logging.getLogger(__name__)


class GunicornWsgi(gunicorn.app.base.BaseApplication):

    def __init__(self, app, host, port, workers=None):
        """
        The access log format.

        ===========  ===========
        Identifier   Description
        ===========  ===========
        h            remote address
        l            ``'-'``
        u            user name
        t            date of the request
        r            status line (e.g. ``GET / HTTP/1.1``)
        m            request method
        U            URL path without query string
        q            query string
        H            protocol
        s            status
        B            response length
        b            response length or ``'-'`` (CLF format)
        f            referer
        a            user agent
        T            request time in seconds
        D            request time in microseconds
        L            request time in decimal seconds
        p            process ID
        {Header}i    request header
        {Header}o    response header
        {Variable}e  environment variable
        ===========  ===========
        """
        self.app = app
        self.options = {
            'bind': '%s:%s' % (host, port),
            'workers': workers or 1,
            'worker_class': 'gevent',
            'threads': multiprocessing.cpu_count() * 2,
            'accesslog': '-',  # stdout
            'errorlog': '-',   # stdout

            # Gunicorn 19 introduced a breaking change: To compliance with
            # RFC 3875, the REMOTE_ADDR is now the IP address of the
            # proxy and not the actual user(X-Forwarded-For).
            # More discussion can be found here:
            #   https://github.com/benoitc/gunicorn/issues/797
            'access_log_format': ('%({X-Forwarded-For}i)s %(l)s %(u)s %(t)s'
                                  '"%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(L)s')
        }
        super(GunicornWsgi, self).__init__()

    def load_config(self):
        for key, value in self.options.iteritems():
            self.cfg.set(key, value)

    def load(self):
        return self.app


def run_api():
    log.setup()

    host = cfg.config('API').get('host')
    port = cfg.config('API').getint('port')
    workers = cfg.config('API').getint('workers')

    LOG.info("API start listen on http://%s:%s" % (host, port))

    webapp = app.create_webapp()

    if cfg.config().getboolean('debug'):
        # gunicorn does't support pdb, so debug mode using gevent wsgi server.
        http_server = WSGIServer((host, port), webapp)
        http_server.serve_forever()
    else:
        GunicornWsgi(webapp, host, port, workers=workers).run()
