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


class MusicNotesInput(base.BaseInteraction):
    """Interaction for music notes input."""

    name = '音符输入'
    description = (
        '学生通过拖拽的方式输入音符号')
    display_mode = base.DISPLAY_MODE_SUPPLEMENTAL
    _dependency_ids = ['midijs']
    answer_type = 'MusicPhrase'
    instructions = '拖拽增加或删除音符'
    narrow_instructions = '显示音符'
    needs_summary = True

    _customization_arg_specs = [{
        'name': 'sequenceToGuess',
        'description': '正确的乐谱',
        'schema': {
            'type': 'custom',
            'obj_type': 'MusicPhrase',
        },
        'default_value': [],
    }, {
        'name': 'initialSequence',
        'description': '乐谱开头',
        'schema': {
            'type': 'custom',
            'obj_type': 'MusicPhrase',
        },
        'default_value': [],
    }]
