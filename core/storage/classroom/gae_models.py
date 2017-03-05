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

"""Model for an Oppia classroom."""

# import datetime

import core.storage.base_model.gae_models as base_models
# import core.storage.user.gae_models as user_models
# import feconf

from google.appengine.ext import ndb


class Classroom(base_models.BaseModel):
    # 教室名称
    name = ndb.StringProperty(required=True)

    building = ndb.StringProperty(required=True)

    # 位置
    location = ndb.StringProperty(required=True)

    # 一周中的第几天
    day_of_week = ndb.IntegerProperty(required=True, choices=[
        1, 2, 3, 4, 5, 6, 7])

    # 闲置时间，用数字表示，一天1-12节，用‘,’隔开
    sections = ndb.StringProperty(required=True)

    # 座位数量
    seat_count = ndb.IntegerProperty(required=True)

    # 设置人
    author_id = ndb.StringProperty(required=True)

    @classmethod
    def get_by_author(cls, author_id, page_size, urlsafe_start_cursor):
        return cls._fetch_page_sorted_by_last_updated(
            cls.query().filter(cls.author_id == author_id),
            page_size, urlsafe_start_cursor)

    @classmethod
    def get_all(cls, page_size, urlsafe_start_cursor):
        return cls._fetch_page_sorted_by_last_updated(
            cls.query(), page_size, urlsafe_start_cursor)
