"use strict"

###
AngurlarJS App
###
diary = angular.module "diary", []

diary.directive "diaryNavigation", ->
  template: """<ul>
    <li><a href="#/">Home</a></li>
    <li><a href="#/over-deze-site">Over deze site</a></li>
  </ul>"""

diary.directive "diaryContent", ["$window", "$compile", ($window, $compile) ->
  controller: ($scope) ->
    $scope.user = $window.user
    angular.element(document).on "loggedIn", (e) ->
      $scope.$broadcast "diary::loggedIn"
      $scope.user = e.detail
      $window.user = e.detail

    console.log "1", $window.user.id
    $scope.$on "diary::loggedIn", (event) ->
      console.log "2", $window.user.id
      $scope.user = event.targetScope.user
      $window.user = event.targetScope.user

  link: (scope, element) ->
    element.html("""<div>Hier komt de inhoud: <span ng-model="user">{{user.id}}</span></div>""")
    $compile(element.contents())(scope)

  # template: """<div ng-model="user">Hier komt de inhoud: {{user}}</div>"""
]

diary.directive "diaryFooter", ->
  template: """<p>&#169; 2014 - <a href="http://www.online-dagboek.nl/">www.online-dagboek.nl</a></p>"""
