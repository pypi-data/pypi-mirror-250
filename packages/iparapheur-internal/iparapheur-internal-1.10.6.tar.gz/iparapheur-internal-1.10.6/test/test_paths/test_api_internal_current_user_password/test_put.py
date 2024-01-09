# coding: utf-8

"""


    Generated by: https://openapi-generator.tech
"""

import unittest
from unittest.mock import patch

import urllib3

import iparapheur_internal
from iparapheur_internal.paths.api_internal_current_user_password import put  # noqa: E501
from iparapheur_internal import configuration, schemas, api_client

from .. import ApiTestMixin


class TestApiInternalCurrentUserPassword(ApiTestMixin, unittest.TestCase):
    """
    ApiInternalCurrentUserPassword unit test stubs
        Update user password  # noqa: E501
    """
    _configuration = configuration.Configuration()

    def setUp(self):
        used_api_client = api_client.ApiClient(configuration=self._configuration)
        self.api = put.ApiForput(api_client=used_api_client)  # noqa: E501

    def tearDown(self):
        pass

    response_status = 404






if __name__ == '__main__':
    unittest.main()
