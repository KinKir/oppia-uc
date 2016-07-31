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

from extensions.interactions import base


class CodeRepl(base.BaseInteraction):
    """Interaction that allows programs to be input."""

    name = '编码器'
    description = '学生输入可以执行的代码'
    display_mode = base.DISPLAY_MODE_SUPPLEMENTAL
    is_trainable = False
    _dependency_ids = ['skulpt', 'codemirror']
    answer_type = 'CodeEvaluation'
    instructions = '在编辑器中输入代码'
    narrow_instructions = '输入编码'
    needs_summary = True

    # Language options 'lua', 'scheme', 'coffeescript', 'javascript', and
    # 'ruby' have been removed for possible later re-release.
    _customization_arg_specs = [{
        'name': 'language',
        'description': '代码语言',
        'schema': {
            'type': 'unicode',
            'choices': [
                'python',
            ]
        },
        'default_value': 'python'
    }, {
        'name': 'placeholder',
        'description': '初始代码',
        'schema': {
            'type': 'unicode',
            'ui_config': {
                'coding_mode': 'none',
            },
        },
        'default_value': '# 在这里输入你的代码.'
    }, {
        'name': 'preCode',
        'description': '添加到学生输入代码之前的代码',
        'schema': {
            'type': 'unicode',
            'ui_config': {
                'coding_mode': 'none',
            },
        },
        'default_value': ''
    }, {
        'name': 'postCode',
        'description': '添加到学生输入代码之后的代码',
        'schema': {
            'type': 'unicode',
            'ui_config': {
                'coding_mode': 'none',
            },
        },
        'default_value': ''
    }]
