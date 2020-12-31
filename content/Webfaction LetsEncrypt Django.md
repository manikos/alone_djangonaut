Title: Webfaction LetsEncrypt Django
Date: 2016-12-31
Category: Https
Tags: python, django, webfaction, letsencrypt
Summary: Hosting you Django project on Webfaction is easy. Did you know that converting your website from HTTP to HTTPS, using LetsEncrypt is, also, easy too? Extra bonus: it's free of charge!
description: Automate the process of renewing your ssl certificates using Django, Webfaction and LetsEncrypt.
author: Nick Mavrakis
Status: published


## Why HTTPS


First things first. I do not work for [Google](https://www.google.com) nor I have any (social, financial, ethical etc) benefits from this gigantic company. But let be honest. If you are not ranked hign enough in Google's search results, your optimism about your website success is slowly betake to collapse. I think everybody that owns a website, wants his "e-property" to be shown amongst the first results in Google. Of course, you might say, that the search keywords added in the search bar are very important too, but that is not to be discussed here.

So, you have a website (maybe you have build it too) and your domain is i.e `http://www.ilovewhatido.com/`. Then you read this [blog post](https://security.googleblog.com/2016/09/moving-towards-more-secure-web.html) by Google and got terrified about your ranking position. Thinking *"Oh man, I have to change the http protocol to https. How painful will this be?"* or *"how much do I have to pay (monthly or yearly) in order to do that?"* or *"if I switch to https, will my web app behave the same as it was with http?"*.

Lets give answers to these questions:

+ *"Oh man, I have to change the http protocol to https. How painful will this be?"*

> Super easy. Assuming your application is hosted on [Webfaction](https://www.webfaction.com/), just follow [the guide that follows](#django-webfaction-and-letsencrypt-3-great-friends)!

+ *"How much do I have to pay (monthly or yearly) in order to do that?"*

> None! Zero! Nothing! It's free! Using [LetsEncrypt](https://www.letsencrypt.org/) you get a certificate free of charge that lasts 3 months (60 days). You have the ability to renew the certificate 1 month (30 days) before expiration. Of course, you must be aware that there are various types of certificates. The most used ones are: [Domain Validation - DV](https://en.wikipedia.org/wiki/Domain-validated_certificate), [Organization Validation - OV](https://en.wikipedia.org/wiki/Public_key_certificate#Organization_validation) and [Extended Validation - EV](https://en.wikipedia.org/wiki/Extended_Validation_Certificate). Each type of certificate depends on its lifetime (months or years until expiration), procedure in order to be obtained (is it just one click away or you have to wait days or weeks in order to get it), cost (from free of charge up to thousands of dollars/euros). [LetsEncrypt issues only DN certificates](https://letsencrypt.org/docs/faq/#will-lets-encrypt-issue-organization-validation-ov-or-extended-validation-ev-certificates). You can learn more about the different types of certificates [here](https://kb.wisc.edu/security/page.php?id=18922).<br />
So, why there are so many kind of certificates, you ask? Apart from the fact that certifiacte authorities (CA) have to earn money somehow, each certificate type varies by occasion (are you a small, medium or large-sized company, is it just a personal blog, is it a local news website, are you a medium-sized e-commerce website etc). So, for example, a small-sized business is not obliged to pay thousands of euros/dollars in order to obtain a certificate just to prove to the end user that it is what it claims to be. This kind of business can obtain a free one. Anyway, it is up to the website owner to choose the certificate of his preference. One sidenote though, have you ever noticed in your Web browser, that in some HTTPS sites the whole address bar turns green and the business' info are visible to the left of the URL, whereas in other HTTPS sites the browser's address bar is not green and it just shows a green lockpad? This is because in the first case the website owner choosed an EV certificate (which offers this green address bar) while in the latter case the website owner choosed either a DV or an OV certificate.

+ *"If I switch to https, will my web app behave the same as it was with http?"*

> This depends extremely on the framework your application was build. Using [Django](https://www.djangoproject.com/) there is nothing to worry about when switching to HTTPS. Just make sure you are including the [SecurityMiddleware](https://docs.djangoproject.com/en/dev/ref/middleware/#module-django.middleware.security) in your [MIDDLEWARE](https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-MIDDLEWARE) setting. After you switch to HTTPS, run the following Django command in your server (to which you will be connected via `ssh`): [`python manage.py check --deploy`](https://docs.djangoproject.com/en/dev/ref/django-admin/#cmdoption-check-deploy). This will check your deployment settings and underline any potential warnings you should take a closer look.

<br />
## Django, Webfaction and Letsencrypt (3 great friends!)

So, you have build your HTTP website using Django, uploaded to Webfaction and everything works smoothly. Now you want to switch to HTTPS. Here is what to do (do not be terrified of the too many steps, I am just too descriptive!):
**(Many thanks to [cpbotha](https://cpbotha.net/2016/07/18/installing-free-lets-encrypt-ssl-certificates-on-webfaction-in-3-easy-steps/), [Neilpang acme.sh](https://github.com/Neilpang/acme.sh) and [ryans answer](https://community.webfaction.com/questions/19988/using-letsencrypt#answer-container-19989). Forgive me if there is someone I forget.)**

[UPDATE, thanks to Ned Batchelder (see comments below)]: In order for the follow to work you should have [openssl](https://www.openssl.org/) installed (just run `which openssl` and check if it's installed), otherwise install it following [this guide](http://stackoverflow.com/questions/9655613/installing-openssl-from-source#answer-9658354).


1. Login to your
    [Applications](https://my.webfaction.com/applications)
    and click `Add new application`
2. Select a name for it, say `my_ssl_app` and under the `App category` menu select `PHP`. Under the `App type` select `Static/CGI/PHP-7.0`. Click the `Save` button.
3. Now navigate to your [Websites](https://my.webfaction.com/websites), make an exact copy of your existent HTTP website and enable HTTPS on it. How? Simple create a new website, choose the same domains (with and without `www`), choose the same Application (not the one we have just created) but **do not forget to select the button `Encrypted website (https)`**. Click `Save`.
4. You will notice that your HTTPS website says *Security HTTPS, using shared certificate*. That's OK for now. We'll fix that later.
5. Select your HTTP version of your website and under the `Contents` section remove your existing application. Then, add the new one we just created (`my_ssl_app`). Click `Save`.
6. **Now, if you visit your site you will NOT get your usual homepage**. We have not done any redirection to HTTPS yet. Stay with me!
7. From your local machine open terminal and `ssh yourUserName@webXXX.webfaction.com`
8. `vim ~/webapps/my_ssl_app/.htaccess`
9. Hit key `i` (to enter Insert mode and start writing), copy (`Ctrl + c`) the following text and paste it (`Ctrl + Shift + v`) to the opened file (`.htaccess`). After pasting, hit the `Esc` key and then write `:wq` (this will save the file and quit the vim editor):

		:::apacheconf
		RewriteEngine on
		RewriteRule !^.well-known($|/) https://%{HTTP_HOST}%{REQUEST_URI} [R=301,L]

10. Done with redirection. Now if you visit your site (`mysite.com`) you will be redirected to `https://mysite.com`, BUT a security warning will arise saying that the site you are trying to visit may be dangerous or so. That's because we are using a shared certificate. Getting closer!
11. In terminal you must install the terrific [acme.sh]((https://github.com/Neilpang/acme.sh)) script. Simply:

		:::shell
		curl https://get.acme.sh | sh

12. Everything is done automatically for you. Log out from the terminal and `ssh` to log back in.

13. Now you have the command `acme.sh` available globally. Time to use it. 

14. Before, of course, to request a brand new official certificate from LetsEncrypt, we must request a staging (test) certifiacte, in order to be sure that everything is working properly. So...

15. 
	acme.sh --issue --test -d mysite.com -d www.mysite.com -w ~/webapps/my_ssl_app

16. If everything worked, you should have 7 files to the path `~/.acme.sh/mysite.com/` which are (`ca.cer`, `fullchain.cer`, `mysite.com.cer`, `mysite.com.conf`, `mysite.com.csr`, `mysite.com.csr.conf` and `mysite.com.key`). If something is missing, then maybe this is because these are just test certificates and keys. **Not usable in production**. 

17. Now that everything worked, it's time to issue for the real ones. 

18. (notice the missing `--test` parameter)

		acme.sh --issue -d mysite.com -d www.mysite.com -w ~/webapps/my_ssl_app

19. The above command will fetch the same kind of files (with the same name) but this time this folks are official. Their lifetime is 90 days and LetsEncrypt lets you renew your certificates no earlier than 60 days after your last issue. For example, if you issued your certificates today (2016-12-31) then the earlier you can issue them again (renew them) is at 2017-02-31. Of course there is always the option to renew them earlier by using the `--force` argument.

20. Now go to the [SSL certificates](https://my.webfaction.com/ssl-certificates), select `Add SSL Certificate` and choose `Upload Certificate`. *This step, you only have to do it once*. Give it a name, say `mysite_cert` (**remember this name, it will be used in the last step**) and then copy the contents of `~/.acme.sh/mysite.com/mysite.com.cer` to a file and the upload it to the `Certificate` section. Do the same with the `~/.acme.sh/mysite.com.key` and the `Private Key` section and finally with the `~/.acme.sh/ca.cer` and the `Intermediates/bundle` section. All these could be done via the [create_certificate funtion](https://docs.webfaction.com/xmlrpc-api/apiref.html#method-create_certificate) of the Webfaction's API, of course.

21. [SCRIPT UPDATED ON 2017-02-21] Now for my favourite part, *automation*. I have written a Python (2.7) script in order to talk to [Webfaction's API](https://docs.webfaction.com/xmlrpc-api/apiref.html) and update my certificates automatically without bringing my site offline AND without having me (a human) to interact with the Control Panel every 2 months in order to install manually the renewed certificates. This Python script is executed every day (as a cron job). 

		:::python
		#!/usr/local/bin python

		from os import chdir, environ, getcwd, listdir, stat

		from sys import exit

		from subprocess import Popen, PIPE

		from xmlrpclib import ServerProxy, Fault

		
		HIDDEN_ACME_DIR_NAME = '.acme.sh'

		
		def data_to_var(filename):
	    	try:
	        	assert (filename in listdir('.') and stat(filename).st_size > 0)
	    	except AssertionError as exc:
	        	exit('The file \"{}\" does not exist inside \"{}\" or is empty. Exception: {}'.format(filename, getcwd(), exc))
	    	else:
	        	with open(filename, 'r') as f:
	            	var_cert = f.read()
	        	return var_cert


		if __name__ == '__main__':
			# Run the command advised by acme.sh script in order to renew the certificates.
			# Each certificate lasts 90 days and the max permitted day to renew a certificate is 60 days from the issue date -
			# in other words the earlier we can renew a certificate is 30 days before expiration. This can be changed through
			# the --days argument during the --issue step. Type ".acme.sh/acme.sh --help" for more information.
			# This script will run as a cron job every day in order for the certs to be renewed when appropriate.

			acme_process = Popen(['%s/acme.sh' % HIDDEN_ACME_DIR_NAME, 'cron'], stdout=PIPE, stderr=PIPE)
			out, err = acme_process.communicate()

			if err:
				exit("An error occurred during the renewal process. Error: {}".format(err))

			if 'Cert success.' in out:
				hostname, err = Popen(['hostname', '-s'], stdout=PIPE, stderr=PIPE).communicate()
				if err:
					exit("An error occurred while trying to determine the hostname. Error: {}".format(err))
				d = {
        			'url': 'https://api.webfaction.com/',  # Fixed. Not to be changed.
        			'version': 2,  # Fixed. Not to be changed.
		            's_name': hostname.strip('\n').title(),
		            'user': environ.get('USER'),
		            'pwd': 'password',  # Your Webfaction password.
		            'domain': 'mysite.com',  # Your domain name where you issued the certificate.
		            'cert_name': 'mysite_cert',  # Your certification name (see step #20).
			    }

		        # Initially empty values (to be filled later with data from files)
		        domain_cert, pv_key, intermediate_cert = '', '', ''
		        # Directory declarations in order to know where to work
        		valid_cert_dir = '{home}/{acme}/{domain}'.\
        			format(home=environ.get('HOME'), acme=HIDDEN_ACME_DIR_NAME, domain=d.get('domain'))

        		# Change directory to the one that matches our domain
        		chdir(valid_cert_dir)
        		# Test if current working directory is the valid one
				try:
					assert getcwd() == valid_cert_dir
				except AssertionError:
					exit('Current working directory is not {}! Instead is {}.'.format(valid_cert_dir, getcwd()))

				# try to connect to Webfaction API
				try:
					server = ServerProxy(d.get('url'))
            		session_id, _ = server.login(d.get('user'), d.get('pwd'), d.get('s_name'), d.get('version'))
            	except Fault as e:
            		exit("Exception occurred at connection with Webfaction's API. {}".format(e))
            	else:
            		# Connection is successful. Proceed...

            		# read domain certificate and store it as a variable
            		domain_cert = data_to_var('{}.cer'.format(d.get('domain')))

					# read private key certificate and store it as a variable
            		pv_key = data_to_var('{}.key'.format(d.get('domain')))

		            # read intermediate certificate and store it as a variable
            		intermediate_cert = data_to_var('ca.cer')

		            # Install the renewed certificate to your Web server through the Webfaction's API
		            if domain_cert and pv_key and intermediate_cert:
		                # https://docs.webfaction.com/xmlrpc-api/apiref.html#method-update_certificate
		                # update_certificate(session_id, name, certificate, private_key, intermediates)
		                server.update_certificate(session_id, d.get('cert_name'), domain_cert, pv_key, intermediate_cert)


22. Save the above to your server, say as `.certificate_renewal.py` and **place it under your $HOME directory**, `~/.certificate_renewal.py`.

23. Now, `crontab -e` and delete the line at the very bottom that was inserted during the installation of the `acme.sh` script before (step #10).

24. Instead, write:

		0 2 * * * /usr/local/bin/python $HOME/.certificate_renewal.py 2>> /path/to/your/log

25. The above cron job will run every day at 02.00 (am) and check if your certificates need any renewal. If so, then they will be automatically updated for you (via the function [update_certificate](https://docs.webfaction.com/xmlrpc-api/apiref.html#method-update_certificate)) from the API.

26. Last step. Go to your [websites](https://my.webfaction.com/websites/663047/edit-website) and choose the HTTPS version of your domain. Under the "Security" section, "Choose a certificate" dropdown menu, choose the certificate you created (not the "Shared certificate", of course). You will find it with the name you gave it on step 20 (in this example we gave it the name `mysite_cert`).

27. [BONUS]: If you're using Python 3 (which you should) the following modification should be made in order for the script to work. 
    1. First: change `from xmlrpclib import ServerProxy, Fault` to `from xmlrpc`**`.client`** import ServerProxy, Fault`.
    2. Second: change `if 'Cert success.' in out:` to `if 'Cert success.' in out`**`.decode('utf8')`**:`.
    3. Third: change `'s_name': hostname.strip('\n').title(),` to `'s_name': hostname`**`.decode('utf8')`**`.strip('\n').title(),`.
    3. Fourth: in your cron job change `/usr/local/bin/python` (which defaults to python 2.7 but maybe not if you have already an alias to it with python 3. Better check it by simply typing `python` and check the version you got back. If its 3.x.x then do not alter the cron on step #24, otherwise continue to the change) to `/usr/local/bin/python3.x` where `x` is the version you want to use. That's it!


Wasn't that easy enough? Now you have a HTTPS secured website where the certification is automatically renewed every 2 months!


Happy New Year to all Earth(ians)!
