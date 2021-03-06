// Copyright 2014 The Oppia Authors. All Rights Reserved.
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//      http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS-IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

/**
 * Created by hcz on 16-8-8.
 */
oppia.factory('privateLogDataService', [
  '$http', '$q', 'alertsService',
  function($http, $q, alertsService) {
    var _PRIVATELOG_HANDLER_URL = '/privatelog/handler/';
    return {
      createNewLog: function(newTitle, newCategory, newContent, saveSuccess) {
        $http.post(_PRIVATELOG_HANDLER_URL + '0', {
          newTitle: newTitle,
          newCategory: newCategory,
          newContent: newContent
        }).then(function() {
          if (saveSuccess) {
            saveSuccess();
          }
          alertsService.addSuccessMessage('日志发表成功！');
        }, function() {
          alertsService.addWarning('保存日志失败.');
        });
      },
      getPrivateLog: function(logId, loaded) {
        $http.get(_PRIVATELOG_HANDLER_URL + logId).then(function(response) {
          var data = response.data;
          if (loaded) {
            loaded(data);
          }
        });
      },
      Save: function(logid, newTitle, newCategory, newContent, saveSuccess) {
        $http.post(_PRIVATELOG_HANDLER_URL + logid, {
          newTitle: newTitle,
          newCategory: newCategory,
          newContent: newContent
        }).then(function() {
          if (saveSuccess) {
            saveSuccess();
          }
          alertsService.addSuccessMessage('保存成功');
        }, function() {
          alertsService.addWarning('保存日志失败.');
        });
      }
    };
  }]);
