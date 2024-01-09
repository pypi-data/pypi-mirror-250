# coding: utf-8

"""


    Generated by: https://openapi-generator.tech
"""

import unittest
from unittest.mock import patch

import urllib3

import iparapheur_internal
from iparapheur_internal.paths.api_internal_admin_tenant_tenant_id_layer_layer_id import delete  # noqa: E501
from iparapheur_internal import configuration, schemas, api_client

from .. import ApiTestMixin


class TestApiInternalAdminTenantTenantIdLayerLayerId(ApiTestMixin, unittest.TestCase):
    """
    ApiInternalAdminTenantTenantIdLayerLayerId unit test stubs
        Delete layer  # noqa: E501
    """
    _configuration = configuration.Configuration()

    def setUp(self):
        used_api_client = api_client.ApiClient(configuration=self._configuration)
        self.api = delete.ApiFordelete(api_client=used_api_client)  # noqa: E501

    def tearDown(self):
        pass

    response_status = 204
    response_body = ''


if __name__ == '__main__':
    unittest.main()
