<h1 align="center">
<a href="https://github.com/xinbeiliu/Instapic-project">
  <img alt="Instapic" src="https://www.brandchannel.com/wp-content/uploads/2016/05/instagram-new-logo-may-2016.jpg" width="400"></a>
  <br> 👍🏻👎🏻 Instapic - Clone of Instagram <br>
</h1>

<div align="center">
  <sub> Built with ❤︎ by
    <a href="https://github.com/xinbeiliu/">Aileen Liu</a>
</div>
<br>
  
Instapic is a user-friendly social media web application. It combines everything you may need for social media posting, such as uploading photos with captions or hashtags, liking or disliking a photo, saving a photo, search photos by different hashtags, like a real Instagram.

## Requirements

To start using Instapic, you will first need to download Python:

- [`MacOS`](https://www.python.org/downloads/) (v3.4 or above) must be installed.
- [`Windows`](https://www.python.org/downloads/windows/) (v3.4 or above) must be installed.
- [`Linux/Unix`](https://www.python.org/downloads/source/) (v3.4 or above) must be installed.

## Installing

<p>You will create a virtual environment and install them, using a <cite>requirements.txt</cite>
file that has the names and exact versions of products you'd like to use:</p>
<pre>
$ <span>virtualenv</span> <span>env</span>
New python executable in env/bin/python
Installing setuptools, pip...done.
$ <span>source env/bin/activate</span>
(env) $ <span>pip3</span> <span>install -r requirements.txt</span>
Downloading/unpacking Flask (from -r requirements.txt (line 1))
Downloading Flask-0.10.1.tar.gz (544kB): 544kB downloaded
<span>...</span>
</pre>

## Running Server

<pre>
(env) $ <span>python3 server.py</span>
Serving Flask app "server" (lazy loading)
Environment: production
WARNING: This is a development server. Do not use it in a production deployment.
Use a production WSGI server instead.
 * Debug mode: on
 * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 235-437-032
<span>...</span>
</pre>
