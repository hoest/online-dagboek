"use strict"

###
Facebook button
###
window.user =
  "id": -1
  "first_name": null
  "last_name": null
  "token": null

window.statusChangeCallback = (response) ->
  # Logged into your app and Facebook.
  if response.status is "connected"
    register(response.authResponse)
  else
    window.user =
      "id": -1
      "first_name": null
      "last_name": null
      "token": null

window.checkLoginState = ->
  FB.getLoginStatus (response) ->
    statusChangeCallback(response)

window.fbAsyncInit = ->
  FB.init
    "appId": "169415933126285"
    cookie: true
    xfbml: true
    version: "v2.1"

  FB.getLoginStatus (response) ->
    statusChangeCallback(response)

window.register = (auth) ->
  console.log "auth", auth
  return unless auth?
  FB.api "/me", (response) ->
    console.log "response", response
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
        window.user =
          "id": response.id
          "first_name": response.first_name
          "last_name": response.last_name
          "token": token.token
        event = new CustomEvent "loggedIn", "detail": window.user
        document.dispatchEvent event

# Load the SDK asynchronously
((d, s, id) ->
  fjs = d.getElementsByTagName(s)[0]
  return if d.getElementById(id)
  js = d.createElement(s)
  js.id = id
  js.src = "//connect.facebook.net/nl_NL/sdk.js"
  fjs.parentNode.insertBefore js, fjs
) document, "script", "facebook-jssdk"
