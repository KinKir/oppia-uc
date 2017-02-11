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

// This directive can only be used in the context of an exploration.

oppia.directive('localfilepathEditor', [
  '$compile', '$http', '$sce', '$timeout',
  'alertsService', 'OBJECT_EDITOR_URL_PREFIX',
  function($compile, $http, $sce, $timeout, alertsService,
           OBJECT_EDITOR_URL_PREFIX) {
    return {
      link: function(scope, element) {
        scope.getTemplateUrl = function() {
          return OBJECT_EDITOR_URL_PREFIX + 'Localfilepath';
        };
        $compile(element.contents())(scope);
      },
      restrict: 'E',
      scope: true,
      template: '<div ng-include="getTemplateUrl()"></div>',
      controller: function($scope) {
        // Reset the component each time the value changes (e.g. if this is part
        // of an editable list).
        $scope.$watch('$parent.value', function(newValue) {
          $scope.localValue = {
            label: newValue || ''
          };
          $scope.imageUploaderIsActive = true;
        });
        /* utf.js - UTF-8 <=> UTF-16 convertion
         *
         * Copyright (C) 1999 Masanao Izumo <iz@onicos.co.jp>
         * Version: 1.0
         * LastModified: Dec 25 1999
         * This library is free. You can redistribute it and/or modify it.
         */
        /*
         * Interfaces:
         * utf8 = utf16to8(utf16);
         * utf16 = utf8to16(utf8);
         */
        function utf16to8(str) {
          var out, i, len, c;
          out = "";
          len = str.length;
          for (i = 0; i < len; i++) {
            c = str.charCodeAt(i);
            if ((c >= 0x0001) && (c <= 0x007F)) {
              out += str.charAt(i);
            } else if (c > 0x07FF) {
              out += String.fromCharCode(0xE0 | ((c >> 12) & 0x0F));
              out += String.fromCharCode(0x80 | ((c >> 6) & 0x3F));
              out += String.fromCharCode(0x80 | ((c >> 0) & 0x3F));
            } else {
              out += String.fromCharCode(0xC0 | ((c >> 6) & 0x1F));
              out += String.fromCharCode(0x80 | ((c >> 0) & 0x3F));
            }
          }
          return out;
        }

        function utf8to16(str) {
          var out, i, len, c;
          var char2, char3;
          out = "";
          len = str.length;
          i = 0;
          while (i < len) {
            c = str.charCodeAt(i++);
            switch (c >> 4) {
              case 0:
              case 1:
              case 2:
              case 3:
              case 4:
              case 5:
              case 6:
              case 7:
                // 0xxxxxxx
                out += str.charAt(i - 1);
                break;
              case 12:
              case 13:
                // 110x xxxx 10xx xxxx
                char2 = str.charCodeAt(i++);
                out += String.fromCharCode(((c & 0x1F) << 6) | (char2 & 0x3F));
                break;
              case 14:
                // 1110 xxxx 10xx xxxx 10xx xxxx
                char2 = str.charCodeAt(i++);
                char3 = str.charCodeAt(i++);
                out += String.fromCharCode(((c & 0x0F) << 12) | ((char2 & 0x3F) << 6) | ((char3 & 0x3F) << 0));
                break;
            }
          }
          return out;
        }

        /*
         * Interfaces:
         * b64 = base64encode(data);
         * data = base64decode(b64);
         */
        var base64EncodeChars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_";
        var base64DecodeChars = [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 62, -1, -1, -1, 63,
          52, 53, 54, 55, 56, 57, 58, 59, 60, 61, -1, -1, -1, -1, -1, -1, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14,
          15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, -1, -1, -1, -1, -1, -1, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40,
          41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, -1, -1, -1, -1, -1];

        function base64encode(str) {
          var out, i, len;
          var c1, c2, c3;
          len = str.length;
          i = 0;
          out = "";
          while (i < len) {
            c1 = str.charCodeAt(i++) & 0xff;
            if (i == len) {
              out += base64EncodeChars.charAt(c1 >> 2);
              out += base64EncodeChars.charAt((c1 & 0x3) << 4);
              out += "==";
              break;
            }
            c2 = str.charCodeAt(i++);
            if (i == len) {
              out += base64EncodeChars.charAt(c1 >> 2);
              out += base64EncodeChars.charAt(((c1 & 0x3) << 4) | ((c2 & 0xF0) >> 4));
              out += base64EncodeChars.charAt((c2 & 0xF) << 2);
              out += "=";
              break;
            }
            c3 = str.charCodeAt(i++);
            out += base64EncodeChars.charAt(c1 >> 2);
            out += base64EncodeChars.charAt(((c1 & 0x3) << 4) | ((c2 & 0xF0) >> 4));
            out += base64EncodeChars.charAt(((c2 & 0xF) << 2) | ((c3 & 0xC0) >> 6));
            out += base64EncodeChars.charAt(c3 & 0x3F);
          }
          return out;
        }

        function base64decode(str) {
          var c1, c2, c3, c4;
          var i, len, out;
          len = str.length;
          i = 0;
          out = "";
          while (i < len) {
            /* c1 */
            do {
              c1 = base64DecodeChars[str.charCodeAt(i++) & 0xff];
            } while (i < len && c1 == -1);
            if (c1 == -1) break;
            /* c2 */
            do {
              c2 = base64DecodeChars[str.charCodeAt(i++) & 0xff];
            } while (i < len && c2 == -1);
            if (c2 == -1) break;
            out += String.fromCharCode((c1 << 2) | ((c2 & 0x30) >> 4));
            /* c3 */
            do {
              c3 = str.charCodeAt(i++) & 0xff;
              if (c3 == 61) return out;
              c3 = base64DecodeChars[c3];
            } while (i < len && c3 == -1);
            if (c3 == -1) break;
            out += String.fromCharCode(((c2 & 0XF) << 4) | ((c3 & 0x3C) >> 2));
            /* c4 */
            do {
              c4 = str.charCodeAt(i++) & 0xff;
              if (c4 == 61) return out;
              c4 = base64DecodeChars[c4];
            } while (i < len && c4 == -1);
            if (c4 == -1) break;
            out += String.fromCharCode(((c3 & 0x03) << 6) | c4);
          }
          return out;
        }

        var safe64 = function(base64) {
          base64 = base64.replace(/\+/g, "-");
          base64 = base64.replace(/\//g, "_");
          return base64;
        };

        var qiniuAppCnfg = {
          qiniuUploadUrl: "http://up.qiniu.com",
          defaultDomain: 'http://ol7l5h5m9.bkt.clouddn.com/',
          Bucket: "test",
          SignUrl: "token.php",
          policy: {
            scope: 'test'
          },
          async: "",
          returnType: "",
          returnUrl: "",
          returnBody: "",
          endUser: "",
          callbackBody: "",
          callbackUrl: "",
          persistentOps: "",
          persistentNotifyUrl: "",
          expire: 1,
          AK: "1bqQxt7j3AK3fpNTjC1SKFBw7wVhT3coLfPMV_dy",
          SK: "AL3ygOTz8KewUs7GliKnbPwUh3lERUWjElL81gyP"
        };
        var genUpToken = function(accessKey, secretKey, putPolicy) {

          //SETP 2
          var put_policy = JSON.stringify(putPolicy);
          console && console.log("put_policy = ", put_policy);

          //SETP 3
          var encoded = base64encode(utf16to8(put_policy));
          console && console.log("encoded = ", encoded);

          //SETP 4
          var hash = CryptoJS.HmacSHA1(encoded, secretKey);
          var encoded_signed = hash.toString(CryptoJS.enc.Base64);
          console && console.log("encoded_signed=", encoded_signed);

          //SETP 5
          var upload_token = accessKey + ":" + safe64(encoded_signed) + ":" + encoded;
          console && console.log("upload_token=", upload_token);
          return upload_token;
        };
        var getPolicy = function(currentFilename) {
          var policy = qiniuAppCnfg.policy;
          policy.scope = qiniuAppCnfg.Bucket;
          var key = currentFilename;
          if (key) {
            policy.scope += ":" + key;
          }
          var type = qiniuAppCnfg.returnType;
          switch (type.type) {
            case "return": {
              var returnUrl = qiniuAppCnfg.returnUrl;
              var returnBody = qiniuAppCnfg.returnBody;
              if (returnUrl) {
                policy.returnUrl = returnUrl;
                policy.returnBody = safe64(returnBody);
              }
            }
              break;
            case "callback": {
              var callbackUrl = qiniuAppCnfg.callbackUrl;
              var callbackBody = qiniuAppCnfg.callbackBody;
              if (callbackUrl) {
                if (!callbackBody) {
                  alertsService.addWarning("callbackBody不能为空，格式为a=1&b=2&c=3");
                  return
                }
                policy.callbackUrl = callbackUrl;
                policy.callbackBody = callbackBody;
              }
            }
          }
          policy['deadline'] = Math.round(new Date().getTime() / 1000) + qiniuAppCnfg.expire * 3600;
          return policy;
        };
        $scope.maxValue = 100;
        $scope.percentComplete = 0;
        $scope.scoreBarLabel = '';
        $scope.showPreview = false;
        $scope.showProgress = false;
        $scope.getScoreValue = function() {
          return $scope.percentComplete;
        };
        var qiniuUpload = function(f, token, key) {
          var xhr = new XMLHttpRequest();
          xhr.open('POST', qiniuAppCnfg.qiniuUploadUrl, true);
          var formData, startDate;
          formData = new FormData();
          if (key) formData.append('key', key);
          formData.append('token', token);
          formData.append('file', f);
          var taking;
          xhr.upload.addEventListener("progress", function(evt) {
            if (evt.lengthComputable) {
              var nowDate = new Date().getTime();
              taking = nowDate - startDate;
              var x = (evt.loaded) / 1024;
              var y = taking / 1000;
              var uploadSpeed = (x / y);
              var formatSpeed;
              if (uploadSpeed > 1024) {
                formatSpeed = (uploadSpeed / 1024).toFixed(2) + "Mb\/s";
              } else {
                formatSpeed = uploadSpeed.toFixed(2) + "Kb\/s";
              }
              $timeout(function() {
                $scope.scoreBarLabel = formatSpeed;
                $scope.percentComplete = Math.round(evt.loaded * 100 / evt.total);
              });

              // console && console.log(percentComplete, ",", formatSpeed);
            }
          }, false);

          xhr.onreadystatechange = function(response) {
            if (xhr.readyState == 4 && xhr.status == 200 && xhr.responseText != "") {
              var blkRet = JSON.parse(xhr.responseText);
              console && console.log(blkRet);
              $timeout(function() {
                $scope.scoreBarLabel = '上传完成！';
                $scope.showPreview = true;
                $scope.localValue.label = qiniuAppCnfg.defaultDomain + blkRet.key;
                var uri = $scope.localValue.label;
                var flashvars = {
                  f: uri,
                  c: 0,
                  p: 1
                };
                var params = {
                  bgcolor: '#FFF',
                  allowFullScreen: true,
                  allowScriptAccess: 'always',
                  wmode: 'transparent'
                };
                var video = [uri + '->video/mp4'];
                CKobject.embed('/third_party/static/ckplayer-6.8/ckplayer/ckplayer.swf',
                  'ckpreview', 'ckplayer_a1', '100%', '100%',
                  true, flashvars, video, params);

                $scope.$apply();
              });
            } else if (xhr.status != 200 && xhr.responseText) {

            }
          };
          startDate = new Date().getTime();
          xhr.send(formData);
          $scope.showProgress = true;
        };

        $scope.validate = function(localValue) {
          return localValue.label && localValue.label.length > 0;
        };

        $scope.$watch('localValue.label', function(newValue) {
          if (newValue) {
            alertsService.clearWarnings();
            $scope.localValue = {
              label: newValue
            };
            $scope.$parent.value = newValue;
          }
        });

        $scope.getPreviewUrl = function(filepath) {
          var encodedFilepath = window.encodeURIComponent(filepath);
          return $sce.trustAsResourceUrl(
            qiniuAppCnfg.defaultDomain + encodedFilepath);
        };

        $scope.resetImageUploader = function() {
          $scope.currentFile = null;
          $scope.currentFilename = null;
          $scope.imagePreview = null;
        };

        $scope.openImageUploader = function() {
          $scope.resetImageUploader();
          $scope.uploadWarning = null;
          $scope.imageUploaderIsActive = true;
        };

        $scope.closeImageUploader = function() {
          $scope.imageUploaderIsActive = false;
        };

        $scope.onFileChanged = function(file, filename) {
          if (!file || !file.size || !file.type.match('video.*')) {
            $scope.uploadWarning = '该文件不是视频文件.';
            $scope.resetImageUploader();
            $scope.$apply();
            return;
          }

          $scope.currentFile = file;
          $scope.currentFilename = filename;
          $scope.uploadWarning = null;

          var reader = new FileReader();
          reader.onload = function(e) {
            $scope.$apply(function() {
              //$scope.imagePreview = e.target.result;
              var filepath = 'http://img.ksbbs.com/asset/Mon_1605/25d705200a4eab4.mp4';
              var encodedFilepath = filepath;// window.encodeURIComponent(filepath);
              $scope.imagePreview = $sce.trustAsResourceUrl(encodedFilepath);
            });
          };
          reader.readAsDataURL(file);

          $scope.$apply();
        };

        $scope.saveUploadedFile = function(file, filename) {
          alertsService.clearWarnings();

          if (!file || !file.size) {
            alertsService.addWarning('请选择文件.');
            return;
          }
          if (!file.type.match('video.*')) {
            alertsService.addWarning(
              '请选择视频格式文件.');
            return;
          }

          if (!filename) {
            alertsService.addWarning('文件名不能为空.');
            return;
          }

          var token = genUpToken(qiniuAppCnfg.AK, qiniuAppCnfg.SK, getPolicy(filename));
          qiniuUpload(file, token, filename);
          return;
          var form = new FormData();
          form.append('image', file);
          form.append('payload', JSON.stringify({
            filename: filename
          }));
          form.append('csrf_token', GLOBALS.csrf_token);

          $.ajax({
            url: '/createhandler/imageupload/' + $scope.explorationId,
            data: form,
            processData: false,
            contentType: false,
            type: 'POST',
            dataFilter: function(data) {
              // Remove the XSSI prefix.
              var transformedData = data.substring(5);
              return JSON.parse(transformedData);
            },
            dataType: 'text'
          }).done(function(data) {
            var inputElement = $('#newImage');
            $scope.filepaths.push(data.filepath);
            $scope.closeImageUploader();
            $scope.localValue.label = data.filepath;
            $scope.$apply();
          }).fail(function(data) {
            // Remove the XSSI prefix.
            var transformedData = data.responseText.substring(5);
            var parsedResponse = JSON.parse(transformedData);
            alertsService.addWarning(
              parsedResponse.error || 'Error communicating with server.');
            $scope.$apply();
          });
        };

        $scope.filepathsLoaded = false;
        // $http.get(
        //   '/createhandler/resource_list/' + $scope.explorationId
        // ).then(function(response) {
        //   $scope.filepaths = response.data.filepaths;
        //   $scope.filepathsLoaded = true;
        // });
      }
    };
  }
]);
