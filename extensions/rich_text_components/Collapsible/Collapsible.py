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


class Collapsible(base.BaseRichTextComponent):
    """A rich-text component representing a collapsible block."""

    name = '折叠面板'
    category = 'Basic Input'
    description = '折叠面板.'
    frontend_name = 'collapsible'
    tooltip = '插入折叠面板'
    is_complex = True
    is_block_element = True

    _customization_arg_specs = [{
        'name': 'heading',
        'description': '名称',
        'schema': {
            'type': 'unicode',
        },
        'default_value': '名称',
    }, {
        'name': 'content',
        'description': '内容',
        'schema': {
            'type': 'html',
            'ui_config': {
                'hide_complex_extensions': True,
            }
        },
        'default_value': '打开后显示的内容.'
    }]
