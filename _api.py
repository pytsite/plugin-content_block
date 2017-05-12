"""PytSite Content Block Plugin API.
"""
from pytsite import lang as _lang, auth as _auth
from plugins import content as _content
from . import _model, _error

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

_VALID_BLOCK_TYPES = ('text', 'wysiwyg')
_blocks = {}


def is_defined(uid: str, language: str = 'n') -> bool:
    """Check whether block is defined.
    """
    return (uid, language) in _blocks


def define(uid: str, title: str, content_type: str = 'wysiwyg', language: str = 'n') -> _model.Block:
    """Define block.
    """
    if is_defined(uid, language):
        raise _error.BlockAlreadyDefined("Block '{}' for language '{}' is already defined".format(uid, language))

    if content_type not in _VALID_BLOCK_TYPES:
        raise ValueError('Invalid content type: {}'.format(content_type))

    _blocks[(uid, language)] = content_type

    try:
        block = get(uid, language)
    except _error.BlockNotFound:
        _auth.switch_user_to_system()
        block = _content.dispense('content_block')
        block.f_set('block_uid', uid).f_set('language', language).f_set('title', title).save()
        _auth.restore_user()

    return block


def get(uid: str, language: str = None) -> _model.Block:
    """Get block.
    """
    language = language or _lang.get_current()
    f = _content.find('content_block', language='*').inc('language', (language, 'n')).eq('block_uid', uid)
    block = f.first()  # type: _model.Block
    if not block:
        raise _error.BlockNotFound("Block '{}' for language '{}' is not found".format(uid, language))

    try:
        block.content_type = _blocks[(uid, language)]
    except KeyError:
        block.content_type = _blocks[(uid, 'n')]

    return block


def get_blocks() -> dict:
    """Get all defined blocks.
    """
    return _blocks
