"""PytSite Content Block Plugin
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite import plugman as _plugman

if _plugman.is_installed(__name__):
    # Public API
    from . import _error as error
    from ._api import is_defined, define, get


def plugin_load():
    from pytsite import tpl, lang
    from plugins import content
    from . import _model, _api

    # Resources
    lang.register_package(__name__, alias='content_block')

    # Content model
    content.register_model('content_block', _model.Block, 'content_block@blocks', 1000, 'fa fa-th')

    # Tpl globals
    tpl.register_global('content_block', get)
