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

### Enable the Google Drive API
To get started integrating with the Google Drive UI, you need to enable the Drive API within your app's 
Cloud Platform project and provide configuration details.

Please see [Enable the Google Drive API](https://developers.google.com/drive/api/v3/enable-drive-api)

## Unit testing
> In order to execute the unit test that downloads content from Google Drive, you must have access to the 
> Google Drive account where the content is stored. 

## Download a copy of a website

This application needs a local copy of a website (www.fiquipedia.es) to use as input. The source HTML will be 
converted to Markdown.

### Prerequisites on Linux (Ubuntu/Debian)
#### Install 'wget'
> $ apt-get install wget

### Prerequisites on Mac
#### Install Homebrew
> $ /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

#### Install 'wget'
> $ brew install wget

### Using 'wget' to download a local copy of a website
> wget --content-disposition --recursive -p http://www.fiquipedia.es

### URL parameters in file names downloaded by wget 

If the server is kind, it might be sticking a Content-Disposition header on 
the download advising your client of the correct filename. Telling `wget` to 
listen to that header for the final filename is as simple as:

> wget --content-disposition

Otherwise, you need to execute this script to remove the URL parameters from
the file names added by wget` 

```sh
# /bin/bash
for i in `find $1 -type f`
do
    output=`echo $i | cut -d? -f1`
    if [ $i != $output ]
    then
        mv $i $ouput
    else
        echo "Skiping $i"
    fi
done
```