# GitLab API

## End-points

+ [Users](users.md)
+ [Config](config.md)
+ [Voip SIP](voip_sip.md)
+ [Voip IAX](voip_iax.md)
+ [System](system.md)
+ [System Panel](system_panel.md)

## Introduction

All API requests require authentication. You need to pass a `secret` parameter by url or header. If passed as header, the header name must be "SECRET". You can find or reset your private token in your own profile.

The API uses JSON or XML to serialize data. By default all api requests will be returned with json format but you can specify custom format in request each request.

