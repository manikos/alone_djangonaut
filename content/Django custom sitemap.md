Title: Django custom sitemap (updated 2018)
Date: 2016-12-27
Modified: 2018-09-29
Category: Django
Tags: python, sitemap, google
Summary: Build a sitemap (xml file) for multi-regional and multilingual websites using Django's builtin Sitemap framework.
Description: Build a Google-verified sitemap for multi-regional and multilingual websites using Django's builtin Sitemap framework.
Author: Nick Mavrakis
Status: published

**UPDATE Sep 2018**: The old post regarding the template tag had some bugs. As of 2018, I fixed it and now this post
is updated and works only for Python 3.6+.


So you have done the following:

1. Used your favorite Web Framework ([Django](https://www.djangoproject.com/)) to build your website.
2. Made enough [tests](https://docs.djangoproject.com/en/dev/topics/testing/) to verify that everything is working flawlessly.
3. [Translated](https://docs.djangoproject.com/en/dev/topics/i18n/translation/) your whole website in each 
   [language][languages] and (of course) each page has its translated version.
4. Used [`i18n_patterns`][i18n_patterns] function to prefix your urls with the language code.
5. Hosted your website somewhere and...

asked yourself why Google does not index your translated pages of your website.


## Introduction

This [excellent article from Google](https://support.google.com/webmasters/answer/182192?hl=en&ref_topic=2370587) states that there are 2 kinds
of "translated" websites: `multilingual` and `multi-regional`. You can have none, one of them or both, depending on your needs.
Let's assume that you have build a `multiregional` website:

> *A multilingual website is any website that offers content in more than one language. Examples of multilingual websites might include a 
  Canadian business with an English and a French version of its site, or a blog on Latin American soccer available in both Spanish and Portuguese.*

It also states that:

> Keep the content for each language on separate URLs. Don’t use cookies to show translated versions of the page.
  Consider cross-linking each language version of a page. That way, a French user who lands on the German version of your page
  can get to the right language version with a single click. Avoid automatic redirection based on the user’s perceived language.
  These redirections could prevent users (and search engines) from viewing all the versions of your site.

Not to be confused with too many quotes, lets clarify some things:

- Lets say that your domain is `www.example.com`.
- Suppose you have set the [`LANGUAGE`](https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-LANGUAGE) setting as `en-US`.
  This means that the default (and fallback, if translations of other languages are not found) language of your entire website will be `en-US`.
- Next, you have support for 2 other languages, declared in the [LANGUAGES][languages] setting. Say, `it` and `el`.
- As we said, you use [`i18n_patterns`][i18n_patterns] function to prefix your urls with the language code.
  So, the `about` page in English would be: `www.example.com/en/about/`, the Italian version: `www.example.com/it/about/`
  and the Greek version: `www.example.com/el/about/`.
- When someone (who lives in an English spoken language region) searches Google (keywords such as "example about") for your about page, 
  the result is `www.example.com/en/about/` (the english version of the about page).
- When I search Google with keywords such as "example about" (I live in Greece) I expect to get `www.example.com/el/about/`
  but instead I get the same result as the English spoken user. Same happens with the Italian user.

So, how do you tell Google (at least Googlebot) to index the other versions of the same page?


## Enter the **hreflang** attribute

There are 3 ways to notify web crawlers to index your translated pages.
[Another excellent article](https://support.google.com/webmasters/answer/189077?hl=en&ref_topic=2370587) from Google which exposes the 3 potential 
ways (HTML tags, HTTP headers and Sitemap).

In this post, we will cover the 3rd option. That is, build a Sitemap for our entrire website with respect to **all** the supported languages.
How do we do it? Using the [Django's built-in Sitemap framework](https://docs.djangoproject.com/en/dev/ref/contrib/sitemaps/).

But before we jump into code, take a look at the [template of the sitemap file](https://support.google.com/webmasters/answer/2620865?hl=en&ref_topic=2370587)
which we need to construct. The key point is to **include in each `<url></url>` element the page itself and the other versions of this page**
using the `<xhtml:link rel="alternate" hreflang="xx" href="xxx"/>` element. Maybe this sounds confusing but bear with me.

Assuming that you have done the [basics](https://docs.djangoproject.com/en/dev/ref/contrib/sitemaps/#installation) (in order for the `Sitemap`
framework to work properly) and you are in position to generate a `sitemap.xml` file when someone hits `www.example.com/sitemap.xml`,
then lets begin with building owr own sitemap file.

1. Create an empty file `sitemap.xml` and place it under the `templates/` directory.
2. Make sure that the `templates/` dir is [discoverable](https://docs.djangoproject.com/en/dev/ref/settings/#dirs)
   by Django (but you have already done this, right?).
3. Edit your root `URLconf` file and under the url that serves the sitemap file, change the template to be used.
   In my case, I have this (note the `template_name` dictionary key):

		:::python
		urlpatterns += [
		    url(r'^sitemap\.xml/$', django.contrib.sitemaps.views.sitemap, 
				{'sitemaps': SITEMAPS, 
		    	'template_name': 'sitemap.xml'}, 
		    	name='django.contrib.sitemaps.views.sitemap')
		]

3. Edit the `sitemap.py` file that is responsible of generating the sitemap and add in each `Class` that inherits from `django.contrib.sitemaps.Sitemap`
   the attribute `i18n = True`, in order for the sitemap to include **all** the urls (including the ones with the prefixed language code).
   If we didn't include it (the default value is `False`) then the sitemap would include i.e only the `www.example.com/about/` page and not
   the other two ones (`it` and `el`).
4. Create an app (`python manage.py startapp`), if you haven't already, that will hold the project's wide template tags (or/and filters).
   My usual way to do this, is that with every project I always create an app (called `dtl_utils`) which hosts code that is project-wide applied
   (not bound to a specific app). Follow the guide on [how to write custom template tags](https://docs.djangoproject.com/en/dev/howto/custom-template-tags/#writing-custom-template-tags).
   I'll assume that the `.py` file which contains the template tag is named `dtl_tags.py`.
5. Open the `dtl_tags.py` file and add the following:

		:::python
		import re
		from urllib.parse import urlparse

		from django import template
		from django.utils.html import mark_safe
		from django.conf import settings

		register = template.Library()

		LANG_CODES = [lang[0] for lang in settings.LANGUAGES]
		PATTERN = f'^/({"|".join(LANG_CODES)})/'
		REGEX = re.compile(PATTERN)
		HREF_LANG = '<xhtml:link rel="alternate" hreflang="{hreflang}" href="{href}" />'

		@register.simple_tag()
		def sitemap_hreflang_url(uri):
			"""
			parse.urlparse extracts to 6 components (https://tools.ietf.org/html/rfc1808.html):

			scheme://   netloc/           path    ;parameters  ?query   #fragment
			  |            |               |          |          |          |
			|---|   |--------------|  |----------| |------|  |-------|  |------|
			https://www.example.com   /en/moments/ ;type=a   ?active=1   #go-to

			We want each url (generated by the sitemap) to include itself along with
			other translated versions.
			For example: the url "www.example.com" (el) should include itself along
			with "www.example.com/en/" (en) and the url "www.example.com/en/" (en)
			should include itself along with "www.example.com" (el). This procedure
			should apply to all urls.
			Google's answer:
			support.google.com/webmasters/answer/2620865?hl=en&ref_topic=2370587
			:param str uri: A fully qualified URL incl schema (https://ex.com/statues/)
			:return: string
			"""
			parsed_uri = urlparse(uri)
			to_return = []
			for lang_code in LANG_CODES:
				new_path = REGEX.sub(f"/{lang_code}/", parsed_uri.path)
				new_uri = parsed_uri._replace(path=new_path)
				to_return.append(HREF_LANG.format(hreflang=lang_code, href=new_uri.geturl()))

			return mark_safe("\n\t\t".join(to_return))

6. The comments inside the template tag `sitemap_hreflang_url` are quite self-explanatory.
   We take advantage of all the urls generated by the `sitemap.py` file (not shown here, but a simple look of this is shown in the
   [Django docs](https://docs.djangoproject.com/en/dev/ref/contrib/sitemaps/#a-simple-example)) with the option `i18n = True` in each `Class`
   and we try to figure out all the other versions of this url.

7. Open the empty `templates/sitemap.xml` file and add the following:

		:::xml
		{% load dtl_tags %}<?xml version="1.0" encoding="UTF-8"?>
		<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">
		{% for url in urlset %}
			<url>
				<loc>{{ url.location }}</loc>
				{% if url.lastmod %}<lastmod>{{ url.lastmod|date:"Y-m-d" }}</lastmod>{% endif %}
				{% if url.changefreq %}<changefreq>{{ url.changefreq }}</changefreq>{% endif %}
				{% if url.priority %}<priority>{{ url.priority }}</priority>{% endif %}
				{% sitemap_hreflang_url url.location %}
		   </url>
		{% endfor %}
		</urlset>

8. A few notes here:
	- The `<?xm version=...` line should be on the first line (along with the `load` statement), otherwise the `.xml` file will not be valid.
	- The core of this template lives inside `django.contrib.sitemaps.templates` directory. The only parts that we have added are
	  `{% load dtl_tags %}`, `xmlns:xhtml="http://www.w3.org/1999/xhtml"` and `{% sitemap_hreflang_url url.location %}`.


## Conclusion

So, that's it! 

With the above implementation you can have a Google verified sitemap.xml which will inform the Googlebot about the other (translated)
versions of your urls-pages.


[i18n_patterns]: https://docs.djangoproject.com/en/dev/topics/i18n/translation/#django.conf.urls.i18n.i18n_patterns
[languages]: https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-LANGUAGES

