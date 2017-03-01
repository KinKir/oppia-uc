// Copyright 2015 The Oppia Authors. All Rights Reserved.
//
// Licensed under the Apache License, Version 2.0 (the "License");
// You may not use this file except in compliance with the License.
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
 * @fileoverview Translation functions for Oppia.
 *
 * @author milagro.teruel@gmail.com (Milagro Teruel)
 */

// Translations of strings that are loaded in the front page. They are listed
oppia.factory('videoListService', ['$http',
  function($http) {
    var _VIDEO_LIST_DATA_HANLDER_URL = '/video/data/' + categoryId + '/';
    return {
      getVideoList: function() {
        return $http.get(_VIDEO_LIST_DATA_HANLDER_URL + '0');
      },
      createVideo: function(name, ids, category) {
        return $http.post(_VIDEO_LIST_DATA_HANLDER_URL + '0', {
          name: name,
          ids: ids,
          category: category
        });
      },
      saveEditVideo: function(id, name, ids, category) {
        return $http.post(_VIDEO_LIST_DATA_HANLDER_URL + id, {
          id: id,
          name: name,
          ids: ids,
          category: category
        });
      },
      getVideo: function(id, $scope) {
        $http.get(_VIDEO_LIST_DATA_HANLDER_URL + id).then(function(response) {
          var data = response.data;
          $scope.name = data.name;
          $scope.id = data.id;
          $scope.ids = data.ids;
          $scope.create_on = data.create_on;
          $scope.category = data.category;
        });
      },
      deleteData: function(id) {
        return $http.delete(_VIDEO_LIST_DATA_HANLDER_URL + id);
      }
    };
  }]);
