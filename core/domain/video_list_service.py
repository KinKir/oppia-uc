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

"""Commands for video list operations."""

from core.domain import video_list_demain
# from core.platform import models
from core.storage.video_list import gae_models as video_list_models
import feconf


def create_video(author_id, name, category, mid):
    """
    创建一个视频
    :param author_id:创建人id
    :param name:视频名称
    :param category:分类
    :param mid:对应的地址
    :return:None
    """

    video = video_list_models.VideoList()
    video.name = name
    video.category = category
    video.author_id = author_id
    video.ids = mid
    video.put()


def _get_video_from_model(model):
    return video_list_demain \
        .VideoList(model.id,
                   model.name,
                   model.ids,
                   model.category,
                   model.author_id,
                   model.created_on,
                   model.last_updated
                  )


def get_all_video(page_size=feconf.FEEDBACK_TAB_PAGE_SIZE,
                  urlsafe_start_cursor=None):
    results, new_urlsafe_start_cursor, more = \
        video_list_models.VideoList.get_all_video(page_size,
                                                  urlsafe_start_cursor)
    return [_get_video_from_model(model)
            for model in results], \
           new_urlsafe_start_cursor, more


def get_by_id(vid):
    return _get_video_from_model(
        video_list_models.VideoList.get(long(vid)))


def delete_video(vid):
    video_list_models.VideoList.get(long(vid)).delete()
