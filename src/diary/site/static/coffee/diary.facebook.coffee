"use strict"

###
Facebook button
###
diary.run ["$rootScope", "$window", ($rootScope, $window) ->
  $rootScope.user =
    "id": -1
    "first_name": null
    "last_name": null
    "token": null

  $window.fbAsyncInit = ->
    FB.init
      "appId": "169415933126285"
      cookie: true
      xfbml: true
      version: "v2.1"

    FB.getLoginStatus (response) ->
      statusChangeCallback(response)

  $window.checkLoginState = ->
    FB.getLoginStatus (response) ->
      statusChangeCallback(response)

  statusChangeCallback = (response) ->
    # Logged into your app and Facebook.
    if response.status is "connected"
      getAuthToken(response.authResponse)
    else
      user =
        "id": -1
        "first_name": null
        "last_name": null
        "token": null
      triggerLoggedInEvent user

  getAuthToken = (auth) ->
    return unless auth?
    FB.api "/me", (response) ->
      data = JSON.stringify
        "facebook": response
        "auth": auth

      r = new XMLHttpRequest();
      r.open "POST", "/api/v1/token", true
      r.setRequestHeader "Content-Type", "application/json"
      r.send(data)

      r.onreadystatechange = () ->
        return if r.readyState is not 4 or r.status is not 200
        if r?.response isnt ""
          # success
          token = JSON.parse r.responseText
          # global
          user =
            "id": response.id
            "first_name": response.first_name
            "last_name": response.last_name
            "token": token.token
          triggerLoggedInEvent user

  triggerLoggedInEvent = (user) ->
    event = new CustomEvent "loggedIn", "detail": user
    document.dispatchEvent event
    $rootScope.user = user
    $rootScope.$apply()

  # Load the SDK asynchronously
  ((d, s, id) ->
    fjs = d.getElementsByTagName(s)[0]
    return if d.getElementById(id)
    js = d.createElement(s)
    js.id = id
    js.src = "//connect.facebook.net/nl_NL/sdk.js"
    fjs.parentNode.insertBefore js, fjs
  ) document, "script", "facebook-jssdk"
]
