import everyplay

from everyplay.tests.utils import MockResponse

from urllib import urlencode

from nose.tools import eq_, raises
from fudge import patch


def test_kwargs_parsing_valid():
    """Test that valid kwargs are stored as properties on the client."""
    client = everyplay.Client(client_id='foo', client_secret='foo')
    assert isinstance(client, everyplay.Client)
    eq_('foo', client.client_id)
    client = everyplay.Client(client_id='foo', client_secret='bar',
                               access_token='baz', username='you',
                               password='secret', redirect_uri='foooo')
    eq_('foo', client.client_id)
    eq_('baz', client.access_token)


@raises(AttributeError)
def test_kwargs_parsing_invalid():
    """Test that unknown kwargs are ignored."""
    client = everyplay.Client(foo='bar', client_id='bar')
    client.foo


def test_url_creation():
    """Test that resources are turned into urls properly."""
    client = everyplay.Client(client_id='foo')
    url = client._resolve_resource_name('videos')
    eq_('https://api.everyplay.com/videos.json', url)
    url = client._resolve_resource_name('/videos/')
    eq_('https://api.everyplay.com/videos.json', url)


def test_url_creation_options():
    """Test that resource resolving works with different options."""
    client = everyplay.Client(client_id='foo', use_ssl=False)
    client.site = 'everyplay.dev'
    url = client._resolve_resource_name('games/1')
    eq_('http://everyplay.dev/games/1.json', url)


def test_method_dispatching():
    """Test that getattr is doing right by us."""
    client = everyplay.Client(client_id='foo')
    for method in ['get', 'post', 'put', 'delete', 'head']:
        p = getattr(client, method)
        eq_((method,), p.args)
        eq_('_request', p.func.__name__)


def test_host_config():
    """We should be able to set the site on the client."""
    client = everyplay.Client(client_id='foo', site='api.everyplay.dev')
    eq_('api.everyplay.dev', client.site)
    client = everyplay.Client(client_id='foo')
    eq_('api.everyplay.com', client.site)


@patch('requests.get')
def test_disabling_ssl_verification(fake_get):
    """We should be able to disable ssl verification when we are in dev mode"""
    client = everyplay.Client(client_id='foo', site='api.everyplay.dev',
                               verify_ssl=False)
    expected_url = '%s?%s' % (
        client._resolve_resource_name('videos'),
        urlencode({
            'order': 'popularity',
            'limit': 5,
            'client_id': 'foo'
        }))
    headers = {
        'User-Agent': everyplay.USER_AGENT
    }
    (fake_get.expects_call()
             .with_args(expected_url,
                        headers=headers,
                        verify=False,
                        allow_redirects=True)
             .returns(MockResponse("{}")))
    client.get('videos', order='popularity', limit=5)


@raises(AttributeError)
def test_method_dispatching_invalid_method():
    """Test that getattr raises an attributeerror if we give it garbage."""
    client = everyplay.Client(client_id='foo')
    client.foo()


@patch('requests.get')
def test_method_dispatching_get_request_readonly(fake_get):
    """Test that calling client.get() results in a proper call
    to the get function in the requests module with the provided
    kwargs as the querystring.
    """
    client = everyplay.Client(client_id='foo')
    expected_url = '%s?%s' % (
        client._resolve_resource_name('videos'),
        urlencode({
            'order': 'popularity',
            'limit': 5,
            'client_id': 'foo'
        }))
    headers = {
        'User-Agent': everyplay.USER_AGENT
    }
    (fake_get.expects_call()
             .with_args(expected_url, headers=headers, allow_redirects=True)
             .returns(MockResponse("{}")))
    client.get('videos', order='popularity', limit=5)


@patch('requests.post')
def test_method_dispatching_post_request(fake_post):
    """Test that calling client.post() results in a proper call
    to the post function in the requests module.

    TODO: Revise once read/write support has been added.
    """
    client = everyplay.Client(client_id='foo')
    expected_url = client._resolve_resource_name('videos')
    data = {
        'client_id': 'foo'
    }
    headers = {
        'User-Agent': everyplay.USER_AGENT
    }
    (fake_post.expects_call()
              .with_args(expected_url,
                         data=data,
                         headers=headers,
                         allow_redirects=True)
              .returns(MockResponse("{}")))
    client.post('videos')


@patch('requests.get')
def test_proxy_servers(fake_request):
    """Test that providing a dictionary of proxy servers works."""
    proxies = {
        'http': 'myproxyserver:1234'
    }
    client = everyplay.Client(client_id='foo', proxies=proxies)
    expected_url = "%s?%s" % (
        client._resolve_resource_name('me'),
        urlencode({
            'client_id': 'foo'
        })
    )
    headers = {
        'User-Agent': everyplay.USER_AGENT
    }
    (fake_request.expects_call()
                 .with_args(expected_url,
                            headers=headers,
                            proxies=proxies,
                            allow_redirects=True)
                 .returns(MockResponse("{}")))
    client.get('/me')
