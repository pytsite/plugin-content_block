"""PytSite Content Block Plugin.
"""
from . import _error as error
from ._api import get_block

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
    def tpl_global_render_block(*args, **kwargs) -> str:
        try:
            return get_block(*args, **kwargs).body
        except error.BlockNotFound:
            return ''

    # Tpl globals
    tpl.register_global('content_block', tpl_global_render_block)


_init()
