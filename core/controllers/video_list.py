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

"""Controllers for the videioList page."""

from core.controllers import base
# from core.domain import user_services
# from core.domain import config_domain
from core.domain import video_list_service
import feconf
# import utils


class VedioListHandler(base.BaseHandler):
    """处理视频列表"""
    PAGE_NAME_FOR_CSRF = "editor"

    def get(self):
        self.render_json(self.values)


class VideoListPage(base.BaseHandler):
    def get(self):
        self.values.update({
            'meta_description': feconf.SPLASH_PAGE_DESCRIPTION,
            'nav_mode': 'video',
        })
        self.render_template(
            'video_list/video_list.html')


class VideoListData(base.BaseHandler):
    """视频数据处理"""
    def get(self, video_id):
        if video_id is not None and video_id != '0':
            video = video_list_service.get_by_id(video_id)
            self.values.update(video.to_dict())
            self.render_json(self.values)
        else:
            urlsafe_start_cursor = self.request.get('cursor')
            lists, new_urlsafe_start_cursor, more = \
                video_list_service.get_all_video(
                    urlsafe_start_cursor=urlsafe_start_cursor)
            self.render_json({
                'results': [m.to_dict() for m in lists],
                'cursor': new_urlsafe_start_cursor,
                'more': more,
            })

    def delete(self, video_id):
        """删除视频"""
        video_list_service.delete_video(video_id)
