"""PytSite Content Block Plugin
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

# Public API
from . import _error as error
from ._api import is_defined, define, get


def plugin_load():
    from pytsite import tpl, lang
    from plugins import content, permissions
    from . import _model, _api

    # Resources
    lang.register_package(__name__, alias='content_block')

    # Permissions group
    permissions.define_group('content_block', 'content_block@blocks')

    # Content model
    content.register_model('content_block', _model.Block, 'content_block@blocks', 0, 'fa fa-th', 'settings')

    # Tpl globals
    tpl.register_global('content_block', get)
