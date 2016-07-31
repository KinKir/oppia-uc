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


class InteractiveMap(base.BaseInteraction):
    """Interaction for pinpointing a location on a map."""

    name = '世界地图'
    description = '允许学生在地图上指定点作为答案'
    display_mode = base.DISPLAY_MODE_SUPPLEMENTAL
    is_trainable = False
    _dependency_ids = ['google_maps']
    answer_type = 'CoordTwoDim'
    instructions = '点击地图'
    narrow_instructions = '查看地图'
    needs_summary = True

    _customization_arg_specs = [{
        'name': 'latitude',
        'description': '显示纬度范围 (-90 to 90)',
        'schema': {
            'type': 'float',
            'validators': [{
                'id': 'is_at_least',
                'min_value': -90.0,
            }, {
                'id': 'is_at_most',
                'max_value': 90.0,
            }]
        },
        'default_value': 0.0,
    }, {
        'name': 'longitude',
        'description': '显示经度范围 (-180 to 180)',
        'schema': {
            'type': 'float',
            'validators': [{
                'id': 'is_at_least',
                'min_value': -180.0,
            }, {
                'id': 'is_at_most',
                'max_value': 180.0,
            }]
        },
        'default_value': 0.0,
    }, {
        'name': 'zoom',
        'description': '缩放级别 (0 显示世界地图)',
        'schema': {
            'type': 'float',
        },
        'default_value': 0.0,
    }]
