# coding: utf-8

"""


    Generated by: https://openapi-generator.tech
"""

import unittest
from unittest.mock import patch

import urllib3

import iparapheur_provisioning
from iparapheur_provisioning.paths.api_provisioning_v1_admin_tenant import get  # noqa: E501
from iparapheur_provisioning import configuration, schemas, api_client

from .. import ApiTestMixin


class TestApiProvisioningV1AdminTenant(ApiTestMixin, unittest.TestCase):
    """
    ApiProvisioningV1AdminTenant unit test stubs
        List tenants  # noqa: E501
    """
    _configuration = configuration.Configuration()

    def setUp(self):
        used_api_client = api_client.ApiClient(configuration=self._configuration)
        self.api = get.ApiForget(api_client=used_api_client)  # noqa: E501

    def tearDown(self):
        pass

    response_status = 200




if __name__ == '__main__':
    unittest.main()
