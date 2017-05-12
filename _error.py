"""PytSite Content Block Plugin Errors
"""

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class BlockNotDefined(Exception):
    pass


class BlockAlreadyDefined(Exception):
    pass


class BlockNotFound(Exception):
    pass
