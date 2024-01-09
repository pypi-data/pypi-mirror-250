# -*- coding: utf-8 -*-
"""
This module shows how to program a command-line tool using plumbum.

It consists of a tool named 'nameoftool' (implemented in the class
CommandLineTool) that has a single sub-command 'say'.

>>> nameoftool say --hello world
dear world

Depending on your preferences in ~/.nameoftool_rc, your output may differ.
If you set 'colloquial' to 'True', it will say 'hello world'.

See `plumbum documentation`_ for more information.

.. _plumbum documentation:
        <https://plumbum.readthedocs.io/en/latest/cli.html#guide-cli>
"""

from plumbum import cli
try:
    from importlib.metadata import version
except ImportError:
    from importlib_metadata import version


class CommandLineTool(cli.Application):
    """
    An example for a command line tool.

    Its name is 'nameoftool' and it provides a single sub-command named 'say'.
    """

    PROGNAME = 'nameoftool'
    VERSION = version('.'.join(__name__.split('.')[:-1]))

    def main(self, *args):
        pass


@CommandLineTool.subcommand('say')
class CLTSay(cli.Application):
    "Say something."

    something = ''

    @cli.switch('--hello')
    def hello(self):
        "Say hello"
        with cli.Config('~/.nameoftool_rc') as config:
            colloquial = config.get('colloquial', False) == 'True'

        if colloquial:
            self.something = 'hello'
        else:
            self.something = 'dear'

    @cli.switch('--bye')
    def bye(self):
        "Say bye"
        self.something = 'bye'

    def main(self, *args):
        print(self.something, *args)


def main():
    CommandLineTool.run()
