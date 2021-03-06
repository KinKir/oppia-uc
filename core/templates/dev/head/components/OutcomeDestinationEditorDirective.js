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
 * @fileoverview Directives for the outcome destination editor.
 */

oppia.directive('outcomeDestinationEditor', [function() {
  return {
    restrict: 'E',
    scope: {
      outcomeHasFeedback: '=',
      outcome: '='
    },
    templateUrl: 'rules/outcomeDestinationEditor',
    controller: [
      '$scope', 'editorContextService', 'explorationStatesService',
      'StateGraphLayoutService', 'PLACEHOLDER_OUTCOME_DEST', 'focusService',
      function(
          $scope, editorContextService, explorationStatesService,
          StateGraphLayoutService, PLACEHOLDER_OUTCOME_DEST, focusService) {
        $scope.$on('saveOutcomeDestDetails', function() {
          // Create new state if specified.
          if ($scope.outcome.dest === PLACEHOLDER_OUTCOME_DEST) {
            var newStateName = $scope.outcome.newStateName;
            $scope.outcome.dest = newStateName;
            delete $scope.outcome.newStateName;

            explorationStatesService.addState(newStateName, null);
          }
        });

        $scope.onDestSelectorChange = function() {
          if ($scope.outcome.dest === PLACEHOLDER_OUTCOME_DEST) {
            focusService.setFocus('newStateNameInputField');
          }
        };

        $scope.isCreatingNewState = function(outcome) {
          return outcome.dest === PLACEHOLDER_OUTCOME_DEST;
        };

        $scope.newStateNamePattern = /^[a-zA-Z0-9.\s-]+$/;
        $scope.destChoices = [];
        $scope.$watch(explorationStatesService.getStates, function() {
          var currentStateName = editorContextService.getActiveStateName();

          // This is a list of objects, each with an ID and name. These
          // represent all states, as well as an option to create a
          // new state.
          $scope.destChoices = [{
            id: currentStateName,
            text: '(重新输入)'
          }];

          // Arrange the remaining states based on their order in the state
          // graph.
          var lastComputedArrangement = (
            StateGraphLayoutService.getLastComputedArrangement());
          var allStateNames = Object.keys(explorationStatesService.getStates());

          var maxDepth = 0;
          var maxOffset = 0;
          for (var stateName in lastComputedArrangement) {
            maxDepth = Math.max(
              maxDepth, lastComputedArrangement[stateName].depth);
            maxOffset = Math.max(
              maxOffset, lastComputedArrangement[stateName].offset);
          }

          // Higher scores come later.
          var allStateScores = {};
          var unarrangedStateCount = 0;
          for (var i = 0; i < allStateNames.length; i++) {
            var stateName = allStateNames[i];
            if (lastComputedArrangement.hasOwnProperty(stateName)) {
              allStateScores[stateName] = (
                lastComputedArrangement[stateName].depth * (maxOffset + 1) +
                lastComputedArrangement[stateName].offset);
            } else {
              // States that have just been added in the rule 'create new'
              // modal are not yet included as part of lastComputedArrangement,
              // so we account for them here.
              allStateScores[stateName] = (
                (maxDepth + 1) * (maxOffset + 1) + unarrangedStateCount);
              unarrangedStateCount++;
            }
          }

          var stateNames = allStateNames.sort(function(a, b) {
            return allStateScores[a] - allStateScores[b];
          });

          for (var i = 0; i < stateNames.length; i++) {
            if (stateNames[i] !== currentStateName) {
              $scope.destChoices.push({
                id: stateNames[i],
                text: stateNames[i]
              });
            }
          }

          $scope.destChoices.push({
            id: PLACEHOLDER_OUTCOME_DEST,
            text: '新建卡片...'
          });
        }, true);
      }
    ]
  };
}]);
