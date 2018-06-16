"""PytSite Content Block Plugin Models
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from frozendict import frozendict as _frozendict
from plugins import widget as _widget, odm as _odm, content as _content, odm_ui as _odm_ui, form as _form


class Block(_content.model.Content):
    """Content Block ODM Model
    """

    def _setup_fields(self):
        """Hook
        """
        super()._setup_fields()

        self.get_field('body').tidyfy_html = False

        self.remove_field('description')
        self.remove_field('author')
        self.remove_field('status')
        self.remove_field('publish_time')

        self.define_field(_odm.field.Bool('enabled', default=True))
        self.define_field(_odm.field.String('block_uid', required=True))
        self.define_field(_odm.field.String('content_type', required=True, default='wysiwyg'))

    def _setup_indexes(self):
        """Hook
        """
        super()._setup_indexes()

        self.define_index([('block_uid', _odm.I_ASC), ('language', _odm.I_ASC)], True)

    @property
    def enabled(self) -> bool:
        return self.f_get('enabled')

    @enabled.setter
    def enabled(self, value: bool):
        self.f_set('enabled', value)

    @property
    def block_uid(self) -> str:
        return self.f_get('block_uid')

    @block_uid.setter
    def block_uid(self, value: str):
        self.f_set('block_uid', value)

    @property
    def content_type(self) -> str:
        return self.f_get('content_type')

    @content_type.setter
    def content_type(self, value: str):
        self.f_set('content_type', value)

    @property
    def data(self) -> _frozendict:
        return self.f_get('data')

    @data.setter
    def data(self, value: str):
        self.f_set('data', value)

    @classmethod
    def odm_auth_permissions_group(cls) -> str:
        """Get model permission group name
        """
        return 'content_block'

    @classmethod
    def odm_auth_permissions(cls) -> tuple:
        """Hook
        """
        return 'modify',

    @classmethod
    def odm_ui_creation_allowed(cls) -> bool:
        """Hook
        """
        # Users cannot create blocks via UI
        return False

    @classmethod
    def odm_ui_browser_setup(cls, browser: _odm_ui.Browser):
        def finder_adjust(f: _odm.Finder):
            from . import _api
            f.inc('block_uid', [b[0] for b in _api.get_defined()])  # Select only defined blocks

        super().odm_ui_browser_setup(browser)
        browser.finder_adjust = finder_adjust

        browser.data_fields = [
            ('block_uid', 'content_block@uid'),
            ('title', 'content_block@title'),
            ('enabled', 'content_block@enabled'),
        ]

    def odm_ui_browser_row(self) -> dict:
        """Hook
        """
        if self.enabled:
            enabled = '<span class="label label-primary">{}</span>'.format(self.t('word_yes'))
        else:
            enabled = '<span class="label label-default">{}</span>'.format(self.t('word_no'))

        return {
            'block_uid': self.block_uid,
            'title': self.title,
            'enabled': enabled,
        }

    def odm_ui_m_form_setup_widgets(self, frm: _form.Form):
        """Hook
        """
        super().odm_ui_m_form_setup_widgets(frm)

        frm.add_widget(_widget.select.Checkbox(
            uid='enabled',
            weight=5,
            label=self.t('enabled'),
            value=self.enabled,
        ))

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
