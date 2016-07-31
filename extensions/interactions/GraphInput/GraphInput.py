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


class GraphInput(base.BaseInteraction):
    """Interaction for evaluating graphs."""

    name = '几何图形'
    description = '允许创建多种几何图形'
    display_mode = base.DISPLAY_MODE_SUPPLEMENTAL
    is_trainable = False
    _dependency_ids = []
    answer_type = 'Graph'
    instructions = '创建几何图形'
    narrow_instructions = 'View graph'
    needs_summary = True

    _customization_arg_specs = [{
        'name': 'graph',
        'description': '初始图形',
        'schema': {
            'type': 'custom',
            'obj_type': 'Graph',
        },
        'default_value': {
            'vertices': [{
                'x': 150.0,
                'y': 50.0,
                'label': '',
            }, {
                'x': 200.0,
                'y': 50.0,
                'label': '',
            }, {
                'x': 150.0,
                'y': 100.0,
                'label': '',
            }],
            'edges': [{
                'src': 0,
                'dst': 1,
                'weight': 1,
            }, {
                'src': 1,
                'dst': 2,
                'weight': 1,
            }],
            'isLabeled': False,
            'isDirected': False,
            'isWeighted': False,
        }
    }, {
        'name': 'canAddVertex',
        'description': '允许添加点',
        'schema': {
            'type': 'bool',
        },
        'default_value': False
    }, {
        'name': 'canDeleteVertex',
        'description': '允许删除点',
        'schema': {
            'type': 'bool',
        },
        'default_value': False
    }, {
        'name': 'canMoveVertex',
        'description': '允许移动点',
        'schema': {
            'type': 'bool',
        },
        'default_value': True
    }, {
        'name': 'canEditVertexLabel',
        'description': '允许编辑节点标签',
        'schema': {
            'type': 'bool',
        },
        'default_value': False
    }, {
        'name': 'canAddEdge',
        'description': '允许添加线',
        'schema': {
            'type': 'bool',
        },
        'default_value': True
    }, {
        'name': 'canDeleteEdge',
        'description': '允许删除线',
        'schema': {
            'type': 'bool',
        },
        'default_value': True
    }, {
        'name': 'canEditEdgeWeight',
        'description': '允许编辑线权重',
        'schema': {
            'type': 'bool',
        },
        'default_value': False
    }]
