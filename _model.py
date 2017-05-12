"""PytSite Content Block Plugin Models.
"""
from typing import Union as _Union
from bson.objectid import ObjectId as _ObjectId
from pytsite import odm as _odm, form as _form, widget as _widget, odm_ui as _odm_ui, lang as _lang
from plugins import content as _content

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class Block(_content.model.Content):
    def __init__(self, model: str, obj_id: _Union[str, _ObjectId] = None):
        """Init.
        """
        super().__init__(model, obj_id)

        self._content_type = 'text'

    def _setup_fields(self):
        """Hook.
        """
        super()._setup_fields()

        self.get_field('body').tidyfy_html = False

        self.remove_field('description')
        self.remove_field('author')
        self.remove_field('status')

        self.define_field(_odm.field.String('block_uid', required=True))

    def _setup_indexes(self):
        super()._setup_indexes()

        self.define_index([('block_uid', _odm.I_ASC), ('language', _odm.I_ASC)], True)

    @property
    def block_uid(self) -> str:
        return self.f_get('block_uid')

    @property
    def content_type(self) -> str:
        return self._content_type

    @content_type.setter
    def content_type(self, value: str):
        self._content_type = value

    @classmethod
    def odm_auth_permissions(cls) -> tuple:
        return 'create', 'modify'

    @classmethod
    def odm_ui_creation_allowed(cls) -> bool:
        """Hook.
        """
        return False

    @classmethod
    def odm_ui_browser_setup(cls, browser: _odm_ui.Browser):
        def finder_adjust(f: _odm.Finder):
            from . import _api
            f.inc('language', (_lang.get_current(), 'n'))
            f.inc('block_uid', [b[0] for b in _api.get_blocks()])  # Select only defined blocks

        _content.model.Content.odm_ui_browser_setup(browser)
        browser.finder_adjust = finder_adjust

        browser.data_fields = [
            ('block_uid', 'content_block@uid'),
            ('title', 'content_block@title'),
        ]

    def odm_ui_browser_row(self) -> tuple:
        return self.block_uid, _lang.t(self.title) if '@' in self.title else self.title

    def odm_ui_m_form_setup_widgets(self, frm: _form.Form):
        """Hook.
        """
        super().odm_ui_m_form_setup_widgets(frm)

        # ID
        frm.add_widget(_widget.input.Text(
            uid='block_uid',
            weight=50,
            label=self.t('uid'),
            value=self.block_uid,
            required=True,
            enabled=False,
        ))

        # Text blocks
        if self.content_type == 'text':
            frm.remove_widget('images')
            frm.remove_widget('video_links')

            frm.replace_widget('body', _widget.input.TextArea(
                uid='body',
                label=self.t('body'),
                value=self.body,
                rows=15,
            ))
