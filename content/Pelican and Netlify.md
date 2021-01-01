Title: How to create a website using Pelican and Netlify (January 2021)
Date: 2021-1-1
Modified: 2021-1-1
Category: python, website
Tags: python, pelican, netlify
Summary: How to properly set Pelican, Github and Netlify for a static generated website in minutes.
Author: Nick Mavrakis
Status: published

# Introduction

This introduction is going to be short since you already know what [Pelican](https://blog.getpelican.com/), Github and [Netlify](https://www.netlify.com/) is used for. If not, here's an overview of those services:

- Pelican: A [static site generator](https://en.wikipedia.org/wiki/Web_template_system#Static_site_generators) (SSG). In other words, a Python program where you write files in Markdown (or reStructuredText) format and Pelican generates a bunch of `.html` files ready to be seen in your browser or deployed in a web server. Got it? No databases (*static*), bunch of `html`files (*site*), pelican python program (*generator*).
- Github: A website which provides hosting for software development and version control using Git. If you're reading this you already know that!
- Netlify: A website that offers hosting for web applications and static websites. The [free plan](https://www.netlify.com/pricing/) for a simple blog is more than enough. It also has DNS management service where we'll configure a custom domain later on.

The choice Pelican was made because I like Python, I'm very familiar with it and if something breaks I can dig into it and fix it. No need to tell about Github! The choice of Netlify was mainly for experiment. I just wanted to try it out and it worked really well. At first, I tried [Github Pages](https://pages.github.com/), but setting up a custom domain there (with SSL and support for `www`subdomain) was a headache. So, I [separated the concerns](https://en.wikipedia.org/wiki/Separation_of_concerns) and used Github for repo hosting and Netlify for website hosting (plus DNS management).

Feel free to try a different combination for your static site. Check out [Jamstack](https://jamstack.org/generators/)!

# Pelican

As of 1<sup>st</sup> Jan 2021, Netlify [supports these Python versions](https://community.netlify.com/t/python-version-for-custom-build/6267/3) in the Ubuntu Xenial 16.04 image (current default build image for all new sites): 2.7, 3.5, and 3.7. Thus, you should install Python 3.7 in your system. The recommended way is one: [pyenv](https://github.com/pyenv/pyenv). Clean and simple.

Before you start, you should [create a vitrualenv](https://docs.python.org/3/tutorial/venv.html) (using python 3.7) and install every pelican-related package under this virtualenv. That's **very important** in order not to "pollute" your system with unnecessary python packages. 

Since a lot of articles have been written about how to set up Pelican (the [official docs](https://docs.getpelican.com/en/latest/) are quite explanatory too), I'll assume that you have completed [this tutorial](https://frankcorso.dev/setting-up-pelican-static-site-generator.html) by [Frank Corso](https://github.com/fpcorso). After all, it's just a `pip install pelican`.

After that, you should initialize your project with git. `cd my_project && git init`.

## Themes

Most of the times, you'll want to change the default theme. Once [you found](http://pelicanthemes.com/) the one you like, visit the github repository and copy the HTTPS url of it (not the SSH one). Then:

```bash
cd your_project
mkdir themes
git submodule add HTTPS_URL_HERE themes/THEME_NAME_HERE
# example
git submodule add https://github.com/alexandrevicenzi/Flex.git themes/Flex
```

We follow this procedure (instead of `git clone`) because I have been bitten by Netlify error regarding submodules, during the build procedure. The first error was submodules-related and the other was [this](https://community.netlify.com/t/hugo-site-deployment-failed-due-to-host-key-verification/783/4) regarding host key verification.

After you have installed your new theme, read it's documentation, play with the variables it provides (you set these variables inside `pelicanconf.py`) and make sure that your site works as expected and looks good.

## Commands

Now that you have your project ready and you can successfully interact with it in your browser, have a look at the `Makefile` and the `tasks.py` file. These files were produced, automatically, by the `pelican-quickstart` command you typed to get started. When you `pip freeze` you'll see the package `invoke` listed. This [package](http://www.pyinvoke.org/) allows you to run local commands/tasks just like it's complementary `fabric` [which focus](https://www.pyinvoke.org/faq.html#invoke-split-from-fabric) on remote tasks (usually over SSH).

Type `inv --list` (alias for `invoke --list`) and you'll see the available commands. For example, typing `inv build` it will actually run under the hood `pelican pelicanconf.py`. Of course you could write the pelican command yourself but wrap it in a task it's more flexible once the commands are getting more complex and reusability is needed.

The most used out-of-the-box command would probably be `inv serve`. This command runs a localhost server at port 8000. Visit `127.0.0.1:8000` or `localhost:8000` and you should see your site. The annoying part is that you have to hit F5 in your browser each time a change is made in one of your `.md` or `.rst` files. 

Enter, hot-reloading by running `inv livereload` (needs `pip install livereload`). Now, each time you save an article, the browser tab reloads automatically. There is a [known closed issue here](https://github.com/getpelican/pelican/issues/2595), where you have to remove the setting `ARTICLE_URL` from the `pelicanconf.py` or move it to `publishconf.py`. I have done both and works. Among other values, my `publishconf.py` includes `ARTICLE_URL = "{slug}"`.

## Github

My `.gitignore` file looks like this: 

```python
*.pid
*.swp
.gitignore
# do not track output directory since it will be rebuild by Netlify
output/
__pycache__/
# This is a PyCharm-specific directory. Delete it if you're not using PyCharm
.idea/
```

Upload your project to Github.

```bash
cd my_project
git status  # optional, check which files are ready to be staged
git add .
git commit -m "initial commit"
git push -u origin main
```

Done. Now we have to find a home for our project.

## Netlify

In order for others to see your website, you have to host it somewhere. Again, Frank Corso, has a [second part tutorial with pictures](https://frankcorso.dev/deploying-your-pelican-static-site-to-netlify.html) which guides you through setting up Netlify.

Two notes here regarding this tutorial. First, in the "Publish directory" setting, enter `output` instead of `output/`. Secondly, you don't have to set the `PYTHON_VERSION` environment variable to `3.7` since this is the default. On the other hand, none will hurt if you do :)

Procedure in a nutshell:

1. You make changes locally
2. You `git push -u origin main`
3. Netlify is notified by the push and starts the build process
4. One task of the build process is the `Build Command` you wrote
5. Once all build tasks are completed, the `output` folder will hold the final `.html` files (along with any js, css, images, fonts etc) which you see in your browser.

## Custom Domain

Netlify, gives each app a unique url (for example `https://admiring-sammet-45tt89.netlify.app/`). If you're fine with that then... congratulations! You have your site deployed and hosted on Netlify.

If not, you have to buy a domain from a registrar. Usually, you buy the bare domain (`example.com` instead of `www.example.com`) and then you can have as many subdomains as you want (depending on you registrar). 

Once you buy it, you can connect it with your netlify app. Steps to follow:

Open the dashboard of your registrar page, where you have admin privileges of your domain. For this specific domain (say, `alone-djangonaut.com`) change the nameservers to:

```python
dns1.p05.nsone.net
dns2.p05.nsone.net
dns3.p05.nsone.net
dns4.p05.nsone.net
```

Wait 10-15 minutes (maybe less) until the new information is propagated among the nameservers. 

Now, visit the dashboard of your app on Netlify (`https://app.netlify.com/teams/YOUR_USERNAME/sites`). Click on your project you want to bind the domain with. Click `Domain Settings`. You should see this:

<img src="/home/nick/Documents/hobby/Python/alone_djangonaut/content/images/pelican_netlify/netlify_domain_list.png" alt="Domain list in Netlify" style="zoom:80%;" />

If  `Netlify DNS` button is not showing, either the nameservers you entered in your registrar page are not propagated yet or there is a typo there. Check again and refresh the page on Netlify until this button is shown. Once it's there, click on it. You should see this:

<img src="/home/nick/Documents/hobby/Python/alone_djangonaut/content/images/pelican_netlify/netlify_dns.png" alt="Netlify DNS records" style="zoom:80%;" />

Each line is a DNS record. The two records that have `IN NETLIFY` will be already there. Disregard the other records. There is a Bonus section at the end of this article (setting up an email using your domain) that explains these records.

For now, you're all done. Visit your domain and share your work with others!

## Expenses

For a personal blog in order to keep your articles/photos/thoughts/you-name-it you don't want to have an extra headache in your monthly expenses. If you do not buy a domain and use the one provided by Netlify, your monthly charge will be zero (0). 

If you decide to buy one, then you set the monthly charge because not all domains cost the same (it depends on various factors such as the Top Level Domain - `.com`, `.io`, `.dev`, `.info` etc). Thus it's your choice how much you're able to spend.

## Workflow

As we said earlier, each time you make a change in your project in contrast to the one that's on Github, you have to push the changes. That's it! You can also wrap this procedure in a function inside `tasks.py` and simply do `inv push`.

Example:

```python
# tasks.py

# ... other tasks here

@task
def push(c):
    """Push project to Github"""
    c.run('git add . && git commit -m "Update project" && git push origin main')
```

## Bonus section (setup an email with your custom domain)

It's a little bit unprofessional to own a domain and not an email with this domain, isn't it? How about to fix that? Bonus #2: this service is also free!

1. Visit https://forwardemail.net/ and create an account. 
2. Go to https://forwardemail.net/en/my-account/domains and click on `ADD NEW DOMAIN` button. 
3. Enter your custom domain you bought (i.e `alone-djangonaut.com`)
4. Click on `Configure your domain` button and follow the very-well-explained instructions
5. Once you have completed these steps, go back and click on `Verify Records` button (see image below)
6. You'll probably get an error since it's too early. You have to wait from 1-10 hours in order for propagation to complete
7. That's it. Now you can receive email using your domain.

<img src="/home/nick/Documents/hobby/Python/alone_djangonaut/content/images/pelican_netlify/forwardemail.png" alt="Forwardemail domain status page" style="zoom:80%;" />

You can also send emails using your domain (`info@alone-djangonaut.com`). For this, you have to follow the instructions after you click the button `Setup your Gmail`.

You can use the image above (with the DNS records), in the `Custom Domain` section, for reference. All records, are going to be written in the Netlify's DNS records. Not your registrar's page. That's because we have changed the nameservers and we are using Netlify's nameservers.

## Fin

You're now a professional with your own website, domain and email!