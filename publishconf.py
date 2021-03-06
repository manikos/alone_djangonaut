#!/usr/bin/env python
# -*- coding: utf-8 -*- #
import os
import sys
sys.path.append(os.curdir)
from pelicanconf import *

# If your site is available via HTTPS, make sure SITEURL begins with https://
SITEURL = "https://alone-djangonaut.com"
RELATIVE_URLS = False
ARTICLE_URL = "{slug}"

FEED_ALL_ATOM = "feeds/all.atom.xml"
CATEGORY_FEED_ATOM = "feeds/{slug}.atom.xml"

DELETE_OUTPUT_DIRECTORY = True

# Following items are often useful when publishing
# DISQUS_SITENAME = ""
# GOOGLE_ANALYTICS = ""

# Flex template settings
# (https://github.com/alexandrevicenzi/Flex/wiki/Custom-Settings)
SITELOGO = f"{SITEURL}/images/logo/logo_3.png"
FAVICON = f"{SITEURL}/extra/favicon.ico"
