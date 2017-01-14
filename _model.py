"""PytSite Content Block Plugin Models.
"""
from pytsite import odm as _odm, form as _form, widget as _widget, odm_ui as _odm_ui, lang as _lang
from plugins import content as _content

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class Block(_content.model.Content):
    def _setup_fields(self):
        """Hook.
        """
        super()._setup_fields()

        self.define_field(_odm.field.String('uid', required=True))

    def _setup_indexes(self):
        super()._setup_indexes()

        self.define_index([('uid', _odm.I_ASC), ('language', _odm.I_ASC)], True)

    @property
    def uid(self) -> str:
        return self.f_get('uid')

    @classmethod
    def odm_ui_browser_setup(cls, browser: _odm_ui.Browser):
        _content.model.Content.odm_ui_browser_setup(browser)
        browser.data_fields = [
            ('title', 'content_block@title'),
            ('uid', 'content_block@uid'),
            ('author', 'content_block@author')
        ]

    def odm_ui_browser_row(self) -> tuple:
        return self.title, self.uid, self.author.full_name

    def odm_ui_m_form_setup_widgets(self, frm: _form.Form):
        """Hook.
        """
        super().odm_ui_m_form_setup_widgets(frm)

        # ID
        frm.add_widget(_widget.input.Text(
            uid='uid',
            weight=50,
            label=self.t('uid'),
            value=self.uid,
            required=True,
        ))

    def odm_ui_m_form_validate(self, frm: _form.Form):
        from . import _api, _error

        block_uid = frm.get_widget('uid').value

        if self.is_new:
            try:
                _api.get_block(block_uid)
                raise _form.error.ValidationError({
                    'uid': _lang.t('content_block@block_already_exists')
                })
            except _error.BlockNotFound:
                pass
        else:
            existing_uid = self.uid
            new_uid = block_uid

            if new_uid != existing_uid:
                try:
                    _api.get_block(new_uid)
                    raise _form.error.ValidationError({
                        'uid': _lang.t('content_block@block_already_exists')
                    })
                except _error.BlockNotFound:
                    pass
