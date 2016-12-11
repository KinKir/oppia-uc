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
 * Directive for the MP4 Video rich-text component.
 *
 * IMPORTANT NOTE: The naming convention for customization args that are passed
 * into the directive is: the name of the parameter, followed by 'With',
 * followed by the name of the arg.
 */
oppia.directive('oppiaNoninteractiveVideoMp4', [
  '$sce', 'oppiaHtmlEscaper', 'EVENT_HTML_CHANGED',
  function($sce, oppiaHtmlEscaper, EVENT_HTML_CHANGED) {
    return {
      restrict: 'E',
      scope: {},
      templateUrl: 'richTextComponent/VideoMp4',
      link:function(scope, element, attrs){

      },
      controller: ['$scope', '$attrs', function($scope, $attrs) {

        $scope.videoUrl = $sce.trustAsResourceUrl(
          oppiaHtmlEscaper.escapedJsonToObj($attrs.videoUrlWithValue));
        var uri = oppiaHtmlEscaper.escapedJsonToObj($attrs.videoUrlWithValue)
          ||  oppiaHtmlEscaper.escapedJsonToObj($attrs.filepathWithValue);
        var flashvars = {
          f: uri,
          c: 0,
          p: 1
        };
        var params = {bgcolor: '#FFF', allowFullScreen: true, allowScriptAccess: 'always', wmode: 'transparent'};
        var video = [uri + '->video/mp4'];
        CKobject.embed('/third_party/static/ckplayer-6.8/ckplayer/ckplayer.swf', 'a1', 'ckplayer_a1', '100%', '100%', true, flashvars, video, params);
        // Clearing the video URL src after a card leaves the user's view
        // helps browsers clear memory and release resources. Without this,
        // a bug was observed where resources would freeze for learning
        // experiences that rely heavily on video.
        //
        // See W3C spec 4.7.10.18
        // Ref: https://www.w3.org/TR/html5/embedded-content-0.html
        $scope.$on(EVENT_HTML_CHANGED, function() {
          $scope.videoUrl = '';
        });
      }]
    };
  }
]);
