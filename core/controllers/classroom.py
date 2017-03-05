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
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS-IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Controllers for the classroom page."""

import jinja2

from core.controllers import base
from core.controllers import editor
from core.domain import config_domain
from core.domain import gadget_registry
from core.domain import rte_component_registry
from core.domain import classroom_domain
from core.storage.classroom import gae_models as classroom_models
import feconf


class ClassroomPage(base.BaseHandler):
    PAGE_NAME_FOR_CSRF = "editor"
    EDITOR_PAGE_DEPENDENCY_IDS = []

    def get(self):
        if self.username in config_domain.BANNED_USERNAMES.value:
            raise self.UnauthorizedUserException("用户被禁止访问")
        else:

            interaction_templates = (
                rte_component_registry.Registry.get_html_for_all_components())

            gadget_types = gadget_registry.Registry.get_all_gadget_types()
            gadget_templates = (
                gadget_registry.Registry.get_gadget_html(gadget_types))

            self.values.update({
                'meta_description': feconf.SPLASH_PAGE_DESCRIPTION,
                'nav_mode': 'video',
                'value_generators_js': jinja2.utils.Markup(
                    editor.get_value_generators_js()),
                'gadget_templates': jinja2.utils.Markup(gadget_templates),
                'interaction_templates': jinja2.utils.Markup(
                    interaction_templates)
            })
            self.render_template(
                'classroom/classroom.html')


class ClassroomHandler(base.BaseHandler):
    PAGE_NAME_FOR_CSRF = "editor"

    def get(self, classroom_id):
        if classroom_id is not None and classroom_id != '0':
            cls_room = classroom_models.Classroom.get(
                long(classroom_id), False)
            if cls_room is None:
                raise self.PageNotFoundException
            m = cls_room
            self.values.update(classroom_domain.Classroom(
                m.id, m.name, m.building, m.location,
                m.day_of_week, m.sections, m.seat_count, m.author_id,
                m.last_updated
            ).to_dict())
            self.render_json(self.values)

        else:
            urlsafe_start_cursor = self.request.get('cursor')
            lists, new_urlsafe_start_cursor, more = \
                classroom_models.Classroom.get_all(page_size=20,
                                                   urlsafe_start_cursor=urlsafe_start_cursor)
            self.values.update({
                'results': [classroom_domain.Classroom(
                    m.id, m.name, m.building, m.location,
                    m.day_of_week, m.sections, m.seat_count, m.author_id,
                    m.last_updated
                ).to_dict() for m in lists],
                'cursor': new_urlsafe_start_cursor,
                'more': more,
            })
            self.render_json(self.values)

    def post(self, classroom_id):
        if classroom_id is not None and classroom_id != '0':
            cls_room = classroom_models.Classroom.get(long(classroom_id))
        else:
            cls_room = classroom_models.Classroom()
            cls_room.author_id = self.user_id

        cls_room.name = self.payload.get('name')
        cls_room.building = self.payload.get('building')
        cls_room.sections = ','.join([unicode(i) for i in self.payload.get('sections')])
        cls_room.day_of_week = int(self.payload.get('day_of_week'))
        cls_room.seat_count = int(self.payload.get('seat_count'))
        cls_room.location = self.payload.get('location')
        cls_room.put()
        self.render_json(self.values)

    def delete(self, classroom_id):
        if classroom_id is not None and classroom_id != '0':
            cls_room = classroom_models.Classroom.get(
                long(classroom_id), False)
            if cls_room is None:
                raise self.PageNotFoundException
            else:
                cls_room.delete()
