Title: Leaving Webfaction
Date: 2018-7-17
Category: Thoughts
Tags: webfaction
Summary: Why I left the (excellent) Webfaction shared hosting service and just "moved on".
Description: Why I left the (excellent) Webfaction shared hosting service and just "moved on".
Author: Nick Mavrakis
Status: published


When I was young
----------------

Five years ago (2013), when I made my first steps on Web Development, building localhost (dummy) projects I never thought of deployment or security issues.
That's the beauty of working locally. You think, write it down, convert it to code, run it and done. Job's done. But, I wanted to make my work available to the public.
What's the point of building a house, decorate it, paint it but with no guests at all? The point is to share. To evolve.

I was building (still do) [Django](https://www.djangoproject.com/)-based websites and when the time had come to upload it somewhere I did a research.
Few players on the board for Python applications. My best bet back then (with no knowledge about web servers, security, redirects, static files handling etc) was to
rely on a shared hosting service. I had rejected virtual private services (VPS) since I had absolutely no idea about how to setup a server with a Django application.
Remember, it was 5 years ago, Django was at 1.6 release (if I recall correctly), I was just learning HTML, CSS, JS, Git etc and I had my app ready to deploy.
I wrote down on a paper all the possible solutions and finally concluded to [Webfaction](https://www.webfaction.com/). Price was (still is) $10/month.
Not bad for an *all included* hosting service back then.


Webfaction
----------

I signed up for an account, I read their documentation about [launching a Django-based website](https://docs.webfaction.com/software/django/getting-started.html?highlight=django#getting-started-with-django/)
and I had, finally, a Django-powered website online! Of course, I had some problems at the beginning, like setting up SSL, setting up a git server and other things I don't quite recall.
But all of them fixed either by their excellent support team or by searching the vast sea of internet. So far so good.
But I knew I should make myself more independent than to be *enclosed* inside Webfaction's system. Not because it was fancy and I had to learn it but because I wanted to.
I felt like it was a missing piece of my understanding about web development. You see, when you develop a Django application and you hit `./manage.py runserver` you're invoking a server.
The concept of the *server* is everywhere. I wanted to learn how it worked. How to setup a machine from zero to one hundred. I wanted to have full control of my machine. So, I decided to
leave Webfaction and move on a VPS service. That happened on early 2018.


Virtual Private Server
----------------------

Like previously, I had no idea what to do. I signed up on both [Linode](https://linode.com) and [DigitalOcean](https://digitalocean.com/) and followed some *getting started* guides.
I read about how [nginx](https://www.nginx.com) works, how it process a request, security issues, backup, email. Remember, I had no idea how to setup a Linux server machine and configure
it properly. An analogy would be like this: Webfaction is like a cookie-cutter house where you get a house full-equipped but with no access to some areas/places. On the other hand,
DigitalOcean is like the tools you need to build the house from the ground up. You have to saw the woods, to nail the floor, to connect the wires etc. All these by yourself.

> Hard but challenging.

Fast forward to today, after two years reading about web servers (and still do), how to automate stuff using [Ansible](https://www.ansible.com/), how to secure my server and other
things as well (uWSGI, database, etc), I am in position to deploy a website with a hit of a button. That's a great improvement for me.


Going serverless
----------------

This new kid on the block, has drawn my attention but I have not study it yet. [Zappa](https://www.zappa.io/) is an interesting web service to look at. But we have time for this.


Conclusion
----------

I wanted to point out the reasons that made me left a shared hosting service and joining a VPS one. I like the fact that I can `sudo apt-get install something` and have full control
of my machine. Other don't like that. Respectable. Maybe in the future I'll leave this too and join a serverless web service. Who knows?
P.S: I have also tried [Heroku](https://www.heroku.com) which is an amazing web service but I personally, do not like to much magic behind the scenes. I want things to be crystal clear
the moment they happen. One of the reasons I left Heroku too (but I have a couple of websites right now, powered by Heroku).

