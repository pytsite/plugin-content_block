"""PytSite Content Block Plugin API
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite import lang as _lang
from plugins import auth as _auth, content as _content
from . import _model, _error

_VALID_BLOCK_TYPES = ('text', 'wysiwyg')
_BLOCKS = {}


def is_defined(uid: str, language: str = None) -> bool:
    """Check whether block is defined
    """
    if not language:
        language = _lang.get_current()

    if language not in _lang.langs():
        raise ValueError("Language '{}' is not defined".format(language))

    return (uid, language or _lang.get_current()) in _BLOCKS


def define(uid: str, title: str, content_type: str = 'wysiwyg', language: str = None) -> _model.Block:
    """Define a block
    """
    # Check whether a block is already defined
    if is_defined(uid, language):
        raise _error.BlockAlreadyDefined("Block '{}' for language '{}' is already defined".
                                         format(uid, language or _lang.get_current()))

    # Check block's content type
    if content_type not in _VALID_BLOCK_TYPES:
        raise ValueError('Invalid content type: {}'.format(content_type))

    _BLOCKS[(uid, language)] = content_type

    try:
        # Try to load block from the database
        block = get(uid, language)

        # Update content type if it was changed
        if block.content_type != content_type:
            _auth.switch_user_to_system()
            block.f_set('content_type', content_type).save()
            _auth.restore_user()

    except _error.BlockDataNotFound:
        # Block is not found in the database, create it
        _auth.switch_user_to_system()
        block = _content.dispense('content_block')
        block \
            .f_set('block_uid', uid) \
            .f_set('content_type', content_type) \
            .f_set('language', language) \
            .f_set('title', title) \
            .save()
        _auth.restore_user()

    return block


def get(uid: str, language: str = None) -> _model.Block:
    """Load a block entity from the database
    """
    if not language:
        language = _lang.get_current()

    if language not in _lang.langs():
        raise ValueError("Language '{}' is not defined".format(language))

    block = _content.find('content_block', language=language).eq('block_uid', uid).first()

    if not block:
        raise _error.BlockDataNotFound("Block '{}' for language '{}' is not found in database".format(uid, language))

    return block


def get_defined() -> dict:
    """Get all defined blocks
    """
    return _BLOCKS
