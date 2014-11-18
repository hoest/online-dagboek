"use strict"

###
AngurlarJS App
###
@diary = angular.module "diary", ["ngRoute", "ngResource"]

###
Authenticate interceptor
###
diary.factory "diaryAuthenticate", ["$q", "$location", "$rootScope", ($q, $location, $rootScope) ->
  request: (config) ->
    config.headers = config.headers or {}
    if $rootScope.user?.token?
      config.headers.Authorization = "Basic #{window.btoa("token:" + $rootScope.user.token)}"

    config or $q.when(config)

  requestError: (rejection) ->
    $q.reject(rejection)

  response: (response) ->
    response or $q.when(response)

  responseError: (rejection) ->
    if rejection?.status? and rejection.status is 401
      $location.path("/login")

    $q.reject(rejection)
]

diary.config ["$httpProvider", ($httpProvider) ->
  $httpProvider.interceptors.push "diaryAuthenticate"
]

###
Routes
###
diary.config ["$routeProvider", ($routeProvider) ->
  $routeProvider
    .when "/diary/:diary_id?",
      controller: "diaryController"
      templateUrl: "/site/static/templates/posts.html"
]

###
Diary controller
###
diary.controller "diaryController", ["$scope", "$rootScope", "$routeParams", "$resource", ($scope, $rootScope, $routeParams, $resource) ->
  Posts = $resource("/api/v1/diaries/#{$routeParams.diary_id}/posts")
  $scope.posts = []
  Posts.get (data) ->
    $scope.posts = data.posts

  $scope.user = $rootScope.user
]

###
Navigation
###
diary.directive "diaryNavigation", ->
  restrict: "A"

  template: """<ul>
    <li><a href="#/">Home</a></li>
    <li ng-if="user.token">Dagboeken<subitems data-diary-list /></li>
    <li><a href="#/over-deze-site">Over deze site</a></li>
  </ul>"""

###
Content
###
diary.directive "diaryContent", ["$rootScope", "$resource", ($rootScope, $resource) ->
  controller: ($scope) ->
    $scope.user = $rootScope.user

  restrict: "A"

  template: """<div ng-if="user.token">
    <p>Welkom {{user.first_name}} ({{user.id}})</p>
    <div data-ng-view></div>
  </div>"""
]

diary.directive "diaryList", ["$resource", "$location", ($resource, $location) ->
  controller: ($scope) ->
    Diaries = $resource("/api/v1/diaries")
    $scope.diaries = []
    Diaries.get (data) ->
      $scope.diaries = data.diaries

    $scope.open = (id) ->
      $location.path("/diary/#{id}")

  restrict: "A"

  replace: true

  template: """<ul>
    <li data-ng-repeat="diary in diaries">
      <a href ng-click="open(diary.id)">{{diary.title}}</a>
    </li>
  </ul>"""
]

###
Footer
###
diary.directive "diaryFooter", ->
  template: """<p>&#169; 2014 - <a href="http://www.online-dagboek.nl/">www.online-dagboek.nl</a></p>"""

###
Facebook picture
###
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
