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


class Link(base.BaseRichTextComponent):
    """A rich-text component for displaying links."""

    name = 'Link'
    category = 'Basic Input'
    description = 'A link to a URL.'
    frontend_name = 'link'
    tooltip = 'Insert link'

    _customization_arg_specs = [{
        'name': 'url',
        'description': (
            '链接网址。如果没有指定协议，HTTPS将使用.'),
        'schema': {
            'type': 'custom',
            'obj_type': 'SanitizedUrl',
        },
        'default_value': 'https://www.example.com',
    }, {
        'name': 'text',
        'description': (
            '链接文本。如果留空，会使用链接URL作为链接文本.'),
        'schema': {
            'type': 'unicode',
        },
        'default_value': '',
    }, {
        'name': 'open_link_in_same_window',
        'description': '打开在同一个窗口中的链接?',
        'schema': {
            'type': 'bool'
        },
        'default_value': False,
    }]
