# coding: utf-8

"""
    iparapheur

    iparapheur v5.x main core application.  The main link between every sub-services, integrating business code logic.   # noqa: E501

    The version of the OpenAPI document: DEVELOP
    Contact: iparapheur@libriciel.coop
    Generated by: https://openapi-generator.tech
"""

from iparapheur_provisioning.paths.api_provisioning_v1_admin_tenant.post import CreateTenant
from iparapheur_provisioning.paths.api_provisioning_v1_admin_tenant_tenant_id.delete import DeleteTenant
from iparapheur_provisioning.paths.api_provisioning_v1_admin_tenant_tenant_id.get import GetTenant
from iparapheur_provisioning.paths.api_provisioning_v1_admin_tenant.get import ListTenants
from iparapheur_provisioning.paths.api_provisioning_v1_admin_tenant_tenant_id.put import UpdateTenant


class AdminTenantApi(
    CreateTenant,
    DeleteTenant,
    GetTenant,
    ListTenants,
    UpdateTenant,
):
    """NOTE: This class is auto generated by OpenAPI Generator
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """
    pass
