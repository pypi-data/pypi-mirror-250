"""
Module that contains the command line app.

Why does this file exist, and why not put this in __main__?

  You might be tempted to import things from __main__ later, but that will cause
  problems: the code will get executed twice:

  - When you run `python -mluis_v_subtitler` python will execute
    ``__main__.py`` as a script. That means there will not be any
    ``luis_v_subtitler.__main__`` in ``sys.modules``.
  - When you import __main__ it will get executed again (as a module) because
    there"s no ``luis_v_subtitler.__main__`` in ``sys.modules``.

  Also see (1) from http://click.pocoo.org/5/setuptools/#setuptools-integration
"""
import logging

import click

from .utils import basic_test

# Configure logging settings
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


@click.command()
@click.argument("names", nargs=-1)
def main(names):
    basic_test()
    click.echo(repr(names))
