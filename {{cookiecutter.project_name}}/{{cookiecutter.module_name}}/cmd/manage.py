# -*- coding:utf-8 -*-
import os
import argparse
import logging

from alembic import config as alembic_config
from alembic import command as alembic_command
from alembic import util as alembic_util

from {{cookiecutter.module_name}} import cfg
from {{cookiecutter.module_name}} import log
from {{cookiecutter.module_name}} import db

LOG = logging.getLogger(__name__)


def do_alembic_command(cmd, *args, **kwargs):
    folder_name = 'alembic'
    db_url = cfg.config('DB').get('sql_connection')

    configx = alembic_config.Config(
        os.path.join(os.path.abspath(os.path.dirname(db.__file__)),
                     folder_name, 'alembic.ini')
    )
    configx.set_main_option('script_location', '{{cookiecutter.module_name}}.db:%s' % folder_name)
    configx.set_main_option('sqlalchemy.url', db_url)

    try:
        getattr(alembic_command, cmd)(configx, *args, **kwargs)
    except alembic_util.CommandError as e:
        alembic_util.err(str(e))


def do_upgrade(args):
    if not args.revision:
        raise SystemExit("You must provide a revision, maybe 'head' is great")

    do_alembic_command('upgrade', args.revision, sql=args.sql)


def do_downgrade(args):
    if not args.revision:
        raise SystemExit("You must provide a revision, maybe 'head' is great")

    do_alembic_command('downgrade', args.revision, sql=args.sql)


def do_revision(args):
    do_alembic_command('revision',
                       message=args.message,
                       autogenerate=args.autogenerate,
                       sql=args.sql)


def do_history(args):
    do_alembic_command('history')


def do_version(args):
    do_alembic_command('current')


def do_shell(args):
    try:
        _launch_ipython()
    except ImportError:
        _launch_python()


def do_dump_config(args):
    # force all config return to default value
    reload(cfg)
    cfg.dump_example_config()


def _launch_ipython():
    try:
        from IPython import embed
        embed()
    except ImportError:
        # Ipython < 0.11
        # Explicitly pass an empty list as arguments, because
        # otherwise IPython would use sys.argv from this script.
        import IPython

        shell = IPython.Shell.IPShell(argv=[])
        shell.mainloop()


def _launch_python():
    import code
    try:
        # Try activating rlcompleter, because it's handy.
        import readline
    except ImportError:
        pass
    else:
        # We don't have to wrap the following import in a 'try',
        # because we already know 'readline' was imported successfully.
        readline.parse_and_bind("tab:complete")
    code.interact()


def main():
    main_parser = argparse.ArgumentParser()
    main_parser.add_argument('-c', '--config', help='config file path')
    main_parser.add_argument("-v", "--verbose",
                             help="increase output verbosity",
                             action="store_true")

    subparsers = main_parser.add_subparsers()

    parser = subparsers.add_parser('upgrade')
    parser.add_argument('--sql', action='store_true')
    parser.add_argument('revision', nargs='?')
    parser.set_defaults(func=do_upgrade)

    parser = subparsers.add_parser('downgrade')
    parser.add_argument('--sql', action='store_true')
    parser.add_argument('revision', nargs='?')
    parser.set_defaults(func=do_downgrade)

    parser = subparsers.add_parser('version',
                                   help="print current database version")
    parser.set_defaults(func=do_version)

    parser = subparsers.add_parser('history',
                                   help="print database migration history")
    parser.set_defaults(func=do_history)

    parser = subparsers.add_parser('revision')
    parser.add_argument('-m', '--message')
    parser.add_argument('--autogenerate', action='store_true', default=True)
    parser.add_argument('--sql', action='store_true')
    parser.set_defaults(func=do_revision)

    parser = subparsers.add_parser('shell',
                                   help="jump into a python shell")
    parser.set_defaults(func=do_shell)

    parser = subparsers.add_parser(
        'dump_config', help="Dump example config into {{cookiecutter.module_name}}.conf.sample")
    parser.set_defaults(func=do_dump_config)

    args = main_parser.parse_args()

    if args.config:
        cfg.load_config(args.config)
    else:
        cfg.load_config()

    log.setup()
    args.func(args)


if __name__ == '__main__':
    main()
