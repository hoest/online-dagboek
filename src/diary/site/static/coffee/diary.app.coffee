"use strict"

###
AngurlarJS App
###
@diary = angular.module "diary", []

diary.directive "diaryNavigation", ->
  restrict: "A"

  template: """<ul>
    <li><a href="#/">Home</a></li>
    <li><a href="#/over-deze-site">Over deze site</a></li>
  </ul>"""

diary.directive "diaryContent", ["$rootScope", ($rootScope) ->
  controller: ($scope) ->
    $scope.user = $rootScope.user

  restrict: "A"

  template: """<div ng-if="user.token">
    <p>Welkom {{user.first_name}} ({{user.id}})</p>
  </div>"""
]

diary.directive "diaryFooter", ->
  template: """<p>&#169; 2014 - <a href="http://www.online-dagboek.nl/">www.online-dagboek.nl</a></p>"""

diary.directive "facebookPicture", ["$rootScope", ($rootScope) ->
  controller: ($scope) ->
    $scope.user = $rootScope.user

  restrict: "A"

  template: """<div class="facebook-picture" ng-if="user.token">
    <a href="//www.facebook.com/{{user.id}}">
      <img src="//graph.facebook.com/{{user.id}}/picture"
           alt="Profielfoto van {{user.first_name}}"
           title="Profielfoto van {{user.first_name}}" />
    </a>
  </div>"""
]
