# coding: utf-8

"""


    Generated by: https://openapi-generator.tech
"""

import unittest
from unittest.mock import patch

import urllib3

import iparapheur_provisioning
from iparapheur_provisioning.paths.api_provisioning_v1_admin_tenant_tenant_id_seal_certificate import post  # noqa: E501
from iparapheur_provisioning import configuration, schemas, api_client

from .. import ApiTestMixin


class TestApiProvisioningV1AdminTenantTenantIdSealCertificate(ApiTestMixin, unittest.TestCase):
    """
    ApiProvisioningV1AdminTenantTenantIdSealCertificate unit test stubs
        Create a seal certificate  # noqa: E501
    """
    _configuration = configuration.Configuration()

    def setUp(self):
        used_api_client = api_client.ApiClient(configuration=self._configuration)
        self.api = post.ApiForpost(api_client=used_api_client)  # noqa: E501

    def tearDown(self):
        pass

    response_status = 400




if __name__ == '__main__':
    unittest.main()
