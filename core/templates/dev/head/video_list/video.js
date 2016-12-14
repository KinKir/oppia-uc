/**
 * Created by Administrator on 2016/12/14 0014.
 */
oppia.controller('VideoView', ['$scope', '$modal', '$rootScope', '$window',
  'oppiaDatetimeFormatter', 'alertsService', 'FATAL_ERROR_CODES',
  'videoListService',
  function($scope, $modal, $rootScope, $window,
           oppiaDatetimeFormatter, alertsService, FATAL_ERROR_CODES,
           videoListService) {
    $scope.loadData = function() {
      videoListService.getVideo($scope);
    };
  }]);