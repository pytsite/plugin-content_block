"""PytSite Content Block Plugin.
"""
from . import _error as error
from ._api import is_defined, define, get, get_all

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def _init():
    from pytsite import tpl, lang
    from plugins import content
    from . import _model, _api

    # Resources
    lang.register_package(__name__, alias='content_block')

    # Content model
    content.register_model('content_block', _model.Block, 'content_block@blocks', 1000, 'fa fa-th')

    # Tpl global callback
    def tpl_render_block(*args, **kwargs) -> str:
        try:
            return get(*args, **kwargs).body
        except error.BlockNotDefined:
            return ''

    # Tpl globals
    tpl.register_global('get_content_block', get)
    tpl.register_global('content_block', tpl_render_block)


_init()
