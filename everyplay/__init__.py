"""Python Everyplay API Wrapper."""

__version__ = '0.3.5'
__all__ = ['Client']

USER_AGENT = 'Everyplay Python API Wrapper %s' % __version__

from everyplay.client import Client
