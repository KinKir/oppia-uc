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

"""Commands for private log operations."""

# import datetime

from core.domain import privatelog_domain
# from core.domain import rights_manager
# from core.domain import user_services
from core.platform import models

# import feconf

(privatelog_models,) = models.Registry.import_models([models.NAMES.privatelog])


def create_private_log(author_id, category_id, title, content):
    """Creates a thread and the first message in it.
    """

    log = privatelog_models.PrivateLogModel()
    log.title = title
    log.category_id = category_id
    log.category_name = privatelog_models.LogCategoryModel \
        .get(category_id).category_name
    log.content = content
    log.author_id = author_id
    log.put()


def try_create_category(author_id, category_name):
    """Creates category
    """
    if not privatelog_models.LogCategoryModel.check_exist(
            author_id, category_name):
        category = privatelog_models.LogCategoryModel()
        category.category_name = category_name
        category.author_id = author_id
        category.put()
        return category
    else:
        return get_category_by_name(author_id, category_name)


def get_privatelog(log_id):
    return _get_privatelog_from_model(
        privatelog_models.PrivateLogModel.get(long(log_id)))


def get_privatelog_model(log_id):
    return privatelog_models.PrivateLogModel.get(long(log_id))


def get_category_by_name(author_id, category_name):
    return privatelog_models.LogCategoryModel.get_category_by_name(
        author_id, category_name)


def _get_privatelog_from_model(privatelog_model):
    category_name = privatelog_models.LogCategoryModel \
        .get(privatelog_model.category_id).category_name
    return privatelog_domain \
        .PrivateLog(privatelog_model.id,
                    privatelog_model.author_id,
                    privatelog_model.title,
                    privatelog_model.content,
                    privatelog_model.category_id, category_name,
                    privatelog_model.created_on,
                    privatelog_model.last_updated)


def get_all_privatelog(author_id):
    logs = privatelog_models.PrivateLogModel.get_by_author(author_id)
    return [_get_privatelog_from_model(model) for model in logs]
