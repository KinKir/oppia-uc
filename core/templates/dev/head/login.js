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

oppia.controller('Login', ['$scope', '$modal', '$rootScope', '$window',
  '$http', 'alertsService',
  function($scope, $modal, $rootScope, $window, $http, alertsService) {
    var LOGIN_URL = '/login';
    $scope.login = function() {
      $http.post(LOGIN_URL, {
        username: $scope.username,
        password: $scope.password,
        return_url: $scope.return_url
      }).then(function(response) {
          var data = response.data;
          if (data.res === true || data.res === 'true') {
            document.write(data.msg);
          } else {
            alertsService.addWarning('登录失败' + data.msg);
          }
        },
        function() {
          alertsService.addWarning('登录失败');
        });
    };
  }
]);
