# coding: utf-8
#
# Copyright 2014 The Oppia Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, softwar
# distributed under the License is distributed on an "AS-IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from extensions.rich_text_components import base


TAB_CONTENT_SCHEMA = {
    'type': 'dict',
    'properties': [{
        'name': 'title',
        'description': '标签标题',
        'schema': {
            'type': 'unicode',
            'validators': [{
                'id': 'is_nonempty'
            }]
        }
    }, {
        'name': 'content',
        'description': '标签内容',
        'schema': {
            'type': 'html',
            'ui_config': {
                'hide_complex_extensions': True,
            }

        }
    }]
}


class Tabs(base.BaseRichTextComponent):
    """A rich-text component representing a series of tabs."""

    name = 'Tabs'
    category = 'Basic Input'
    description = '标签页面.'
    frontend_name = 'tabs'
    tooltip = '插入标签页面'
    is_complex = True
    is_block_element = True

    _customization_arg_specs = [{
        'name': 'tab_contents',
        'description': '标签名称和内容.',
        'schema': {
            'type': 'list',
            'items': TAB_CONTENT_SCHEMA,
            'ui_config': {
                'add_element_text': '添加'
            }
        },
        'default_value': [{
            'title': '标签1',
            'content': ('第一个标签内容 '
                        '点击标签显示响应的内容.')
        }, {
            'title': '标签 2',
            'content': '第二个标签内容.'
        }],
    }]
