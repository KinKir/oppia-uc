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
 * @fileoverview Data and controllers for the user's private log dashboard.
 */
oppia.controller('PrivateLogs', [
  '$scope', '$http', '$modal', '$rootScope', 'oppiaDatetimeFormatter',
  'privateLogDataService',
  function($scope, $http, $modal, $rootScope, oppiaDatetimeFormatter,
           privateLogDataService) {
    $scope.navigateToItem = function(activityId, notificationType) {
      window.location.href = '/create/' + activityId + (
          notificationType === 'feedback_thread' ? '#/feedback' : '');
    };

    $scope.navigateToProfile = function($event, username) {
      $event.stopPropagation();
      window.location.href = '/profile/' + username;
    };
    $scope.showPrivateLogModel = function(logid) {
      privateLogDataService.getPrivateLog(logid, function(data) {
        $modal.open({
          templateUrl: 'modals/editorPrivateLogCreate',
          backdrop: true,
          resolve: {},
          controller: ['$scope', '$modalInstance',
            function($scope, $modalInstance) {
              $scope.schema = {
                type: 'html'
              };
              $scope.contentEditorIsOpen = false;
              $scope.saveTextContent = function() {
                $scope.contentEditorIsOpen = false;
              };
              $scope.openStateContentEditor = function() {
                $scope.contentEditorIsOpen = true;
              };
              $scope.onSaveContentButtonClicked = function(content) {
                $scope.saveTextContent();
                $scope.newLogContent = content;
                // Show the interaction when the text content is saved, even if no content
                // is entered.
                //$scope.isInteractionShown = true;
              };
              $scope.newLogTitle = data.title;
              $scope.newCategory = data.category_name;
              $scope.newLogContent = data.content;
              $scope.save = function(newLogTitle, newCategory,
                                     newLogContent) {
                $modalInstance.close({
                  logid: logid,
                  newLogTitle: newLogTitle,
                  newLogContent: newLogContent,
                  newCategory: newCategory
                });
              };
              $scope.cancel = function() {
                $modalInstance.dismiss('cancel');
              };
            }]
        }).result.then(function(result) {
          privateLogDataService.Save(result.logid, result.newLogTitle,
            result.newCategory, result.newLogContent, $scope.loadData);
        });
      });
    };
    $scope.getLocaleAbbreviatedDatetimeString = function(millisSinceEpoch) {
      return oppiaDatetimeFormatter.getLocaleAbbreviatedDatetimeString(
        millisSinceEpoch);
    };
    $scope.showCreateLogModal = function() {
      $modal.open({
        templateUrl: 'modals/editorPrivateLogCreate',
        backdrop: true,
        resolve: {},
        transclude: true,
        replace: true,
        controller: ['$scope', '$modalInstance',
          function($scope, $modalInstance) {
            $scope.schema = {
              type: 'html'
            };
            $scope.contentEditorIsOpen = false;
            $scope.saveTextContent = function() {
              //$scope.newLogContent = $scope.newLogContent
              $scope.contentEditorIsOpen = false;
            };
            $scope.openStateContentEditor = function() {
              $scope.contentEditorIsOpen = true;
            };

            $scope.onSaveContentButtonClicked = function(content) {
              $scope.saveTextContent();
              $scope.newLogContent = content;
              // Show the interaction when the text content is saved, even if no content
              // is entered.
              //$scope.isInteractionShown = true;
            };
            $scope.cancelEdit = function() {
              // $scope.content = explorationStatesService.getStateContentMemento(
              //   editorContextService.getActiveStateName());
              $scope.contentEditorIsOpen = false;
            };
            $scope.save = function(newLogTitle, newCategory, newLogContent) {
              $modalInstance.close({
                newLogTitle: newLogTitle,
                newLogContent: newLogContent,
                newCategory: newCategory
              });
            };
            $scope.cancel = function() {
              $modalInstance.dismiss('cancel');
            };
          }]
      }).result.then(function(result) {
        privateLogDataService.createNewLog(result.newLogTitle,
          result.newCategory, result.newLogContent, $scope.loadData);
      });
    };
    $scope.loadData = function() {
      $rootScope.loadingMessage = '加载中...';
      $http.get('/privatelog/data').then(function(response) {
        var data = response.data;
        $scope.logs = data.logs;
        $scope.jobQueuedMsec = data.job_queued_msec;
        $scope.lastSeenMsec = data.last_seen_msec || 0.0;
        $scope.currentUsername = data.username;
        $rootScope.loadingMessage = '';
      });
    };
    $scope.loadData();
  }]);
