Title: Django, Axios and CSRF token
Date: 2020-4-18
Modified: 2020-4-18
Category: django
Tags: python, django, csrf
Summary: How to properly set Django and axios library to work together with CSRF protection.
Author: Nick Mavrakis
Status: published

# Introduction

I am building a "hybrid web app" (I'll post on it in the near future) using [Vue](https://vuejs.org/) to the front and [Django](https://www.djangoproject.com/) to the back.  A "hybrid web app" is something between a SPA and a classic website. The server sends the HTML template, the HTML template has a Vue component and then Vue takes place, mounts on it and do its things.

The app consists of some forms. When the user presses the `submit` button, the Vue component will make a `POST` `XMLHttpRequest` (aka AJAX request) using the [axios](https://github.com/axios/axios) library and the server will respond with some JSON data. The reason I want to make an AJAX call and not a usual form submit is that I do not want the page to refresh and the state of my Vue app re-initialize. So far so good.

Since, my Django view is `CSRF` protected, I want axios to properly handle the CSRF token for me and everything work transparent. Fortunately, `axios` has two config settings (`xsrfHeaderName` and `xsrfCookieName`) which set the proper header of the request in order to pass the csrf token to the server.

However, `axios` gives you the possibility to add (extra) headers using the `headers` config object. This is the point where I got confused. What is the meaning of having two separate settings for `xsrf` handling while you can manually config this in the `headers` objects?

First things first:

1. The form does not include a hidden input field named `csrftoken` because we want to pass it to the server using only the HTTP headers. More on this on the [`AJAX` section in Django docs](https://docs.djangoproject.com/en/dev/ref/csrf/#ajax).
2. The csrf token is passed to the Vue component as a prop. So, the component knows the token.

## Axios-Django communication using the default settings

Let's begin with the very first response from the server to the client when the latter requests a page. Note, that we will use the defaults that Django **and** axios provide, regarding the CSRF (also, I have deleted some irrelevant request/response headers).

1. Server's very first response. Tells the client to set the cookie named `csrftoken` to this very long value!

```html
HTTP/1.1 200 OK
Date: Fri, 17 Apr 2020 19:05:07 GMT
Server: WSGIServer/0.2 CPython/3.7.1
Content-Type: text/html; charset=utf-8
Set-Cookie: csrftoken=KNsdOUx8u7MSMNPcQdwn5FlrznsGJuhmoCByYyVqW2UHEXV66FC0fBBP2OYlhuJF;
```

2. The page renders and the form appears. We fill the form and hit submit. These are the request headers:

```html
POST /home/ HTTP/1.1
Host: 127.0.0.1:8000
User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:75.0) Gecko/20100101 Firefox/75.0
Accept: application/json, text/plain, */*
Content-Type: application/x-www-form-urlencoded
Cookie: csrftoken=KNsdOUx8u7MSMNPcQdwn5FlrznsGJuhmoCByYyVqW2UHEXV66FC0fBBP2OYlhuJF;
```

​	And these are the response headers 😢:

```html
HTTP/1.1 403 Forbidden
Date: Fri, 17 Apr 2020 19:13:04 GMT
Server: WSGIServer/0.2 CPython/3.7.1
Content-Type: text/html
```

It seems that Django is not able to verify the CSRF token. But how Django looks for it? Remember, we do not include it inside the `form` as a hidden input.

## How Django search for the CSRF token

Django looks two times for the csrf token.

On the first search, Django tries get the token that has set at the beginning of the communication with the client (look the `Set-Cookie` header above). There are two places for that. As a cookie (like above, the default) or embedded inside the session dict.  If stored as a [cookie](https://github.com/django/django/blob/master/django/middleware/csrf.py#L170), Django will look for it. Also if inside the [`session dict`](https://github.com/django/django/blob/master/django/middleware/csrf.py#L161).

The second phase is when the form is submitted (a `POST` request) and the Django view is CSRF protected. Now, Django will have to match the token from the phase one with the one from this request. Django [first look for a request parameter](https://github.com/django/django/blob/master/django/middleware/csrf.py#L297) named `csrfmiddlewaretoken` inside the `request.POST` dictionary. Since we do not provide this, Django skips it and [looks inside the `request.META` dictionary](https://github.com/django/django/blob/master/django/middleware/csrf.py#L309) for a header named `settings.CSRF_HEADER_NAME` ([defaults](https://docs.djangoproject.com/en/dev/ref/settings/#csrf-header-name) to `HTTP_X_CSRFTOKEN`).

Back to our app, there is no `HTTP_X_CSRFTOKEN` header in the request headers above. So, Django is unable to verify the token that comes when the form is submitted with the initial one. Thus, you get a beautiful `403 Forbidden` status code!

## Solution(s)

Each solution has benefits and drawbacks. I will mention both in each case.

### Using only the `headers` object in axios config

Inside the axios `POST` call we do this:

```js
const headers = {"X-CSRFTOKEN": "<csrf_token_very_long_string_goes_here>"}
axios.post("/url/here/", {<form_data_to_post>}, {headers: headers})
```

Refresh everything and lets try again. Here are the request headers:

```html
POST /home/ HTTP/1.1
Host: 127.0.0.1:8000
User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:75.0) Gecko/20100101 Firefox/75.0
Accept: application/json, text/plain, */*
Content-Type: application/x-www-form-urlencoded
X-CSRFTOKEN: KNsdOUx8u7MSMNPcQdwn5FlrznsGJuhmoCByYyVqW2UHEXV66FC0fBBP2OYlhuJF
Cookie: csrftoken=KNsdOUx8u7MSMNPcQdwn5FlrznsGJuhmoCByYyVqW2UHEXV66FC0fBBP2OYlhuJF;
```

And the response ones:

```html
HTTP/1.1 200 OK
Date: Fri, 17 Apr 2020 20:03:19 GMT
Server: WSGIServer/0.2 CPython/3.7.1
Content-Type: application/json
```

Now that the request includes the header `X-CSRFTOKEN` (which is the default Django is looking) with the token as its value, the CSRF mechanism verifies the initial and the new token and responds with the `200 OK` status code!

- Benefits: dead simple to use plus it works with the [`CSRF_COOKIE_HTTPONLY = True`](https://docs.djangoproject.com/en/dev/ref/settings/#csrf-cookie-httponly) setting.
- Drawbacks: if your app has many forms, you have to remember to pass it in each `axios.post()` call. Explicit is better than implicit, but many developers are lazy. Which brings us to the second solution.

### Using the `xsrfHeaderName` and `xsrfCookieName` axios config settings

Inside your `main.js` file (or another that you keep your configurations) enter this:

```js
import axios from 'axios'
axios.defaults.xsrfHeaderName = "X-CSRFTOKEN"
axios.defaults.xsrfCookieName = "csrftoken"
```

Now in each axios `POST` call you make, axios will embed the appropriate header for you.

```js
// No need to set the {headers} object as the 3rd argument
axios.post("/url/here/", {<form_data_to_post>})
```

Here are the request headers:

```html
POST /home/ HTTP/1.1
Host: 127.0.0.1:8000
User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:75.0) Gecko/20100101 Firefox/75.0
Accept: application/json, text/plain, */*
Content-Type: application/x-www-form-urlencoded
X-CSRFToken: KNsdOUx8u7MSMNPcQdwn5FlrznsGJuhmoCByYyVqW2UHEXV66FC0fBBP2OYlhuJF
Cookie: csrftoken=KNsdOUx8u7MSMNPcQdwn5FlrznsGJuhmoCByYyVqW2UHEXV66FC0fBBP2OYlhuJF;
```

Spoiler alert! The response contains a `200 OK` status code.

- Benefits: as previously said, you declare it once in your js config file and forget about it.
- Drawbacks: unfortunately, turning [`CSRF_COOKIE_HTTPONLY = True`](https://docs.djangoproject.com/en/dev/ref/settings/#csrf-cookie-httponly), Django will give you a `403 Forbidden` error since, now, JavaScript (in other words axios) cannot read the cookie and will not set the appropriate header on the request.

### Tweaks/Playground

Bonus: You can change the header names on both Django and axios and things will still work. Example:

```python
# settings.py

# The default is HTTP_X_CSRFTOKEN.
# Now Django will look for this header name on the request.
# Something like: HTTP_BLABLABLA: <very_long_token_here>
CSRF_HEADER_NAME = "HTTP_HELLOWORLD"

# The default is csrftoken.
# Now Django will set csrf cookie token under this name
# Something like this: Set-Cookie: welcometothejungle=<very_long_token_here>;
CSRF_COOKIE_NAME = "welcometothejungle"
```

Of course, the same must appear in axios settings:

```js
// main.js

axios.defaults.xsrfHeaderName = "HELLOWORLD"
axios.defaults.xsrfCookieName = "welcometothejungle"
```

Delete previous stored cookies and refresh. The very first response by the server is this:

```html
HTTP/1.1 200 OK
Date: Fri, 17 Apr 2020 20:57:52 GMT
Server: WSGIServer/0.2 CPython/3.7.1
Content-Type: text/html; charset=utf-8
Set-Cookie: welcometothejungle=bracDaFzr4eXwkiNbZdTEOQ37NRJg1jJIdznw2ypft3ulBSyCc8mKEKBQTm;
```

And then comes the form submit `POST` request:

```html
POST /home/ HTTP/1.1
Host: 127.0.0.1:8000
User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:75.0) Gecko/20100101 Firefox/75.0
Accept: application/json, text/plain, */*
Content-Type: application/x-www-form-urlencoded
HELLOWORLD: SFXi8xjp5U6NKiG4RpAsrPmKi3Jm3jwxJcXlZ41GeY4VccenUS8PL7NTHaKKnSuQ
Cookie: welcometothejungle=SFXi8xjp5U6NKiG4RpAsrPmKi3Jm3jwxJcXlZ41GeY4VccenUS8PL7NTHaKKnSuQ;
```

The response is a `200 OK` status!

## Conclusion

Reading the source code of a library (such a Django) makes you understand some things in depth and know how certain pieces fit together. Try it and you'll not lose!

Personally, I prefer the first approach (the explicit one) because for [security reasons](https://youtu.be/QuhgjXKzfI8?t=4194) I always have `CSRF_COOKIE_HTTPONLY` turned on. It is a very good practice and after all....

> Explicit is better than implicit.
>
> https://www.python.org/dev/peps/pep-0020/