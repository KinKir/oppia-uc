// Copyright 2015 The Oppia Authors. All Rights Reserved.
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
 * @fileoverview Translation functions for Oppia.
 *
 * @author milagro.teruel@gmail.com (Milagro Teruel)
 */

// Translations of strings that are loaded in the front page. They are listed

oppia.controller('VideoList', ['$scope', '$modal', '$rootScope', '$window',
  'oppiaDatetimeFormatter', 'alertsService', 'FATAL_ERROR_CODES',
  'videoListService',
  function($scope, $modal, $rootScope, $window,
           oppiaDatetimeFormatter, alertsService,
           FATAL_ERROR_CODES, videoListService) {
    $scope.loadData = function() {
      videoListService.getVideoList($scope);
    };
    $scope.loadData();
    $scope.showCreateModal = function() {
      $modal.open({
        templateUrl: 'modals/editorVideoCreate',
        backdrop: true,
        resolve: {},
        controller: ['$scope', '$modalInstance',
          function($scope, $modalInstance) {
            $scope.schema = {
              type: 'html'
            };
            $scope.create = function(name, ids,
                                     category) {
              $modalInstance.close({
                name: name,
                ids: ids,
                category: category
              });
            };
            $scope.cancel = function() {
              $modalInstance.dismiss('cancel');
            };
          }]
      }).result.then(function(result) {
        videoListService.createVideo(result.name, result.ids, result.category);
      });
    };
  }]);
