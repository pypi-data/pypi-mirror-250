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

from google.auth.transport.requests import AuthorizedSession  # type: ignore
import json  # type: ignore
import grpc  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore
from google.auth import credentials as ga_credentials  # type: ignore
from google.api_core import exceptions as core_exceptions
from google.api_core import retry as retries
from google.api_core import rest_helpers
from google.api_core import rest_streaming
from google.api_core import path_template
from google.api_core import gapic_v1

from google.protobuf import json_format
from requests import __version__ as requests_version
import dataclasses
import re
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple, Union
import warnings

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object]  # type: ignore


from google.cloud.orgpolicy_v2.types import constraint
from google.cloud.orgpolicy_v2.types import orgpolicy
from google.protobuf import empty_pb2  # type: ignore

from .base import OrgPolicyTransport, DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO


DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=BASE_DEFAULT_CLIENT_INFO.gapic_version,
    grpc_version=None,
    rest_version=requests_version,
)


class OrgPolicyRestInterceptor:
    """Interceptor for OrgPolicy.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the OrgPolicyRestTransport.

    .. code-block:: python
        class MyCustomOrgPolicyInterceptor(OrgPolicyRestInterceptor):
            def pre_create_custom_constraint(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_custom_constraint(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_policy(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_policy(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_custom_constraint(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_delete_policy(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_get_custom_constraint(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_custom_constraint(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_effective_policy(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_effective_policy(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_policy(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_policy(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_constraints(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_constraints(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_custom_constraints(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_custom_constraints(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_policies(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_policies(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_custom_constraint(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_custom_constraint(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_policy(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_policy(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = OrgPolicyRestTransport(interceptor=MyCustomOrgPolicyInterceptor())
        client = OrgPolicyClient(transport=transport)


    """

    def pre_create_custom_constraint(
        self,
        request: orgpolicy.CreateCustomConstraintRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[orgpolicy.CreateCustomConstraintRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_custom_constraint

        Override in a subclass to manipulate the request or metadata
        before they are sent to the OrgPolicy server.
        """
        return request, metadata

    def post_create_custom_constraint(
        self, response: constraint.CustomConstraint
    ) -> constraint.CustomConstraint:
        """Post-rpc interceptor for create_custom_constraint

        Override in a subclass to manipulate the response
        after it is returned by the OrgPolicy server but before
        it is returned to user code.
        """
        return response

    def pre_create_policy(
        self,
        request: orgpolicy.CreatePolicyRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[orgpolicy.CreatePolicyRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_policy

        Override in a subclass to manipulate the request or metadata
        before they are sent to the OrgPolicy server.
        """
        return request, metadata

    def post_create_policy(self, response: orgpolicy.Policy) -> orgpolicy.Policy:
        """Post-rpc interceptor for create_policy

        Override in a subclass to manipulate the response
        after it is returned by the OrgPolicy server but before
        it is returned to user code.
        """
        return response

    def pre_delete_custom_constraint(
        self,
        request: orgpolicy.DeleteCustomConstraintRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[orgpolicy.DeleteCustomConstraintRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_custom_constraint

        Override in a subclass to manipulate the request or metadata
        before they are sent to the OrgPolicy server.
        """
        return request, metadata

    def pre_delete_policy(
        self,
        request: orgpolicy.DeletePolicyRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[orgpolicy.DeletePolicyRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_policy

        Override in a subclass to manipulate the request or metadata
        before they are sent to the OrgPolicy server.
        """
        return request, metadata

    def pre_get_custom_constraint(
        self,
        request: orgpolicy.GetCustomConstraintRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[orgpolicy.GetCustomConstraintRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_custom_constraint

        Override in a subclass to manipulate the request or metadata
        before they are sent to the OrgPolicy server.
        """
        return request, metadata

    def post_get_custom_constraint(
        self, response: constraint.CustomConstraint
    ) -> constraint.CustomConstraint:
        """Post-rpc interceptor for get_custom_constraint

        Override in a subclass to manipulate the response
        after it is returned by the OrgPolicy server but before
        it is returned to user code.
        """
        return response

    def pre_get_effective_policy(
        self,
        request: orgpolicy.GetEffectivePolicyRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[orgpolicy.GetEffectivePolicyRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_effective_policy

        Override in a subclass to manipulate the request or metadata
        before they are sent to the OrgPolicy server.
        """
        return request, metadata

    def post_get_effective_policy(self, response: orgpolicy.Policy) -> orgpolicy.Policy:
        """Post-rpc interceptor for get_effective_policy

        Override in a subclass to manipulate the response
        after it is returned by the OrgPolicy server but before
        it is returned to user code.
        """
        return response

    def pre_get_policy(
        self, request: orgpolicy.GetPolicyRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[orgpolicy.GetPolicyRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_policy

        Override in a subclass to manipulate the request or metadata
        before they are sent to the OrgPolicy server.
        """
        return request, metadata

    def post_get_policy(self, response: orgpolicy.Policy) -> orgpolicy.Policy:
        """Post-rpc interceptor for get_policy

        Override in a subclass to manipulate the response
        after it is returned by the OrgPolicy server but before
        it is returned to user code.
        """
        return response

    def pre_list_constraints(
        self,
        request: orgpolicy.ListConstraintsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[orgpolicy.ListConstraintsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_constraints

        Override in a subclass to manipulate the request or metadata
        before they are sent to the OrgPolicy server.
        """
        return request, metadata

    def post_list_constraints(
        self, response: orgpolicy.ListConstraintsResponse
    ) -> orgpolicy.ListConstraintsResponse:
        """Post-rpc interceptor for list_constraints

        Override in a subclass to manipulate the response
        after it is returned by the OrgPolicy server but before
        it is returned to user code.
        """
        return response

    def pre_list_custom_constraints(
        self,
        request: orgpolicy.ListCustomConstraintsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[orgpolicy.ListCustomConstraintsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_custom_constraints

        Override in a subclass to manipulate the request or metadata
        before they are sent to the OrgPolicy server.
        """
        return request, metadata

    def post_list_custom_constraints(
        self, response: orgpolicy.ListCustomConstraintsResponse
    ) -> orgpolicy.ListCustomConstraintsResponse:
        """Post-rpc interceptor for list_custom_constraints

        Override in a subclass to manipulate the response
        after it is returned by the OrgPolicy server but before
        it is returned to user code.
        """
        return response

    def pre_list_policies(
        self,
        request: orgpolicy.ListPoliciesRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[orgpolicy.ListPoliciesRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_policies

        Override in a subclass to manipulate the request or metadata
        before they are sent to the OrgPolicy server.
        """
        return request, metadata

    def post_list_policies(
        self, response: orgpolicy.ListPoliciesResponse
    ) -> orgpolicy.ListPoliciesResponse:
        """Post-rpc interceptor for list_policies

        Override in a subclass to manipulate the response
        after it is returned by the OrgPolicy server but before
        it is returned to user code.
        """
        return response

    def pre_update_custom_constraint(
        self,
        request: orgpolicy.UpdateCustomConstraintRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[orgpolicy.UpdateCustomConstraintRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_custom_constraint

        Override in a subclass to manipulate the request or metadata
        before they are sent to the OrgPolicy server.
        """
        return request, metadata

    def post_update_custom_constraint(
        self, response: constraint.CustomConstraint
    ) -> constraint.CustomConstraint:
        """Post-rpc interceptor for update_custom_constraint

        Override in a subclass to manipulate the response
        after it is returned by the OrgPolicy server but before
        it is returned to user code.
        """
        return response

    def pre_update_policy(
        self,
        request: orgpolicy.UpdatePolicyRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[orgpolicy.UpdatePolicyRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_policy

        Override in a subclass to manipulate the request or metadata
        before they are sent to the OrgPolicy server.
        """
        return request, metadata

    def post_update_policy(self, response: orgpolicy.Policy) -> orgpolicy.Policy:
        """Post-rpc interceptor for update_policy

        Override in a subclass to manipulate the response
        after it is returned by the OrgPolicy server but before
        it is returned to user code.
        """
        return response


@dataclasses.dataclass
class OrgPolicyRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: OrgPolicyRestInterceptor


class OrgPolicyRestTransport(OrgPolicyTransport):
    """REST backend transport for OrgPolicy.

    An interface for managing organization policies.

    The Organization Policy Service provides a simple mechanism for
    organizations to restrict the allowed configurations across
    their entire resource hierarchy.

    You can use a policy to configure restrictions on resources. For
    example, you can enforce a policy that restricts which Google
    Cloud APIs can be activated in a certain part of your resource
    hierarchy, or prevents serial port access to VM instances in a
    particular folder.

    Policies are inherited down through the resource hierarchy. A
    policy applied to a parent resource automatically applies to all
    its child resources unless overridden with a policy lower in the
    hierarchy.

    A constraint defines an aspect of a resource's configuration
    that can be controlled by an organization's policy
    administrator. Policies are a collection of constraints that
    defines their allowable configuration on a particular resource
    and its child resources.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends JSON representations of protocol buffers over HTTP/1.1

    """

    def __init__(
        self,
        *,
        host: str = "orgpolicy.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        client_cert_source_for_mtls: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        url_scheme: str = "https",
        interceptor: Optional[OrgPolicyRestInterceptor] = None,
        api_audience: Optional[str] = None,
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
                This argument is ignored if ``channel`` is provided.
            scopes (Optional(Sequence[str])): A list of scopes. This argument is
                ignored if ``channel`` is provided.
            client_cert_source_for_mtls (Callable[[], Tuple[bytes, bytes]]): Client
                certificate to configure mutual TLS HTTP channel. It is ignored
                if ``channel`` is provided.
            quota_project_id (Optional[str]): An optional project to use for billing
                and quota.
            client_info (google.api_core.gapic_v1.client_info.ClientInfo):
                The client info used to send a user-agent string along with
                API requests. If ``None``, then default info will be used.
                Generally, you only need to set this if you are developing
                your own client library.
            always_use_jwt_access (Optional[bool]): Whether self signed JWT should
                be used for service account credentials.
            url_scheme: the protocol scheme for the API endpoint.  Normally
                "https", but for testing or local servers,
                "http" can be specified.
        """
        # Run the base constructor
        # TODO(yon-mg): resolve other ctor params i.e. scopes, quota, etc.
        # TODO: When custom host (api_endpoint) is set, `scopes` must *also* be set on the
        # credentials object
        maybe_url_match = re.match("^(?P<scheme>http(?:s)?://)?(?P<host>.*)$", host)
        if maybe_url_match is None:
            raise ValueError(
                f"Unexpected hostname structure: {host}"
            )  # pragma: NO COVER

        url_match_items = maybe_url_match.groupdict()

        host = f"{url_scheme}://{host}" if not url_match_items["scheme"] else host

        super().__init__(
            host=host,
            credentials=credentials,
            client_info=client_info,
            always_use_jwt_access=always_use_jwt_access,
            api_audience=api_audience,
        )
        self._session = AuthorizedSession(
            self._credentials, default_host=self.DEFAULT_HOST
        )
        if client_cert_source_for_mtls:
            self._session.configure_mtls_channel(client_cert_source_for_mtls)
        self._interceptor = interceptor or OrgPolicyRestInterceptor()
        self._prep_wrapped_messages(client_info)

    class _CreateCustomConstraint(OrgPolicyRestStub):
        def __hash__(self):
            return hash("CreateCustomConstraint")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: orgpolicy.CreateCustomConstraintRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> constraint.CustomConstraint:
            r"""Call the create custom constraint method over HTTP.

            Args:
                request (~.orgpolicy.CreateCustomConstraintRequest):
                    The request object. The request sent to the [CreateCustomConstraintRequest]
                [google.cloud.orgpolicy.v2.OrgPolicy.CreateCustomConstraint]
                method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.constraint.CustomConstraint:
                    A custom constraint defined by customers which can
                *only* be applied to the given resource types and
                organization.

                By creating a custom constraint, customers can apply
                policies of this custom constraint. *Creating a custom
                constraint itself does NOT apply any policy
                enforcement*.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v2/{parent=organizations/*}/customConstraints",
                    "body": "custom_constraint",
                },
            ]
            request, metadata = self._interceptor.pre_create_custom_constraint(
                request, metadata
            )
            pb_request = orgpolicy.CreateCustomConstraintRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"],
                including_default_value_fields=False,
                use_integers_for_enums=True,
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = constraint.CustomConstraint()
            pb_resp = constraint.CustomConstraint.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_custom_constraint(resp)
            return resp

    class _CreatePolicy(OrgPolicyRestStub):
        def __hash__(self):
            return hash("CreatePolicy")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: orgpolicy.CreatePolicyRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> orgpolicy.Policy:
            r"""Call the create policy method over HTTP.

            Args:
                request (~.orgpolicy.CreatePolicyRequest):
                    The request object. The request sent to the [CreatePolicyRequest]
                [google.cloud.orgpolicy.v2.OrgPolicy.CreatePolicy]
                method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.orgpolicy.Policy:
                    Defines an organization policy which
                is used to specify constraints for
                configurations of Google Cloud
                resources.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v2/{parent=projects/*}/policies",
                    "body": "policy",
                },
                {
                    "method": "post",
                    "uri": "/v2/{parent=folders/*}/policies",
                    "body": "policy",
                },
                {
                    "method": "post",
                    "uri": "/v2/{parent=organizations/*}/policies",
                    "body": "policy",
                },
            ]
            request, metadata = self._interceptor.pre_create_policy(request, metadata)
            pb_request = orgpolicy.CreatePolicyRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"],
                including_default_value_fields=False,
                use_integers_for_enums=True,
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = orgpolicy.Policy()
            pb_resp = orgpolicy.Policy.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_policy(resp)
            return resp

    class _DeleteCustomConstraint(OrgPolicyRestStub):
        def __hash__(self):
            return hash("DeleteCustomConstraint")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: orgpolicy.DeleteCustomConstraintRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ):
            r"""Call the delete custom constraint method over HTTP.

            Args:
                request (~.orgpolicy.DeleteCustomConstraintRequest):
                    The request object. The request sent to the [DeleteCustomConstraint]
                [google.cloud.orgpolicy.v2.OrgPolicy.DeleteCustomConstraint]
                method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "delete",
                    "uri": "/v2/{name=organizations/*/customConstraints/*}",
                },
            ]
            request, metadata = self._interceptor.pre_delete_custom_constraint(
                request, metadata
            )
            pb_request = orgpolicy.DeleteCustomConstraintRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

    class _DeletePolicy(OrgPolicyRestStub):
        def __hash__(self):
            return hash("DeletePolicy")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: orgpolicy.DeletePolicyRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ):
            r"""Call the delete policy method over HTTP.

            Args:
                request (~.orgpolicy.DeletePolicyRequest):
                    The request object. The request sent to the [DeletePolicy]
                [google.cloud.orgpolicy.v2.OrgPolicy.DeletePolicy]
                method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "delete",
                    "uri": "/v2/{name=projects/*/policies/*}",
                },
                {
                    "method": "delete",
                    "uri": "/v2/{name=folders/*/policies/*}",
                },
                {
                    "method": "delete",
                    "uri": "/v2/{name=organizations/*/policies/*}",
                },
            ]
            request, metadata = self._interceptor.pre_delete_policy(request, metadata)
            pb_request = orgpolicy.DeletePolicyRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

    class _GetCustomConstraint(OrgPolicyRestStub):
        def __hash__(self):
            return hash("GetCustomConstraint")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: orgpolicy.GetCustomConstraintRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> constraint.CustomConstraint:
            r"""Call the get custom constraint method over HTTP.

            Args:
                request (~.orgpolicy.GetCustomConstraintRequest):
                    The request object. The request sent to the [GetCustomConstraint]
                [google.cloud.orgpolicy.v2.OrgPolicy.GetCustomConstraint]
                method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.constraint.CustomConstraint:
                    A custom constraint defined by customers which can
                *only* be applied to the given resource types and
                organization.

                By creating a custom constraint, customers can apply
                policies of this custom constraint. *Creating a custom
                constraint itself does NOT apply any policy
                enforcement*.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v2/{name=organizations/*/customConstraints/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_custom_constraint(
                request, metadata
            )
            pb_request = orgpolicy.GetCustomConstraintRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = constraint.CustomConstraint()
            pb_resp = constraint.CustomConstraint.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_custom_constraint(resp)
            return resp

    class _GetEffectivePolicy(OrgPolicyRestStub):
        def __hash__(self):
            return hash("GetEffectivePolicy")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: orgpolicy.GetEffectivePolicyRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> orgpolicy.Policy:
            r"""Call the get effective policy method over HTTP.

            Args:
                request (~.orgpolicy.GetEffectivePolicyRequest):
                    The request object. The request sent to the [GetEffectivePolicy]
                [google.cloud.orgpolicy.v2.OrgPolicy.GetEffectivePolicy]
                method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.orgpolicy.Policy:
                    Defines an organization policy which
                is used to specify constraints for
                configurations of Google Cloud
                resources.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v2/{name=projects/*/policies/*}:getEffectivePolicy",
                },
                {
                    "method": "get",
                    "uri": "/v2/{name=folders/*/policies/*}:getEffectivePolicy",
                },
                {
                    "method": "get",
                    "uri": "/v2/{name=organizations/*/policies/*}:getEffectivePolicy",
                },
            ]
            request, metadata = self._interceptor.pre_get_effective_policy(
                request, metadata
            )
            pb_request = orgpolicy.GetEffectivePolicyRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = orgpolicy.Policy()
            pb_resp = orgpolicy.Policy.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_effective_policy(resp)
            return resp

    class _GetPolicy(OrgPolicyRestStub):
        def __hash__(self):
            return hash("GetPolicy")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: orgpolicy.GetPolicyRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> orgpolicy.Policy:
            r"""Call the get policy method over HTTP.

            Args:
                request (~.orgpolicy.GetPolicyRequest):
                    The request object. The request sent to the [GetPolicy]
                [google.cloud.orgpolicy.v2.OrgPolicy.GetPolicy] method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.orgpolicy.Policy:
                    Defines an organization policy which
                is used to specify constraints for
                configurations of Google Cloud
                resources.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v2/{name=projects/*/policies/*}",
                },
                {
                    "method": "get",
                    "uri": "/v2/{name=folders/*/policies/*}",
                },
                {
                    "method": "get",
                    "uri": "/v2/{name=organizations/*/policies/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_policy(request, metadata)
            pb_request = orgpolicy.GetPolicyRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = orgpolicy.Policy()
            pb_resp = orgpolicy.Policy.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_policy(resp)
            return resp

    class _ListConstraints(OrgPolicyRestStub):
        def __hash__(self):
            return hash("ListConstraints")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: orgpolicy.ListConstraintsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> orgpolicy.ListConstraintsResponse:
            r"""Call the list constraints method over HTTP.

            Args:
                request (~.orgpolicy.ListConstraintsRequest):
                    The request object. The request sent to the [ListConstraints]
                [google.cloud.orgpolicy.v2.OrgPolicy.ListConstraints]
                method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.orgpolicy.ListConstraintsResponse:
                    The response returned from the [ListConstraints]
                [google.cloud.orgpolicy.v2.OrgPolicy.ListConstraints]
                method.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v2/{parent=projects/*}/constraints",
                },
                {
                    "method": "get",
                    "uri": "/v2/{parent=folders/*}/constraints",
                },
                {
                    "method": "get",
                    "uri": "/v2/{parent=organizations/*}/constraints",
                },
            ]
            request, metadata = self._interceptor.pre_list_constraints(
                request, metadata
            )
            pb_request = orgpolicy.ListConstraintsRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = orgpolicy.ListConstraintsResponse()
            pb_resp = orgpolicy.ListConstraintsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_constraints(resp)
            return resp

    class _ListCustomConstraints(OrgPolicyRestStub):
        def __hash__(self):
            return hash("ListCustomConstraints")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: orgpolicy.ListCustomConstraintsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> orgpolicy.ListCustomConstraintsResponse:
            r"""Call the list custom constraints method over HTTP.

            Args:
                request (~.orgpolicy.ListCustomConstraintsRequest):
                    The request object. The request sent to the [ListCustomConstraints]
                [google.cloud.orgpolicy.v2.OrgPolicy.ListCustomConstraints]
                method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.orgpolicy.ListCustomConstraintsResponse:
                    The response returned from the [ListCustomConstraints]
                [google.cloud.orgpolicy.v2.OrgPolicy.ListCustomConstraints]
                method. It will be empty if no custom constraints are
                set on the organization resource.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v2/{parent=organizations/*}/customConstraints",
                },
            ]
            request, metadata = self._interceptor.pre_list_custom_constraints(
                request, metadata
            )
            pb_request = orgpolicy.ListCustomConstraintsRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = orgpolicy.ListCustomConstraintsResponse()
            pb_resp = orgpolicy.ListCustomConstraintsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_custom_constraints(resp)
            return resp

    class _ListPolicies(OrgPolicyRestStub):
        def __hash__(self):
            return hash("ListPolicies")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: orgpolicy.ListPoliciesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> orgpolicy.ListPoliciesResponse:
            r"""Call the list policies method over HTTP.

            Args:
                request (~.orgpolicy.ListPoliciesRequest):
                    The request object. The request sent to the [ListPolicies]
                [google.cloud.orgpolicy.v2.OrgPolicy.ListPolicies]
                method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.orgpolicy.ListPoliciesResponse:
                    The response returned from the [ListPolicies]
                [google.cloud.orgpolicy.v2.OrgPolicy.ListPolicies]
                method. It will be empty if no policies are set on the
                resource.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v2/{parent=projects/*}/policies",
                },
                {
                    "method": "get",
                    "uri": "/v2/{parent=folders/*}/policies",
                },
                {
                    "method": "get",
                    "uri": "/v2/{parent=organizations/*}/policies",
                },
            ]
            request, metadata = self._interceptor.pre_list_policies(request, metadata)
            pb_request = orgpolicy.ListPoliciesRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = orgpolicy.ListPoliciesResponse()
            pb_resp = orgpolicy.ListPoliciesResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_policies(resp)
            return resp

    class _UpdateCustomConstraint(OrgPolicyRestStub):
        def __hash__(self):
            return hash("UpdateCustomConstraint")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: orgpolicy.UpdateCustomConstraintRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> constraint.CustomConstraint:
            r"""Call the update custom constraint method over HTTP.

            Args:
                request (~.orgpolicy.UpdateCustomConstraintRequest):
                    The request object. The request sent to the [UpdateCustomConstraintRequest]
                [google.cloud.orgpolicy.v2.OrgPolicy.UpdateCustomConstraint]
                method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.constraint.CustomConstraint:
                    A custom constraint defined by customers which can
                *only* be applied to the given resource types and
                organization.

                By creating a custom constraint, customers can apply
                policies of this custom constraint. *Creating a custom
                constraint itself does NOT apply any policy
                enforcement*.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "patch",
                    "uri": "/v2/{custom_constraint.name=organizations/*/customConstraints/*}",
                    "body": "custom_constraint",
                },
            ]
            request, metadata = self._interceptor.pre_update_custom_constraint(
                request, metadata
            )
            pb_request = orgpolicy.UpdateCustomConstraintRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"],
                including_default_value_fields=False,
                use_integers_for_enums=True,
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = constraint.CustomConstraint()
            pb_resp = constraint.CustomConstraint.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_custom_constraint(resp)
            return resp

    class _UpdatePolicy(OrgPolicyRestStub):
        def __hash__(self):
            return hash("UpdatePolicy")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: orgpolicy.UpdatePolicyRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> orgpolicy.Policy:
            r"""Call the update policy method over HTTP.

            Args:
                request (~.orgpolicy.UpdatePolicyRequest):
                    The request object. The request sent to the [UpdatePolicyRequest]
                [google.cloud.orgpolicy.v2.OrgPolicy.UpdatePolicy]
                method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.orgpolicy.Policy:
                    Defines an organization policy which
                is used to specify constraints for
                configurations of Google Cloud
                resources.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "patch",
                    "uri": "/v2/{policy.name=projects/*/policies/*}",
                    "body": "policy",
                },
                {
                    "method": "patch",
                    "uri": "/v2/{policy.name=folders/*/policies/*}",
                    "body": "policy",
                },
                {
                    "method": "patch",
                    "uri": "/v2/{policy.name=organizations/*/policies/*}",
                    "body": "policy",
                },
            ]
            request, metadata = self._interceptor.pre_update_policy(request, metadata)
            pb_request = orgpolicy.UpdatePolicyRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"],
                including_default_value_fields=False,
                use_integers_for_enums=True,
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = orgpolicy.Policy()
            pb_resp = orgpolicy.Policy.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_policy(resp)
            return resp

    @property
    def create_custom_constraint(
        self,
    ) -> Callable[
        [orgpolicy.CreateCustomConstraintRequest], constraint.CustomConstraint
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateCustomConstraint(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_policy(
        self,
    ) -> Callable[[orgpolicy.CreatePolicyRequest], orgpolicy.Policy]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreatePolicy(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_custom_constraint(
        self,
    ) -> Callable[[orgpolicy.DeleteCustomConstraintRequest], empty_pb2.Empty]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteCustomConstraint(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_policy(
        self,
    ) -> Callable[[orgpolicy.DeletePolicyRequest], empty_pb2.Empty]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeletePolicy(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_custom_constraint(
        self,
    ) -> Callable[[orgpolicy.GetCustomConstraintRequest], constraint.CustomConstraint]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetCustomConstraint(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_effective_policy(
        self,
    ) -> Callable[[orgpolicy.GetEffectivePolicyRequest], orgpolicy.Policy]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetEffectivePolicy(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_policy(self) -> Callable[[orgpolicy.GetPolicyRequest], orgpolicy.Policy]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetPolicy(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_constraints(
        self,
    ) -> Callable[
        [orgpolicy.ListConstraintsRequest], orgpolicy.ListConstraintsResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListConstraints(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_custom_constraints(
        self,
    ) -> Callable[
        [orgpolicy.ListCustomConstraintsRequest],
        orgpolicy.ListCustomConstraintsResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListCustomConstraints(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_policies(
        self,
    ) -> Callable[[orgpolicy.ListPoliciesRequest], orgpolicy.ListPoliciesResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListPolicies(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_custom_constraint(
        self,
    ) -> Callable[
        [orgpolicy.UpdateCustomConstraintRequest], constraint.CustomConstraint
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateCustomConstraint(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_policy(
        self,
    ) -> Callable[[orgpolicy.UpdatePolicyRequest], orgpolicy.Policy]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdatePolicy(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def kind(self) -> str:
        return "rest"

    def close(self):
        self._session.close()


__all__ = ("OrgPolicyRestTransport",)
