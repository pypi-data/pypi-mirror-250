# -*- coding: utf-8 -*-
# Copyright 2023 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import abc
from typing import Awaitable, Callable, Dict, Optional, Sequence, Union

import google.api_core
from google.api_core import exceptions as core_exceptions
from google.api_core import gapic_v1
from google.api_core import retry as retries
import google.auth  # type: ignore
from google.auth import credentials as ga_credentials  # type: ignore
from google.iam.v1 import iam_policy_pb2  # type: ignore
from google.iam.v1 import policy_pb2  # type: ignore
from google.longrunning import operations_pb2  # type: ignore
from google.oauth2 import service_account  # type: ignore
from google.protobuf import empty_pb2  # type: ignore

from google.cloud.datacatalog_v1 import gapic_version as package_version
from google.cloud.datacatalog_v1.types import policytagmanager

DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=package_version.__version__
)


class PolicyTagManagerTransport(abc.ABC):
    """Abstract transport class for PolicyTagManager."""

    AUTH_SCOPES = ("https://www.googleapis.com/auth/cloud-platform",)

    DEFAULT_HOST: str = "datacatalog.googleapis.com"

    def __init__(
        self,
        *,
        host: str = DEFAULT_HOST,
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        api_audience: Optional[str] = None,
        **kwargs,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]):
                 The hostname to connect to.
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            credentials_file (Optional[str]): A file with credentials that can
                be loaded with :func:`google.auth.load_credentials_from_file`.
                This argument is mutually exclusive with credentials.
            scopes (Optional[Sequence[str]]): A list of scopes.
            quota_project_id (Optional[str]): An optional project to use for billing
                and quota.
            client_info (google.api_core.gapic_v1.client_info.ClientInfo):
                The client info used to send a user-agent string along with
                API requests. If ``None``, then default info will be used.
                Generally, you only need to set this if you're developing
                your own client library.
            always_use_jwt_access (Optional[bool]): Whether self signed JWT should
                be used for service account credentials.
        """

        scopes_kwargs = {"scopes": scopes, "default_scopes": self.AUTH_SCOPES}

        # Save the scopes.
        self._scopes = scopes

        # If no credentials are provided, then determine the appropriate
        # defaults.
        if credentials and credentials_file:
            raise core_exceptions.DuplicateCredentialArgs(
                "'credentials_file' and 'credentials' are mutually exclusive"
            )

        if credentials_file is not None:
            credentials, _ = google.auth.load_credentials_from_file(
                credentials_file, **scopes_kwargs, quota_project_id=quota_project_id
            )
        elif credentials is None:
            credentials, _ = google.auth.default(
                **scopes_kwargs, quota_project_id=quota_project_id
            )
            # Don't apply audience if the credentials file passed from user.
            if hasattr(credentials, "with_gdch_audience"):
                credentials = credentials.with_gdch_audience(
                    api_audience if api_audience else host
                )

        # If the credentials are service account credentials, then always try to use self signed JWT.
        if (
            always_use_jwt_access
            and isinstance(credentials, service_account.Credentials)
            and hasattr(service_account.Credentials, "with_always_use_jwt_access")
        ):
            credentials = credentials.with_always_use_jwt_access(True)

        # Save the credentials.
        self._credentials = credentials

        # Save the hostname. Default to port 443 (HTTPS) if none is specified.
        if ":" not in host:
            host += ":443"
        self._host = host

    def _prep_wrapped_messages(self, client_info):
        # Precompute the wrapped methods.
        self._wrapped_methods = {
            self.create_taxonomy: gapic_v1.method.wrap_method(
                self.create_taxonomy,
                default_timeout=None,
                client_info=client_info,
            ),
            self.delete_taxonomy: gapic_v1.method.wrap_method(
                self.delete_taxonomy,
                default_timeout=None,
                client_info=client_info,
            ),
            self.update_taxonomy: gapic_v1.method.wrap_method(
                self.update_taxonomy,
                default_timeout=None,
                client_info=client_info,
            ),
            self.list_taxonomies: gapic_v1.method.wrap_method(
                self.list_taxonomies,
                default_timeout=None,
                client_info=client_info,
            ),
            self.get_taxonomy: gapic_v1.method.wrap_method(
                self.get_taxonomy,
                default_timeout=None,
                client_info=client_info,
            ),
            self.create_policy_tag: gapic_v1.method.wrap_method(
                self.create_policy_tag,
                default_timeout=None,
                client_info=client_info,
            ),
            self.delete_policy_tag: gapic_v1.method.wrap_method(
                self.delete_policy_tag,
                default_timeout=None,
                client_info=client_info,
            ),
            self.update_policy_tag: gapic_v1.method.wrap_method(
                self.update_policy_tag,
                default_timeout=None,
                client_info=client_info,
            ),
            self.list_policy_tags: gapic_v1.method.wrap_method(
                self.list_policy_tags,
                default_timeout=None,
                client_info=client_info,
            ),
            self.get_policy_tag: gapic_v1.method.wrap_method(
                self.get_policy_tag,
                default_timeout=None,
                client_info=client_info,
            ),
            self.get_iam_policy: gapic_v1.method.wrap_method(
                self.get_iam_policy,
                default_timeout=None,
                client_info=client_info,
            ),
            self.set_iam_policy: gapic_v1.method.wrap_method(
                self.set_iam_policy,
                default_timeout=None,
                client_info=client_info,
            ),
            self.test_iam_permissions: gapic_v1.method.wrap_method(
                self.test_iam_permissions,
                default_timeout=None,
                client_info=client_info,
            ),
        }

    def close(self):
        """Closes resources associated with the transport.

        .. warning::
             Only call this method if the transport is NOT shared
             with other clients - this may cause errors in other clients!
        """
        raise NotImplementedError()

    @property
    def create_taxonomy(
        self,
    ) -> Callable[
        [policytagmanager.CreateTaxonomyRequest],
        Union[policytagmanager.Taxonomy, Awaitable[policytagmanager.Taxonomy]],
    ]:
        raise NotImplementedError()

    @property
    def delete_taxonomy(
        self,
    ) -> Callable[
        [policytagmanager.DeleteTaxonomyRequest],
        Union[empty_pb2.Empty, Awaitable[empty_pb2.Empty]],
    ]:
        raise NotImplementedError()

    @property
    def update_taxonomy(
        self,
    ) -> Callable[
        [policytagmanager.UpdateTaxonomyRequest],
        Union[policytagmanager.Taxonomy, Awaitable[policytagmanager.Taxonomy]],
    ]:
        raise NotImplementedError()

    @property
    def list_taxonomies(
        self,
    ) -> Callable[
        [policytagmanager.ListTaxonomiesRequest],
        Union[
            policytagmanager.ListTaxonomiesResponse,
            Awaitable[policytagmanager.ListTaxonomiesResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def get_taxonomy(
        self,
    ) -> Callable[
        [policytagmanager.GetTaxonomyRequest],
        Union[policytagmanager.Taxonomy, Awaitable[policytagmanager.Taxonomy]],
    ]:
        raise NotImplementedError()

    @property
    def create_policy_tag(
        self,
    ) -> Callable[
        [policytagmanager.CreatePolicyTagRequest],
        Union[policytagmanager.PolicyTag, Awaitable[policytagmanager.PolicyTag]],
    ]:
        raise NotImplementedError()

    @property
    def delete_policy_tag(
        self,
    ) -> Callable[
        [policytagmanager.DeletePolicyTagRequest],
        Union[empty_pb2.Empty, Awaitable[empty_pb2.Empty]],
    ]:
        raise NotImplementedError()

    @property
    def update_policy_tag(
        self,
    ) -> Callable[
        [policytagmanager.UpdatePolicyTagRequest],
        Union[policytagmanager.PolicyTag, Awaitable[policytagmanager.PolicyTag]],
    ]:
        raise NotImplementedError()

    @property
    def list_policy_tags(
        self,
    ) -> Callable[
        [policytagmanager.ListPolicyTagsRequest],
        Union[
            policytagmanager.ListPolicyTagsResponse,
            Awaitable[policytagmanager.ListPolicyTagsResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def get_policy_tag(
        self,
    ) -> Callable[
        [policytagmanager.GetPolicyTagRequest],
        Union[policytagmanager.PolicyTag, Awaitable[policytagmanager.PolicyTag]],
    ]:
        raise NotImplementedError()

    @property
    def get_iam_policy(
        self,
    ) -> Callable[
        [iam_policy_pb2.GetIamPolicyRequest],
        Union[policy_pb2.Policy, Awaitable[policy_pb2.Policy]],
    ]:
        raise NotImplementedError()

    @property
    def set_iam_policy(
        self,
    ) -> Callable[
        [iam_policy_pb2.SetIamPolicyRequest],
        Union[policy_pb2.Policy, Awaitable[policy_pb2.Policy]],
    ]:
        raise NotImplementedError()

    @property
    def test_iam_permissions(
        self,
    ) -> Callable[
        [iam_policy_pb2.TestIamPermissionsRequest],
        Union[
            iam_policy_pb2.TestIamPermissionsResponse,
            Awaitable[iam_policy_pb2.TestIamPermissionsResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def list_operations(
        self,
    ) -> Callable[
        [operations_pb2.ListOperationsRequest],
        Union[
            operations_pb2.ListOperationsResponse,
            Awaitable[operations_pb2.ListOperationsResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def get_operation(
        self,
    ) -> Callable[
        [operations_pb2.GetOperationRequest],
        Union[operations_pb2.Operation, Awaitable[operations_pb2.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def cancel_operation(
        self,
    ) -> Callable[[operations_pb2.CancelOperationRequest], None,]:
        raise NotImplementedError()

    @property
    def delete_operation(
        self,
    ) -> Callable[[operations_pb2.DeleteOperationRequest], None,]:
        raise NotImplementedError()

    @property
    def kind(self) -> str:
        raise NotImplementedError()


__all__ = ("PolicyTagManagerTransport",)
