/**
 * Created by Administrator on 2017/3/4 0004.
 */
oppia.controller('Classroom', ['$scope', '$modal', '$mdDialog', '$rootScope', '$window',
  '$http', 'oppiaDatetimeFormatter', 'alertsService', 'FATAL_ERROR_CODES',
  function($scope, $modal, $mdDialog, $rootScope, $window, $http, oppiaDatetimeFormatter,
           alertsService, FATAL_ERROR_CODES) {
    var _CLASSROOM_DATA_HANLDER_URL = '/classroom/data/';
    $scope.loadData = function() {
      $rootScope.loadingMessage = '加载中';
      $http.get(_CLASSROOM_DATA_HANLDER_URL + '0').then(function(response) {
        $rootScope.loadingMessage = '';
        var data = response.data;
        $scope.currentUserIsAdmin = response.data.is_admin;
        $scope.list = data.results;
        for (var i = 0; i < $scope.list.length; i++) {
          var arrWeek = ['', '星期一', '星期二', '星期三', '星期四', '星期五', '星期六', '星期日'];
          $scope.list[i].day_of_week = arrWeek[parseInt($scope.list[i].day_of_week)];
          $scope.list[i].sections = eval('[' + $scope.list[i].sections + ']');
          var strSections = '';
          for (var j = 0; j < $scope.list[i].sections.length; j++) {
            strSections += '第' + $scope.list[i].sections[j] + '节' + ' ';
          }
          $scope.list[i].sections = strSections;
        }
      });
    };
    $scope.loadData();
    var showDialog = function(data) {
      return $modal.open({
        templateUrl: 'modals/editorClassroomCreate',
        backdrop: true,
        resolve: {},
        controller: ['$scope', '$modalInstance',
          function($scope, $modalInstance) {
            $scope.md = data;
            $scope.ClassChoices = [
              {id: 1, text: '第1节'},
              {id: 2, text: '第2节'},
              {id: 3, text: '第3节'},
              {id: 4, text: '第4节'},
              {id: 5, text: '第5节'},
              {id: 6, text: '第6节'},
              {id: 7, text: '第7节'},
              {id: 8, text: '第8节'},
              {id: 9, text: '第9节'},
              {id: 10, text: '第10节'},
              {id: 11, text: '第11节'},
              {id: 12, text: '第12节'}
            ];
            $scope.DayOfWeek = [
              {id: 1, text: '星期一'},
              {id: 2, text: '星期二'},
              {id: 3, text: '星期三'},
              {id: 4, text: '星期四'},
              {id: 5, text: '星期五'},
              {id: 6, text: '星期六'},
              {id: 7, text: '星期日'},
            ];
            $scope.ok = function(m) {
              $modalInstance.close(m);
            };
            $scope.cancel = function() {
              $modalInstance.dismiss('cancel');
            };
          }]
      }).result;
    };
    $scope.edit = function(classroom_id) {
      if (!$scope.currentUserIsAdmin) {
        return;
      }
      $http.get(_CLASSROOM_DATA_HANLDER_URL + classroom_id).then(function(response) {
        var data = response.data;
        data.sections = eval('[' + data.sections + ']');
        showDialog(data).then(function(result) {
          $rootScope.loadingMessage = '保存中';
          $http.post(_CLASSROOM_DATA_HANLDER_URL + result.id, result).then(function() {
            $rootScope.loadingMessage = '';
            $scope.loadData();
          });
        });
      });
    };
    $scope.create = function() {
      showDialog().then(function(result) {
        $rootScope.loadingMessage = '保存中';
        $http.post(_CLASSROOM_DATA_HANLDER_URL + '0', result).then(function() {
          $rootScope.loadingMessage = '';
          $scope.loadData();
        });
      });
    };
    $scope.deleteData = function(classroom_id, ev) {

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
        $rootScope.loadingMessage = '正在删除';
        $http['delete'](_CLASSROOM_DATA_HANLDER_URL + classroom_id).then(function() {
          $rootScope.loadingMessage = '';
          alertsService.addSuccessMessage('删除成功');
          $scope.loadData();
        });
      }, function() {
      });
    }
  }]);
