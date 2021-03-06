import json
import os
import unittest

from multidimensional_urlencode import urlencode

from google.appengine.api import apiproxy_stub_map
from google.appengine.api import urlfetch_stub
from google.appengine.ext import testbed

from gae_discourse_client import discourse_client


class DiscourseCategoryTestCase(unittest.TestCase):
    def setUp(self):
        super(DiscourseCategoryTestCase, self).setUp()

        apiproxy_stub_map.apiproxy = apiproxy_stub_map.APIProxyStubMap()
        apiproxy_stub_map.apiproxy.RegisterStub(
            'urlfetch', urlfetch_stub.URLFetchServiceStub())

        discourse_client.initClient(
            os.environ['DISCOURSE_URL'],
            os.environ['DISCOURSE_API_KEY'],
            'system'
        )

    def testDeleteCategory(self):
        discourse_client.categories.create(
            category_name='Broncos',
            slug='broncos'
        ).get_result()

        response = discourse_client.categories.delete('Broncos').get_result()

        self.assertEqual('OK', response['success'])

    def testCreateCategory(self):
        discourse_client.categories.delete('Broncos').get_result()

        response = discourse_client.categories.create(
            category_name='Broncos',
            slug='broncos'
        ).get_result()

        self.assertTrue(response['category'] is not None)

    def testGetCategoryByName(self):
        response = discourse_client.categories.create(
            category_name='Broncos',
            slug='broncos'
        ).get_result()

        response = discourse_client.categories.getByName('Broncos').get_result()

        self.assertEqual('Broncos', response['name'])
