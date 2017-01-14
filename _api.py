"""PytSite Content Block Plugin API.
"""
from pytsite import lang as _lang
from plugins import content as _content
from . import _model, _error

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def get_block(uid: str, language: str = None) -> _model.Block:
    """Get block by UID.
    """
    if language is None:
        language = _lang.get_current()

    block = _content.find('content_block', language=language).eq('uid', uid).first()
    if not block:
        raise _error.BlockNotFound("Block '{}' is not found.".format(uid))

    return block
