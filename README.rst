=================
everyplay-python
=================

A friendly wrapper around the `Everyplay API`_ based on the `SoundCloud python wrapper`_.

.. _Everyplay API: https://developers.everyplay.com/
.. _SoundCloud python wrapper: https://github.com/soundcloud/soundcloud-python/

Installation
------------

To install everyplay-python, simply: ::

    pip install everyplay

Or if you're not hip to the pip: ::

    easy_install everyplay

Basic Use
---------

To use everyplay-python, you must first create a `Client` instance,
passing at a minimum the client id you obtained when you `registered
your app`_: ::

    import everyplay

    client = everyplay.Client(client_id=YOUR_CLIENT_ID)

The client instance can then be used to fetch or modify resources: ::

    videos = client.get('/videos', order='popularity', limit=10)
    for video in videos:
        print video.title
    app = client.get('/games/1')
    print app.permalink_url

.. _registered your app: https://developers.everyplay.com/

Authentication
--------------

All `OAuth2 authorization flows`_ supported by the Everyplay API are
available in everyplay-python. If you only need read-only access to
public resources, simply provide a client id when creating a `Client`
instance: ::

    import everyplay

    client = everyplay.Client(client_id=YOUR_CLIENT_ID)
    video = client.get('/videos/7000')
    print video.title

If however, you need to access private resources or modify a resource,
you will need to have a user delegate access to your application. To do
this, you can use one of the following OAuth2 authorization flows.

**Authorization Code Flow**

The `Authorization Code Flow`_ involves redirecting the user to everyplay.com
where they will log in and grant access to your application: ::

    import everyplay

    client = everyplay.Client(
        client_id=YOUR_CLIENT_ID,
        client_secret=YOUR_CLIENT_SECRET,
        redirect_uri='http://yourapp.com/callback'
    )
    redirect(client.authorize_url())

Note that `redirect_uri` must match the value you provided when you
registered your application. After granting access, the user will be
redirected to this uri, at which point your application can exchange
the returned code for an access token: ::

    access_token, expires, scope, refresh_token = client.exchange_token(
        code=request.args.get('code'))
    render_text("Hi There, %s" % client.get('/me').username)


**User Credentials Flow**

The `User Credentials Flow`_ allows you to exchange a username and
password for an access token. Be cautious about using this flow, it's
not very kind to ask your users for their password, but may be
necessary in some use cases. The credentials flow is currently only allowed for
gamne profile users: ::

    import everyplay

    client = everyplay.Client(
        client_id=YOUR_CLIENT_ID,
        client_secret=YOUR_CLIENT_SECRET,
        username='profile_user_name',
        password='profile_password'
    )
    print client.get('/me').username

.. _`OAuth2 authorization flows`: http://developers.everyplay.com/
.. _`Authorization Code Flow`: http://developers.everyplay.com/
.. _`User Credentials Flow`: http://developers.everyplay.com/

Examples
--------

Resolve a video and print its id: ::

    import everyplay

    client = everyplay.Client(client_id=YOUR_CLIENT_ID)

    video = client.get('/resolve', url='http://everyplay.com/nomon/first-video')

    print video.id


Start following a user: ::

    import everyplay

    client = everyplay.Client(access_token="a valid access token")
    user_id_to_follow = 123
    client.put('/me/followings/%d' % user_id_to_follow)


Proxy Support
-------------

If you're behind a proxy, you can specify it when creating a client: ::

    import everyplay

    proxies = {
        'http': 'example.com:8000'
    }
    client = everyplay.Client(access_token="a valid access token",
                               proxies=proxies)

The proxies kwarg is a dictionary with protocols as keys and host:port as values.

Running Tests
-------------

To run the tests, run: ::

    $ pip install -r requirements.txt
    $ nosetests --with-doctest
    ..................

Success!

Contributing
------------

Contributions are awesome. You are most welcome to `submit issues`_,
or `fork the repository`_.

everyplay-python is published under a `BSD License`_.

.. _`submit issues`: https://github.com/Everyplay/everyplay-python/issues
.. _`fork the repository`: https://github.com/Everyplay/everyplay-python
.. _`BSD License`: https://github.com/Everyplay/everyplay-python/blob/master/LICENSE
