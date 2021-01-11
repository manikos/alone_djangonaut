#!/usr/bin/env python
# -*- coding: utf-8 -*- #

from datetime import datetime

PATH = "content"
AUTHOR = "Nick Mavrakis"
SITENAME = "Alone Djangonaut"
SITEURL = "http://127.0.0.1:8000"
THEME = "themes/Flex"

ARTICLE_SAVE_AS = "{slug}.html"
PAGE_URL = "page/{slug}/"
PAGE_SAVE_AS = "page/{slug}/index.html"
CATEGORIES_SAVE_AS = "categories.html"
TAGS_SAVE_AS = "tags.html"

STATIC_PATHS = [
    "images",
    "extra",
]
EXTRA_PATH_METADATA = {
    #'extra/robots.txt': {'path': 'robots.txt'},
    "extra/favicon.ico": {"path": "extra/favicon.ico"},
    "extra/manikos_style.css": {"path": "extra/manikos_style.css"},
}

MARKDOWN = {
    "extension_configs": {
        "markdown.extensions.codehilite": {"css_class": "highlight"},
        "markdown.extensions.extra": {},
        "markdown.extensions.meta": {},
        "markdown.extensions.toc": {},
    },
    "output_format": "html5",
}

LOAD_CONTENT_CACHE = False

TIMEZONE = "Europe/Athens"

DEFAULT_LANG = "en"

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = "feeds/all.atom.xml"
CATEGORY_FEED_ATOM = "feeds/{slug}.atom.xml"

# FEED_ALL_ATOM = None
# CATEGORY_FEED_ATOM = None
# TRANSLATION_FEED_ATOM = None
# AUTHOR_FEED_ATOM = None
# AUTHOR_FEED_RSS = None

DEFAULT_PAGINATION = 10
ARTICLE_ORDER_BY = "reversed-date"

# Uncomment following line if you want document-relative URLs when developing
# RELATIVE_URLS = True

# Plumage template settings
# SITE_THUMBNAIL = '/images/logo/logo_3.png'
# SITE_THUMBNAIL_TEXT = 'live in the pale blue dot'

# Flex template settings
# (https://github.com/alexandrevicenzi/Flex/wiki/Custom-Settings)
SITELOGO = f"{SITEURL}/images/logo/logo_3.png"
FAVICON = f"{SITEURL}/extra/favicon.ico"
SITETITLE = "Alone Djangonaut"
SITESUBTITLE = "living in the pale blue dot"
SITEDESCRIPTION = "Tutorials, blog posts and thoughts of a Django developer. He/him. Music lover."
DISABLE_URL_HASH = True
THEME_COLOR = "dark"
THEME_COLOR_AUTO_DETECT_BROWSER_PREFERENCE = True
THEME_COLOR_ENABLE_USER_OVERRIDE = True
# BROWSER_COLOR = '#101010'
COPYRIGHT_NAME = "Nick Mavrakis"
COPYRIGHT_YEAR = datetime.now().year
# HOME_HIDE_TAGS = False
MAIN_MENU = True
MENUITEMS = (
    ("Archives", "/archives.html"),
    ("Categories", "/categories.html"),
    ("Tags", "/tags.html"),
)
# available social names: email, facebook, github, google, instagram,
# linkedin, medium, pinterest, reddit, rss, soundcloud stack-overflow,
# tumblr, twitter, youtube, gitlab, xing, bitbucket
SOCIAL = [
    ("twitter", "https://twitter.com/manikosN"),
    ("github", "https://github.com/manikos"),
    ("stack-overflow", "https://stackoverflow.com/users/2231182/nik-m"),
    ("rss", "feeds/all.atom.xml"),
]
DISQUS_SITENAME = "manikos"
CUSTOM_CSS = "extra/manikos_style.css"
ROBOTS = "all"
PYGMENTS_STYLE = "monokai"


# DISCLAIMER = 'This blog-website expresses my own thoughts, opinions and ideas in order to keep an order in my head. Any reference to an external source is linked.'

# Links
# LINKS_WIDGET_NAME = 'Useful'
# LINKS = (('Pelican', 'http://getpelican.com/'),
#         ('Python.org', 'http://python.org/'),
#         ('Jinja2', 'http://jinja.pocoo.org/'),)

# Social widget
# SOCIAL_WIDGET_NAME = 'Out there'
