# coding: utf-8
#
# Copyright 2016 The Oppia Authors. All Rights Reserved.
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

"""Demain for the videioList page."""

from core.domain import user_services
import utils


class VideoList(object):
    """Domain object for a video"""

    def get_author_name(self):
        return user_services.get_username(self.author_id)

    def __init__(self, mid, name, ids, category, author_id,
                 created_on, last_updated):
        self.author_id = author_id
        self.name = name
        self.ids = ids
        self.category = category
        self.created_on = created_on
        self.last_updated = last_updated
        self.id = mid

    def to_dict(self):
        return {
            'id': self.id,
            'last_updated': utils.get_time_in_millisecs(self.last_updated),
            'original_author_username':
                self.get_author_name() if self.author_id else None,
            'name': self.name,
            'category': self.category,
            'ids': self.ids,
            'created_on': utils.get_time_in_millisecs(self.created_on)
        }
