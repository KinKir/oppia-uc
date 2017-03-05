# coding: utf-8
#
# Copyright 2015 The Oppia Authors. All Rights Reserved.
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

"""Domain objects for a collection and its constituents.

Domain objects capture domain-specific logic and are agnostic of how the
objects they represent are stored. All methods and properties in this file
should therefore be independent of the specific storage models used.
"""

from core.domain import user_services
import utils


class Classroom(object):
    def __init__(self, id, name, building, location, day_of_week, sections, seat_count,
                 author_id,last_updated):
        self.id = id
        self.name = name
        self.building = building
        self.location = location
        self.day_of_week = day_of_week
        self.sections = sections
        self.seat_count = seat_count
        self.author_id = author_id
        self.last_updated = last_updated

    def get_author_name(self):
        return user_services.get_username(self.author_id)

    def to_dict(self):
        return {
            'author_name': self.get_author_name(),
            'id': self.id,
            'name': self.name,
            'building': self.building,
            'location': self.location,
            'day_of_week': self.day_of_week,
            'seat_count': self.seat_count,
            'sections': self.sections,
            'author_id': self.author_id,
            'last_updated': utils.get_time_in_millisecs(self.last_updated),
        }
