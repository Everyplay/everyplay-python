try:
    import json
except ImportError:
    import simplejson as json

from everyplay.resource import wrapped_resource, ResourceList, Resource
from everyplay.tests.utils import MockResponse

from nose.tools import eq_


def test_json_list():
    """Verify that a json list is wrapped in a ResourceList object."""
    resources = wrapped_resource(MockResponse(json.dumps([{'foo': 'bar'}])))
    assert isinstance(resources, ResourceList)
    eq_(1, len(resources))
    eq_('bar', resources[0].foo)


def test_json_object():
    """Verify that a json object is wrapped in a Resource object."""
    resource = wrapped_resource(MockResponse(json.dumps({'foo': 'bar'})))
    assert isinstance(resource, Resource)
    eq_('bar', resource.foo)


def test_properties_copied():
    """Certain properties should be copied to the wrapped resource."""
    response = MockResponse(json.dumps({'foo': 'bar'}),
                            status_code=200,
                            error='This is an error',
                            url='http://example.com')

    resource = wrapped_resource(response)
    eq_(200, resource.status_code)
    eq_('http://example.com', resource.url)
    response = MockResponse(json.dumps('This is an error'),
                            status_code=400,
                            error='This is an error',
                            url='http://example.com')

    resource = wrapped_resource(response)
    eq_(400, resource.status_code)
    eq_('"This is an error"', resource.error)
    eq_('http://example.com', resource.url)
