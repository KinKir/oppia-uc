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
import utils


class VideoCategory(base_models.BaseModel):

    def __init__(selCf):
        pass

    name = ndb.StringProperty(required=True)
    category = ndb.StringProperty(required=True)
    author_id = ndb.StringProperty(indexed=True)

    @classmethod
    def get_by_author(cls, author_id, page_size, urlsafe_start_cursor):
        return cls._fetch_page_sorted_by_last_updated(
            cls.query.filter(cls.author_id == author_id),
            page_size, urlsafe_start_cursor)

    @classmethod
    def get_all(cls, page_size, urlsafe_start_cursor):
        return cls._fetch_page_sorted_by_last_updated(
            cls.query(), page_size, urlsafe_start_cursor
        )

    def to_dict(self):
        return {
            'id': self.id,
            'last_updated': utils.get_time_in_millisecs(self.last_updated),
            'original_author_username':
                self.get_author_name() if self.author_id else None,
            'name': self.name,
            'category': self.category,
            'thumbnail_icon_url': utils.get_thumbnail_icon_url_for_category(self.category),
            'thumbnail_bg_color': utils.get_hex_color_for_category(self.category),
            'ids': self.ids,
            'created_on': utils.get_time_in_millisecs(self.created_on)
        }


class VideoList(base_models.BaseModel):
    # 视频名称
    name = ndb.StringProperty(required=True)
    # 视频编号
    ids = ndb.StringProperty(required=True)

    # 分类
    category = ndb.StringProperty(required=True)
    # 作者，上传人
    author_id = ndb.StringProperty(indexed=True)

    @classmethod
    def get_video_count(cls):
        """Returns the total number of explorations."""
        return cls.get_all().count()

    @classmethod
    def get_by_author(cls, author_id, page_size, urlsafe_start_cursor):
        return cls._fetch_page_sorted_by_last_updated(
            cls.query().filter(cls.author_id == author_id),
            page_size, urlsafe_start_cursor)

    @classmethod
    def get_all_video(cls, page_size, urlsafe_start_cursor):
        return cls._fetch_page_sorted_by_last_updated(
            cls.query(), page_size, urlsafe_start_cursor)
