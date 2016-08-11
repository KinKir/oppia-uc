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

"""Models relating to the per-exploration file system."""

from core.platform import models
import feconf
# import utils

from google.appengine.ext import ndb

(base_models,) = models.Registry.import_models([models.NAMES.base_model])


class LogCategoryModel(base_models.BaseModel):
    """Log category data model"""
    author_id = ndb.StringProperty(indexed=True)
    category_name = ndb.StringProperty(indexed=True)

    @classmethod
    def get_by_author(cls, author_id):
        return cls.get_all().filter(
            cls.author_id == author_id).order(
                cls.category_name).fetch(
                    feconf.DEFAULT_QUERY_LIMIT)

    @classmethod
    def check_exist(cls, author_id, name):
        return cls.get_category_by_name(author_id, name) is not None

    @classmethod
    def get_category_by_name(cls, author_id, name):
        return cls.get_all().filter(
            ndb.AND(cls.author_id == author_id,
                    cls.category_name == name)).get()


class PrivateLogModel(base_models.BaseModel):
    """Private log data model."""

    # The contents of the log.
    content = ndb.TextProperty(indexed=False)
    # ID of the user who posted this log.
    author_id = ndb.StringProperty(indexed=True)
    # log category
    category_name = ndb.StringProperty(indexed=True)

    category_id = ndb.IntegerProperty(indexed=True)

    title = ndb.StringProperty(indexed=True)

    @classmethod
    def get_by_author(cls, author_id):
        return cls.get_all().filter(
            cls.author_id == author_id).order(
                -cls.last_updated).fetch(feconf.DEFAULT_QUERY_LIMIT)

    @classmethod
    def get_by_author_and_category(cls, author, categoryid):
        return cls.get_all().filter(
            ndb.AND(
                cls.author_id == author,
                cls.category_id == categoryid)).order(
                    -cls.last_updated).fetch(
                        feconf.DEFAULT_QUERY_LIMIT)

    @classmethod
    def get_by_author_filter_title(cls, author, filtertitle):
        return cls.get_all().filter(
            ndb.AND(
                cls.author_id == author,
                cls.title.find(filtertitle) != -1)).order(
                    -cls.last_updated).fetch(feconf.DEFAULT_QUERY_LIMIT)

    @classmethod
    def get_all_log_by_author(cls, author_id, page_size, urlsafe_start_cursor):
        return cls._fetch_page_sorted_by_last_updated(
            cls.query(PrivateLogModel.author_id == author_id),
            page_size, urlsafe_start_cursor
        )
