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

"""Domain objects for feedback models"""

from core.domain import user_services
import utils


class PrivateLog(object):
    """Domain object for a private log."""

    def get_author_name(self):
        return user_services.get_username(self.author_id)

    def __init__(self, author_id, title, content, category_id,
                 created_on, last_updated):

        self.author_id = author_id
        self.content = content
        self.title = title
        self.category_id = category_id

        self.created_on = created_on
        self.last_updated = last_updated

    def to_dict(self):
        return {
            'last_updated': utils.get_time_in_millisecs(self.last_updated),
            'original_author_username': user_services.get_username(
                self.author_id) if self.author_id else None,
            'title': self.title,
            'category_id': self.category_id,
            'category_name': self.subject,
            'created_on': self.created_on
        }
