"""PytSite Content Block Plugin API.
"""
from pytsite import lang as _lang, auth as _auth
from plugins import content as _content
from . import _model, _error

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

_blocks = []


def is_defined(uid: str, language: str = 'n') -> bool:
    """Check whether block is defined.
    """
    return (uid, language) in _blocks


def define(uid: str, title: str, language: str = 'n', content_type: str = 'html') -> _model.Block:
    """Define block.
    """
    if is_defined(uid, language):
        raise _error.BlockAlreadyDefined("Block '{}' for language '{}' is already defined".format(uid, language))

    if content_type not in ('text', 'html'):
        raise ValueError('Invalid content type: {}'.format(content_type))

    _blocks.append((uid, language))

    try:
        block = get(uid, language)
    except _error.BlockNotFound:
        _auth.switch_user_to_system()
        block = _content.dispense('content_block')
        block.f_set('uid', uid).f_set('language', language).f_set('title', title).save()
        _auth.restore_user()

    return block


def get(uid: str, language: str = None) -> _model.Block:
    """Get block.
    """
    language = language or _lang.get_current()
    f = _content.find('content_block', language='*').inc('language', (language, 'n')).eq('uid', uid)
    block = f.first()
    if not block:
        raise _error.BlockNotFound("Block '{}' for language '{}' is not found".format(uid, language))

    return block


def get_all() -> list:
    """Get all defined blocks.
    """
    return _blocks.copy()
