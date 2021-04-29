# gsites2md

HTML to Markdown tool, designed to migrate content from Google Sites to gitlab pages.

Tested with [fiquipedia.es](http://fiquipedia.es) (Work in progress)

## A bit of history
In 2012, a one-man army started building [fiquipedia.es](http://fiquipedia.es), hosted on 
[Google Sites](https://sites.google.com/). This page promptly became a reference in the 
Physics and Chemistry Spanish educational landscape. 

Unfortunately Google decided to discontinued Google Sites Classics from September 1st, 2021 on. 
So, our lonely hero decided to migrate the huge amount of content to 
[Gitlab Pages](https://docs.gitlab.com/ee/user/project/pages/). The pre-existing HTML to Markdown migration 
tools did not provide a clean Markdown, so I decided to help.

> Something is infinitely greater than zero
> 
> `E.G.S.` (fiquipedia man)

If you have a Physics or Chemistry problem, if no one else can help, 
and if you can browse to [fiquipedia.es](http://fiquipedia.es) and you find the solution....maybe you can 
[buy a coffe to fiquipedia.es](https://ko-fi.com/fiquipedia).

## Setting up your development environment
These are some recommended readings in order to set up a local environment using PyCharm;
   * [Create a Project from GitHub](https://www.jetbrains.com/pycharm/guide/tips/create-project-from-github/)
   * [Setting Up a Virtual Environment In PyCharm](https://arcade.academy/venv_install/index.html)

### requirements.txt
The standard in Python projects is to create a file called **requirements.txt** and list the packages you want in there.

PyCharm will automatically ask if you want to install those packages as soon as you type them in. Go ahead and let it.

```
beautifulsoup4
google-api-python-client
google-auth-oauthlib
```
## Unit testing
> In order to execute the unit test that download content from Google Driver 
> you must have access to the Google Drive account where the content is stored. 
