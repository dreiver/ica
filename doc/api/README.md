# ICA API

## End-points

+ [Users](users.md)
+ [Config](config.md)
+ [Voip](voip.md)
+ [System](system.md)

## Introduction

All API requests require authentication. You need to pass a `access_token` parameter by url or header. If passed as header, the header name must be "token".

The API uses JSON or XML to serialize data. By default all api requests will be returned in JSON format, but you can specify custom format in each request with `.json` or `.xml` at the end of API URL.

## Authentication

Both methods allowd are basic and token.

### Basic Authentication (sent in header)

	$ curl -u "username" https://example.com/api/v1/conf/index

### Basic Authentication (sent as parameter)

	$ curl https://example.com/api/v1/conf/index?access_token=BASIC-TOKEN

### Token Authentication (sent in header)

	$ curl -H "Authorization: token TOKEN" https://example.com/api/v1/conf/index

### Token Authentication (sent as parameter)

	$ curl https://example.com/api/v1/conf/index?access_token=TOKEN
