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

diary.directive "diaryContent", ->
  controller: ($scope) ->
    angular.element(document).on "loggedIn", (e) ->
      $scope.$broadcast "diary::loggedIn"
      $scope.user = e.detail
      $scope.$apply()

  template: """<div>Welkom {{user}}</div>"""

diary.directive "diaryFooter", ->
  template: """<p>&#169; 2014 - <a href="http://www.online-dagboek.nl/">www.online-dagboek.nl</a></p>"""
