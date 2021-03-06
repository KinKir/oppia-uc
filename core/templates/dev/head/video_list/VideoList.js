// Copyright 2015 The Oppia Authors. All Rights Reserved.
//
// Licensed under the Apache License, Version 2.0 (the 'License');
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//      http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an 'AS-IS' BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

/**
 * @fileoverview Translation functions for Oppia.
 *
 * @author milagro.teruel@gmail.com (Milagro Teruel)
 */

// Translations of strings that are loaded in the front page. They are listed

oppia.controller('VideoList', ['$scope', '$modal', '$mdDialog', '$rootScope', '$window',
  'oppiaDatetimeFormatter', 'alertsService', 'FATAL_ERROR_CODES',
  'videoListService', '$sce',
  function($scope, $modal, $mdDialog, $rootScope, $window,
           oppiaDatetimeFormatter, alertsService,
           FATAL_ERROR_CODES, videoListService, $sce) {
    var _cursor = null;
    $scope.endOfPageIsReached = false;
    $scope.loadData = function() {
      $rootScope.loadingMessage = '加载中';
      videoListService.getVideoList().then(function(response) {
        $scope.videos = response.data.results;
        _cursor = response.data.cursor;
        $scope.endOfPageIsReached = !response.data.more;
        $scope.currentUserIsAdmin = response.data.is_admin;
        $scope.currentUserName = response.data.username;
        $scope.category_objective = $sce.trustAsHtml(response.data.category_objective);
        $rootScope.loadingMessage = '';
      });
    };
    $scope.getLocaleAbbreviatedDatetimeString = function(millisSinceEpoch) {
      return oppiaDatetimeFormatter.getLocaleAbbreviatedDatetimeString(
        millisSinceEpoch);
    };
    $scope.loadData();
    $scope.showMore = function() {
      if (!$rootScope.loadingMessage) {
        videoListService.getVideoMore(_cursor).then(function(response) {
          $scope.videos = $scope.videos.concat(response.data.results);
          _cursor = response.data.cursor;
          $scope.endOfPageIsReached = !response.data.more;
          $scope.currentUserIsAdmin = response.data.is_admin;
          $scope.currentUserName = response.data.username;
          $scope.category_objective = $sce.trustAsHtml(response.data.category_objective);
          $rootScope.loadingMessage = '';
        });
      }
    };
    $scope.showEditModal = function(objid) {
      videoListService.getVideo(objid).then(function(response) {
        $modal.open({
          templateUrl: 'modals/editorVideoCreate',
          backdrop: true,
          resolve: {},
          controller: ['$scope', '$modalInstance', 'CATEGORY_LIST',
            'ALL_CATEGORIES_ZH_MAP',
            function($scope, $modalInstance, CATEGORY_LIST,
                     ALL_CATEGORIES_ZH_MAP) {
              $scope.schema = {
                type: 'html'
              };
              $scope.name = response.data.name;
              $scope.ids = response.data.ids;
              $scope.id = response.data.id;
              $scope.create = function(name, ids) {
                $modalInstance.close({
                  id: $scope.id,
                  name: name,
                  ids: ids,
                  category: categoryId
                });
              };
              $scope.cancel = function() {
                $modalInstance.dismiss('cancel');
              };
            }]
        }).result.then(function(result) {
          $rootScope.loadingMessage = '正在保存';
          videoListService.saveEditVideo(result.id, result.name,
            result.ids,
            result.category).then(function() {
            $rootScope.loadingMessage = '';
            alertsService.addSuccessMessage('保存成功');
            $scope.loadData();
          }, function() {
            $rootScope.loadingMessage = '';
            alertsService.addWarning('保存失败.');
          });
        });
      }, function() {
        $rootScope.loadingMessage = '';
        alertsService.addWarning('信息不存在.');
      });
    };
    $scope.showCreateModal = function() {
      $modal.open({
        templateUrl: 'modals/editorVideoCreate',
        backdrop: true,
        resolve: {},
        controller: ['$scope', '$modalInstance', 'CATEGORY_LIST',
          'ALL_CATEGORIES_ZH_MAP',
          function($scope, $modalInstance, CATEGORY_LIST,
                   ALL_CATEGORIES_ZH_MAP) {
            $scope.schema = {
              type: 'html'
            };
            $scope.create = function(name, ids) {
              $modalInstance.close({
                name: name,
                ids: ids,
                category: categoryId
              });
            };
            $scope.cancel = function() {
              $modalInstance.dismiss('cancel');
            };
          }]
      }).result.then(function(result) {
        $rootScope.loadingMessage = '正在保存';
        videoListService.createVideo(result.name,
          result.ids,
          result.category).then(function() {
          $rootScope.loadingMessage = '';
          alertsService.addSuccessMessage('保存成功');
          $scope.loadData();
        }, function() {
          $rootScope.loadingMessage = '';
          alertsService.addWarning('保存失败.');
        });
      });
    };
    $scope.deleteData = function(objid, ev) {
      ev.stopPropagation();
      var confirm = $mdDialog.confirm({
        template: [
          '<md-dialog aria-label="<[dialog.label]>">',
          '<md-content>',
          '<h2><[ dialog.title ]></h2>',
          '<p><[ dialog.content ]></p>',
          '</md-content>',
          '<div class="md-actions">',
          '<md-button ng-if="dialog.$type == \'confirm\'" ng-click="dialog.abort()">',
          '<[ dialog.cancel ]>',
          '</md-button>',
          '<md-button ng-click="dialog.hide()" class="md-primary">',
          '<[ dialog.ok ]>',
          '</md-button>',
          '</div>',
          '</md-dialog>'
        ].join('')
      })
        .title('确认删除?')
        .content('您确定要删除数据吗，删除后不能恢复！')
        .ariaLabel('Lucky day')
        .ok('确定')
        .cancel('取消').targetEvent(ev);
      $mdDialog.show(confirm).then(function() {
        videoListService.deleteData(objid).then(function(response) {
          var data = response.data;
          alertsService.addSuccessMessage('删除成功!');
          $scope.loadData();
        })
      }, function() {
      });
    };
  }
]);

oppia.controller('VideoCategoryList', ['$scope', '$modal', '$mdDialog',
  '$rootScope', '$window',
  'oppiaDatetimeFormatter',
  'alertsService', 'FATAL_ERROR_CODES',
  'VideoCategoryService',
  function($scope, $modal, $mdDialog, $rootScope, $window,
           oppiaDatetimeFormatter, alertsService,
           FATAL_ERROR_CODES, VideoCategoryService) {
    var _cursor = null;
    $scope.endOfPageIsReached = false;
    $scope.loadData = function() {
      $rootScope.loadingMessage = '加载中';
      VideoCategoryService.getList().then(function(response) {
        $scope.videos = response.data.results;
        $scope.endOfPageIsReached = !response.data.more;
        _cursor = response.data.cursor;
        $scope.currentUserName = response.data.username;
        $scope.currentUserIsAdmin = response.data.is_admin;
        $rootScope.loadingMessage = '';
      });
    };
    $scope.getLocaleAbbreviatedDatetimeString = function(millisSinceEpoch) {
      return oppiaDatetimeFormatter.getLocaleAbbreviatedDatetimeString(
        millisSinceEpoch);
    };
    $scope.loadData();
    $scope.showMore = function() {
      if (!$rootScope.loadingMessage) {
        VideoCategoryService.getListMore(_cursor).then(function(response) {
          $scope.videos = $scope.videos.concat(response.data.results);
          $scope.endOfPageIsReached = !response.data.more;
          _cursor = response.data.cursor;
        })
      }
    };
    $scope.showCreateModal = function() {
      $modal.open({
        templateUrl: 'modals/editorVideoCreate',
        backdrop: true,
        resolve: {},
        controller: ['$scope', '$modalInstance', 'CATEGORY_LIST',
          'ALL_CATEGORIES_ZH_MAP',
          function($scope, $modalInstance, CATEGORY_LIST,
                   ALL_CATEGORIES_ZH_MAP) {
            $scope.schema = {
              type: 'html',
              ui_config: {
                'hide_complex_extensions': true
              }
            };
            $scope.CATEGORY_LIST_FOR_SELECT2 = [];

            for (var i = 0; i < CATEGORY_LIST.length; i++) {
              $scope.CATEGORY_LIST_FOR_SELECT2.push({
                id: CATEGORY_LIST[i],
                text: ALL_CATEGORIES_ZH_MAP[CATEGORY_LIST[i]]
              });
            }
            $scope.create = function(name, pictureName,
                                     category, objective) {
              $modalInstance.close({
                name: name,
                picture_name: pictureName,
                category: category,
                objective: objective
              });
            };
            $scope.cancel = function() {
              $modalInstance.dismiss('cancel');
            };
          }]
      }).result.then(function(result) {
        $rootScope.loadingMessage = '正在保存';
        VideoCategoryService.create(result.name,
          result.picture_name,
          result.category, result.objective).then(function() {
          $rootScope.loadingMessage = '';
          alertsService.addSuccessMessage('保存成功');
          $scope.loadData();
        }, function() {
          $rootScope.loadingMessage = '';
          alertsService.addWarning('保存失败.');
        });
      });
    };
    $scope.showEditModal = function(objid) {

      $rootScope.loadingMessage = '正在加载';
      VideoCategoryService.get(objid).then(function(response) {
        $rootScope.loadingMessage = '';
        $modal.open({
          templateUrl: 'modals/editorVideoCreate',
          backdrop: true,
          resolve: {},
          controller: ['$scope', '$modalInstance', 'CATEGORY_LIST',
            'ALL_CATEGORIES_ZH_MAP',
            function($scope, $modalInstance, CATEGORY_LIST,
                     ALL_CATEGORIES_ZH_MAP) {
              $scope.schema = {
                type: 'html',
                ui_config: {
                  'hide_complex_extensions': true
                }
              };
              $scope.CATEGORY_LIST_FOR_SELECT2 = [];

              for (var i = 0; i < CATEGORY_LIST.length; i++) {
                $scope.CATEGORY_LIST_FOR_SELECT2.push({
                  id: CATEGORY_LIST[i],
                  text: ALL_CATEGORIES_ZH_MAP[CATEGORY_LIST[i]]
                });
              }
              var data = response.data;
              $scope.name = data.name;
              $scope.id = data.id;
              $scope.picture_name = data.picture_name;
              $scope.created_on = data.created_on;
              $scope.category = data.category;
              $scope.objective = data.objective;
              $scope.a = {};
              $scope.a.objective = data.objective;
              $scope.create = function(name, pictureName,
                                       category, objective) {
                $modalInstance.close({
                  name: name,
                  picture_name: pictureName,
                  category: category,
                  objective: objective,
                  id: $scope.id
                });
              };
              $scope.cancel = function() {
                $modalInstance.dismiss('cancel');
              };
            }]
        }).result.then(function(result) {
          $rootScope.loadingMessage = '正在保存';
          VideoCategoryService.save(result.id, result.name,
            result.picture_name,
            result.category, result.objective).then(function() {
            $rootScope.loadingMessage = '';
            $scope.loadData();
            alertsService.addSuccessMessage('保存成功');
          }, function() {
            $rootScope.loadingMessage = '';
            alertsService.addWarning('保存失败.');
          });
        });
      }, function() {
        alertsService.addWarning('获取数据失败.');
      });
    };
    $scope.deleteData = function(objid, ev) {
      var confirm = $mdDialog.confirm({
        template: [
          '<md-dialog aria-label="<[dialog.label]>">',
          '<md-content>',
          '<h2><[ dialog.title ]></h2>',
          '<p><[ dialog.content ]></p>',
          '</md-content>',
          '<div class="md-actions">',
          '<md-button ng-if="dialog.$type == \'confirm\'" ng-click="dialog.abort()">',
          '<[ dialog.cancel ]>',
          '</md-button>',
          '<md-button ng-click="dialog.hide()" class="md-primary">',
          '<[ dialog.ok ]>',
          '</md-button>',
          '</div>',
          '</md-dialog>'
        ].join('')
      })
        .title('确认删除?')
        .content('您确定要删除数据吗，删除后不能恢复！')
        .ariaLabel('Lucky day')
        .ok('确定')
        .cancel('取消').targetEvent(ev);
      $mdDialog.show(confirm).then(function() {
        VideoCategoryService.deleteData(objid).then(function(response) {
          var data = response.data;
          alertsService.addSuccessMessage('删除成功!');
          $scope.loadData();
        })
      }, function() {
      });
    };
  }
]);
