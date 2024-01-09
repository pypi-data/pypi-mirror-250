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
import os

# try/except added for compatibility with python < 3.8
try:
    from unittest import mock
    from unittest.mock import AsyncMock  # pragma: NO COVER
except ImportError:  # pragma: NO COVER
    import mock

import grpc
from grpc.experimental import aio
from collections.abc import Iterable
from google.protobuf import json_format
import json
import math
import pytest
from proto.marshal.rules.dates import DurationRule, TimestampRule
from proto.marshal.rules import wrappers
from requests import Response
from requests import Request, PreparedRequest
from requests.sessions import Session
from google.protobuf import json_format

from google.api_core import client_options
from google.api_core import exceptions as core_exceptions
from google.api_core import gapic_v1
from google.api_core import grpc_helpers
from google.api_core import grpc_helpers_async
from google.api_core import path_template
from google.auth import credentials as ga_credentials
from google.auth.exceptions import MutualTLSChannelError
from google.cloud.orgpolicy_v2.services.org_policy import OrgPolicyAsyncClient
from google.cloud.orgpolicy_v2.services.org_policy import OrgPolicyClient
from google.cloud.orgpolicy_v2.services.org_policy import pagers
from google.cloud.orgpolicy_v2.services.org_policy import transports
from google.cloud.orgpolicy_v2.types import constraint
from google.cloud.orgpolicy_v2.types import orgpolicy
from google.oauth2 import service_account
from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore
from google.type import expr_pb2  # type: ignore
import google.auth


def client_cert_source_callback():
    return b"cert bytes", b"key bytes"


# If default endpoint is localhost, then default mtls endpoint will be the same.
# This method modifies the default endpoint so the client can produce a different
# mtls endpoint for endpoint testing purposes.
def modify_default_endpoint(client):
    return (
        "foo.googleapis.com"
        if ("localhost" in client.DEFAULT_ENDPOINT)
        else client.DEFAULT_ENDPOINT
    )


def test__get_default_mtls_endpoint():
    api_endpoint = "example.googleapis.com"
    api_mtls_endpoint = "example.mtls.googleapis.com"
    sandbox_endpoint = "example.sandbox.googleapis.com"
    sandbox_mtls_endpoint = "example.mtls.sandbox.googleapis.com"
    non_googleapi = "api.example.com"

    assert OrgPolicyClient._get_default_mtls_endpoint(None) is None
    assert OrgPolicyClient._get_default_mtls_endpoint(api_endpoint) == api_mtls_endpoint
    assert (
        OrgPolicyClient._get_default_mtls_endpoint(api_mtls_endpoint)
        == api_mtls_endpoint
    )
    assert (
        OrgPolicyClient._get_default_mtls_endpoint(sandbox_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        OrgPolicyClient._get_default_mtls_endpoint(sandbox_mtls_endpoint)
        == sandbox_mtls_endpoint
    )
    assert OrgPolicyClient._get_default_mtls_endpoint(non_googleapi) == non_googleapi


@pytest.mark.parametrize(
    "client_class,transport_name",
    [
        (OrgPolicyClient, "grpc"),
        (OrgPolicyAsyncClient, "grpc_asyncio"),
        (OrgPolicyClient, "rest"),
    ],
)
def test_org_policy_client_from_service_account_info(client_class, transport_name):
    creds = ga_credentials.AnonymousCredentials()
    with mock.patch.object(
        service_account.Credentials, "from_service_account_info"
    ) as factory:
        factory.return_value = creds
        info = {"valid": True}
        client = client_class.from_service_account_info(info, transport=transport_name)
        assert client.transport._credentials == creds
        assert isinstance(client, client_class)

        assert client.transport._host == (
            "orgpolicy.googleapis.com:443"
            if transport_name in ["grpc", "grpc_asyncio"]
            else "https://orgpolicy.googleapis.com"
        )


@pytest.mark.parametrize(
    "transport_class,transport_name",
    [
        (transports.OrgPolicyGrpcTransport, "grpc"),
        (transports.OrgPolicyGrpcAsyncIOTransport, "grpc_asyncio"),
        (transports.OrgPolicyRestTransport, "rest"),
    ],
)
def test_org_policy_client_service_account_always_use_jwt(
    transport_class, transport_name
):
    with mock.patch.object(
        service_account.Credentials, "with_always_use_jwt_access", create=True
    ) as use_jwt:
        creds = service_account.Credentials(None, None, None)
        transport = transport_class(credentials=creds, always_use_jwt_access=True)
        use_jwt.assert_called_once_with(True)

    with mock.patch.object(
        service_account.Credentials, "with_always_use_jwt_access", create=True
    ) as use_jwt:
        creds = service_account.Credentials(None, None, None)
        transport = transport_class(credentials=creds, always_use_jwt_access=False)
        use_jwt.assert_not_called()


@pytest.mark.parametrize(
    "client_class,transport_name",
    [
        (OrgPolicyClient, "grpc"),
        (OrgPolicyAsyncClient, "grpc_asyncio"),
        (OrgPolicyClient, "rest"),
    ],
)
def test_org_policy_client_from_service_account_file(client_class, transport_name):
    creds = ga_credentials.AnonymousCredentials()
    with mock.patch.object(
        service_account.Credentials, "from_service_account_file"
    ) as factory:
        factory.return_value = creds
        client = client_class.from_service_account_file(
            "dummy/file/path.json", transport=transport_name
        )
        assert client.transport._credentials == creds
        assert isinstance(client, client_class)

        client = client_class.from_service_account_json(
            "dummy/file/path.json", transport=transport_name
        )
        assert client.transport._credentials == creds
        assert isinstance(client, client_class)

        assert client.transport._host == (
            "orgpolicy.googleapis.com:443"
            if transport_name in ["grpc", "grpc_asyncio"]
            else "https://orgpolicy.googleapis.com"
        )


def test_org_policy_client_get_transport_class():
    transport = OrgPolicyClient.get_transport_class()
    available_transports = [
        transports.OrgPolicyGrpcTransport,
        transports.OrgPolicyRestTransport,
    ]
    assert transport in available_transports

    transport = OrgPolicyClient.get_transport_class("grpc")
    assert transport == transports.OrgPolicyGrpcTransport


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (OrgPolicyClient, transports.OrgPolicyGrpcTransport, "grpc"),
        (
            OrgPolicyAsyncClient,
            transports.OrgPolicyGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
        (OrgPolicyClient, transports.OrgPolicyRestTransport, "rest"),
    ],
)
@mock.patch.object(
    OrgPolicyClient, "DEFAULT_ENDPOINT", modify_default_endpoint(OrgPolicyClient)
)
@mock.patch.object(
    OrgPolicyAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(OrgPolicyAsyncClient),
)
def test_org_policy_client_client_options(
    client_class, transport_class, transport_name
):
    # Check that if channel is provided we won't create a new one.
    with mock.patch.object(OrgPolicyClient, "get_transport_class") as gtc:
        transport = transport_class(credentials=ga_credentials.AnonymousCredentials())
        client = client_class(transport=transport)
        gtc.assert_not_called()

    # Check that if channel is provided via str we will create a new one.
    with mock.patch.object(OrgPolicyClient, "get_transport_class") as gtc:
        client = client_class(transport=transport_name)
        gtc.assert_called()

    # Check the case api_endpoint is provided.
    options = client_options.ClientOptions(api_endpoint="squid.clam.whelk")
    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(transport=transport_name, client_options=options)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host="squid.clam.whelk",
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
            api_audience=None,
        )

    # Check the case api_endpoint is not provided and GOOGLE_API_USE_MTLS_ENDPOINT is
    # "never".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "never"}):
        with mock.patch.object(transport_class, "__init__") as patched:
            patched.return_value = None
            client = client_class(transport=transport_name)
            patched.assert_called_once_with(
                credentials=None,
                credentials_file=None,
                host=client.DEFAULT_ENDPOINT,
                scopes=None,
                client_cert_source_for_mtls=None,
                quota_project_id=None,
                client_info=transports.base.DEFAULT_CLIENT_INFO,
                always_use_jwt_access=True,
                api_audience=None,
            )

    # Check the case api_endpoint is not provided and GOOGLE_API_USE_MTLS_ENDPOINT is
    # "always".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "always"}):
        with mock.patch.object(transport_class, "__init__") as patched:
            patched.return_value = None
            client = client_class(transport=transport_name)
            patched.assert_called_once_with(
                credentials=None,
                credentials_file=None,
                host=client.DEFAULT_MTLS_ENDPOINT,
                scopes=None,
                client_cert_source_for_mtls=None,
                quota_project_id=None,
                client_info=transports.base.DEFAULT_CLIENT_INFO,
                always_use_jwt_access=True,
                api_audience=None,
            )

    # Check the case api_endpoint is not provided and GOOGLE_API_USE_MTLS_ENDPOINT has
    # unsupported value.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "Unsupported"}):
        with pytest.raises(MutualTLSChannelError):
            client = client_class(transport=transport_name)

    # Check the case GOOGLE_API_USE_CLIENT_CERTIFICATE has unsupported value.
    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "Unsupported"}
    ):
        with pytest.raises(ValueError):
            client = client_class(transport=transport_name)

    # Check the case quota_project_id is provided
    options = client_options.ClientOptions(quota_project_id="octopus")
    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options, transport=transport_name)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host=client.DEFAULT_ENDPOINT,
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id="octopus",
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
            api_audience=None,
        )
    # Check the case api_endpoint is provided
    options = client_options.ClientOptions(
        api_audience="https://language.googleapis.com"
    )
    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options, transport=transport_name)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host=client.DEFAULT_ENDPOINT,
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
            api_audience="https://language.googleapis.com",
        )


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name,use_client_cert_env",
    [
        (OrgPolicyClient, transports.OrgPolicyGrpcTransport, "grpc", "true"),
        (
            OrgPolicyAsyncClient,
            transports.OrgPolicyGrpcAsyncIOTransport,
            "grpc_asyncio",
            "true",
        ),
        (OrgPolicyClient, transports.OrgPolicyGrpcTransport, "grpc", "false"),
        (
            OrgPolicyAsyncClient,
            transports.OrgPolicyGrpcAsyncIOTransport,
            "grpc_asyncio",
            "false",
        ),
        (OrgPolicyClient, transports.OrgPolicyRestTransport, "rest", "true"),
        (OrgPolicyClient, transports.OrgPolicyRestTransport, "rest", "false"),
    ],
)
@mock.patch.object(
    OrgPolicyClient, "DEFAULT_ENDPOINT", modify_default_endpoint(OrgPolicyClient)
)
@mock.patch.object(
    OrgPolicyAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(OrgPolicyAsyncClient),
)
@mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "auto"})
def test_org_policy_client_mtls_env_auto(
    client_class, transport_class, transport_name, use_client_cert_env
):
    # This tests the endpoint autoswitch behavior. Endpoint is autoswitched to the default
    # mtls endpoint, if GOOGLE_API_USE_CLIENT_CERTIFICATE is "true" and client cert exists.

    # Check the case client_cert_source is provided. Whether client cert is used depends on
    # GOOGLE_API_USE_CLIENT_CERTIFICATE value.
    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": use_client_cert_env}
    ):
        options = client_options.ClientOptions(
            client_cert_source=client_cert_source_callback
        )
        with mock.patch.object(transport_class, "__init__") as patched:
            patched.return_value = None
            client = client_class(client_options=options, transport=transport_name)

            if use_client_cert_env == "false":
                expected_client_cert_source = None
                expected_host = client.DEFAULT_ENDPOINT
            else:
                expected_client_cert_source = client_cert_source_callback
                expected_host = client.DEFAULT_MTLS_ENDPOINT

            patched.assert_called_once_with(
                credentials=None,
                credentials_file=None,
                host=expected_host,
                scopes=None,
                client_cert_source_for_mtls=expected_client_cert_source,
                quota_project_id=None,
                client_info=transports.base.DEFAULT_CLIENT_INFO,
                always_use_jwt_access=True,
                api_audience=None,
            )

    # Check the case ADC client cert is provided. Whether client cert is used depends on
    # GOOGLE_API_USE_CLIENT_CERTIFICATE value.
    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": use_client_cert_env}
    ):
        with mock.patch.object(transport_class, "__init__") as patched:
            with mock.patch(
                "google.auth.transport.mtls.has_default_client_cert_source",
                return_value=True,
            ):
                with mock.patch(
                    "google.auth.transport.mtls.default_client_cert_source",
                    return_value=client_cert_source_callback,
                ):
                    if use_client_cert_env == "false":
                        expected_host = client.DEFAULT_ENDPOINT
                        expected_client_cert_source = None
                    else:
                        expected_host = client.DEFAULT_MTLS_ENDPOINT
                        expected_client_cert_source = client_cert_source_callback

                    patched.return_value = None
                    client = client_class(transport=transport_name)
                    patched.assert_called_once_with(
                        credentials=None,
                        credentials_file=None,
                        host=expected_host,
                        scopes=None,
                        client_cert_source_for_mtls=expected_client_cert_source,
                        quota_project_id=None,
                        client_info=transports.base.DEFAULT_CLIENT_INFO,
                        always_use_jwt_access=True,
                        api_audience=None,
                    )

    # Check the case client_cert_source and ADC client cert are not provided.
    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": use_client_cert_env}
    ):
        with mock.patch.object(transport_class, "__init__") as patched:
            with mock.patch(
                "google.auth.transport.mtls.has_default_client_cert_source",
                return_value=False,
            ):
                patched.return_value = None
                client = client_class(transport=transport_name)
                patched.assert_called_once_with(
                    credentials=None,
                    credentials_file=None,
                    host=client.DEFAULT_ENDPOINT,
                    scopes=None,
                    client_cert_source_for_mtls=None,
                    quota_project_id=None,
                    client_info=transports.base.DEFAULT_CLIENT_INFO,
                    always_use_jwt_access=True,
                    api_audience=None,
                )


@pytest.mark.parametrize("client_class", [OrgPolicyClient, OrgPolicyAsyncClient])
@mock.patch.object(
    OrgPolicyClient, "DEFAULT_ENDPOINT", modify_default_endpoint(OrgPolicyClient)
)
@mock.patch.object(
    OrgPolicyAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(OrgPolicyAsyncClient),
)
def test_org_policy_client_get_mtls_endpoint_and_cert_source(client_class):
    mock_client_cert_source = mock.Mock()

    # Test the case GOOGLE_API_USE_CLIENT_CERTIFICATE is "true".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "true"}):
        mock_api_endpoint = "foo"
        options = client_options.ClientOptions(
            client_cert_source=mock_client_cert_source, api_endpoint=mock_api_endpoint
        )
        api_endpoint, cert_source = client_class.get_mtls_endpoint_and_cert_source(
            options
        )
        assert api_endpoint == mock_api_endpoint
        assert cert_source == mock_client_cert_source

    # Test the case GOOGLE_API_USE_CLIENT_CERTIFICATE is "false".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "false"}):
        mock_client_cert_source = mock.Mock()
        mock_api_endpoint = "foo"
        options = client_options.ClientOptions(
            client_cert_source=mock_client_cert_source, api_endpoint=mock_api_endpoint
        )
        api_endpoint, cert_source = client_class.get_mtls_endpoint_and_cert_source(
            options
        )
        assert api_endpoint == mock_api_endpoint
        assert cert_source is None

    # Test the case GOOGLE_API_USE_MTLS_ENDPOINT is "never".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "never"}):
        api_endpoint, cert_source = client_class.get_mtls_endpoint_and_cert_source()
        assert api_endpoint == client_class.DEFAULT_ENDPOINT
        assert cert_source is None

    # Test the case GOOGLE_API_USE_MTLS_ENDPOINT is "always".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "always"}):
        api_endpoint, cert_source = client_class.get_mtls_endpoint_and_cert_source()
        assert api_endpoint == client_class.DEFAULT_MTLS_ENDPOINT
        assert cert_source is None

    # Test the case GOOGLE_API_USE_MTLS_ENDPOINT is "auto" and default cert doesn't exist.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "true"}):
        with mock.patch(
            "google.auth.transport.mtls.has_default_client_cert_source",
            return_value=False,
        ):
            api_endpoint, cert_source = client_class.get_mtls_endpoint_and_cert_source()
            assert api_endpoint == client_class.DEFAULT_ENDPOINT
            assert cert_source is None

    # Test the case GOOGLE_API_USE_MTLS_ENDPOINT is "auto" and default cert exists.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "true"}):
        with mock.patch(
            "google.auth.transport.mtls.has_default_client_cert_source",
            return_value=True,
        ):
            with mock.patch(
                "google.auth.transport.mtls.default_client_cert_source",
                return_value=mock_client_cert_source,
            ):
                (
                    api_endpoint,
                    cert_source,
                ) = client_class.get_mtls_endpoint_and_cert_source()
                assert api_endpoint == client_class.DEFAULT_MTLS_ENDPOINT
                assert cert_source == mock_client_cert_source


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (OrgPolicyClient, transports.OrgPolicyGrpcTransport, "grpc"),
        (
            OrgPolicyAsyncClient,
            transports.OrgPolicyGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
        (OrgPolicyClient, transports.OrgPolicyRestTransport, "rest"),
    ],
)
def test_org_policy_client_client_options_scopes(
    client_class, transport_class, transport_name
):
    # Check the case scopes are provided.
    options = client_options.ClientOptions(
        scopes=["1", "2"],
    )
    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options, transport=transport_name)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host=client.DEFAULT_ENDPOINT,
            scopes=["1", "2"],
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
            api_audience=None,
        )


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name,grpc_helpers",
    [
        (OrgPolicyClient, transports.OrgPolicyGrpcTransport, "grpc", grpc_helpers),
        (
            OrgPolicyAsyncClient,
            transports.OrgPolicyGrpcAsyncIOTransport,
            "grpc_asyncio",
            grpc_helpers_async,
        ),
        (OrgPolicyClient, transports.OrgPolicyRestTransport, "rest", None),
    ],
)
def test_org_policy_client_client_options_credentials_file(
    client_class, transport_class, transport_name, grpc_helpers
):
    # Check the case credentials file is provided.
    options = client_options.ClientOptions(credentials_file="credentials.json")

    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options, transport=transport_name)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file="credentials.json",
            host=client.DEFAULT_ENDPOINT,
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
            api_audience=None,
        )


def test_org_policy_client_client_options_from_dict():
    with mock.patch(
        "google.cloud.orgpolicy_v2.services.org_policy.transports.OrgPolicyGrpcTransport.__init__"
    ) as grpc_transport:
        grpc_transport.return_value = None
        client = OrgPolicyClient(client_options={"api_endpoint": "squid.clam.whelk"})
        grpc_transport.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host="squid.clam.whelk",
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
            api_audience=None,
        )


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name,grpc_helpers",
    [
        (OrgPolicyClient, transports.OrgPolicyGrpcTransport, "grpc", grpc_helpers),
        (
            OrgPolicyAsyncClient,
            transports.OrgPolicyGrpcAsyncIOTransport,
            "grpc_asyncio",
            grpc_helpers_async,
        ),
    ],
)
def test_org_policy_client_create_channel_credentials_file(
    client_class, transport_class, transport_name, grpc_helpers
):
    # Check the case credentials file is provided.
    options = client_options.ClientOptions(credentials_file="credentials.json")

    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options, transport=transport_name)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file="credentials.json",
            host=client.DEFAULT_ENDPOINT,
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
            api_audience=None,
        )

    # test that the credentials from file are saved and used as the credentials.
    with mock.patch.object(
        google.auth, "load_credentials_from_file", autospec=True
    ) as load_creds, mock.patch.object(
        google.auth, "default", autospec=True
    ) as adc, mock.patch.object(
        grpc_helpers, "create_channel"
    ) as create_channel:
        creds = ga_credentials.AnonymousCredentials()
        file_creds = ga_credentials.AnonymousCredentials()
        load_creds.return_value = (file_creds, None)
        adc.return_value = (creds, None)
        client = client_class(client_options=options, transport=transport_name)
        create_channel.assert_called_with(
            "orgpolicy.googleapis.com:443",
            credentials=file_creds,
            credentials_file=None,
            quota_project_id=None,
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            scopes=None,
            default_host="orgpolicy.googleapis.com",
            ssl_credentials=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )


@pytest.mark.parametrize(
    "request_type",
    [
        orgpolicy.ListConstraintsRequest,
        dict,
    ],
)
def test_list_constraints(request_type, transport: str = "grpc"):
    client = OrgPolicyClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_constraints), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = orgpolicy.ListConstraintsResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_constraints(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == orgpolicy.ListConstraintsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListConstraintsPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_constraints_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = OrgPolicyClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_constraints), "__call__") as call:
        client.list_constraints()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == orgpolicy.ListConstraintsRequest()


@pytest.mark.asyncio
async def test_list_constraints_async(
    transport: str = "grpc_asyncio", request_type=orgpolicy.ListConstraintsRequest
):
    client = OrgPolicyAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_constraints), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            orgpolicy.ListConstraintsResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_constraints(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == orgpolicy.ListConstraintsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListConstraintsAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_constraints_async_from_dict():
    await test_list_constraints_async(request_type=dict)


def test_list_constraints_field_headers():
    client = OrgPolicyClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = orgpolicy.ListConstraintsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_constraints), "__call__") as call:
        call.return_value = orgpolicy.ListConstraintsResponse()
        client.list_constraints(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_constraints_field_headers_async():
    client = OrgPolicyAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = orgpolicy.ListConstraintsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_constraints), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            orgpolicy.ListConstraintsResponse()
        )
        await client.list_constraints(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


def test_list_constraints_flattened():
    client = OrgPolicyClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_constraints), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = orgpolicy.ListConstraintsResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_constraints(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_constraints_flattened_error():
    client = OrgPolicyClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_constraints(
            orgpolicy.ListConstraintsRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_constraints_flattened_async():
    client = OrgPolicyAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_constraints), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = orgpolicy.ListConstraintsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            orgpolicy.ListConstraintsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_constraints(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_list_constraints_flattened_error_async():
    client = OrgPolicyAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_constraints(
            orgpolicy.ListConstraintsRequest(),
            parent="parent_value",
        )


def test_list_constraints_pager(transport_name: str = "grpc"):
    client = OrgPolicyClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_constraints), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            orgpolicy.ListConstraintsResponse(
                constraints=[
                    constraint.Constraint(),
                    constraint.Constraint(),
                    constraint.Constraint(),
                ],
                next_page_token="abc",
            ),
            orgpolicy.ListConstraintsResponse(
                constraints=[],
                next_page_token="def",
            ),
            orgpolicy.ListConstraintsResponse(
                constraints=[
                    constraint.Constraint(),
                ],
                next_page_token="ghi",
            ),
            orgpolicy.ListConstraintsResponse(
                constraints=[
                    constraint.Constraint(),
                    constraint.Constraint(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_constraints(request={})

        assert pager._metadata == metadata

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, constraint.Constraint) for i in results)


def test_list_constraints_pages(transport_name: str = "grpc"):
    client = OrgPolicyClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_constraints), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            orgpolicy.ListConstraintsResponse(
                constraints=[
                    constraint.Constraint(),
                    constraint.Constraint(),
                    constraint.Constraint(),
                ],
                next_page_token="abc",
            ),
            orgpolicy.ListConstraintsResponse(
                constraints=[],
                next_page_token="def",
            ),
            orgpolicy.ListConstraintsResponse(
                constraints=[
                    constraint.Constraint(),
                ],
                next_page_token="ghi",
            ),
            orgpolicy.ListConstraintsResponse(
                constraints=[
                    constraint.Constraint(),
                    constraint.Constraint(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_constraints(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_constraints_async_pager():
    client = OrgPolicyAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_constraints), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            orgpolicy.ListConstraintsResponse(
                constraints=[
                    constraint.Constraint(),
                    constraint.Constraint(),
                    constraint.Constraint(),
                ],
                next_page_token="abc",
            ),
            orgpolicy.ListConstraintsResponse(
                constraints=[],
                next_page_token="def",
            ),
            orgpolicy.ListConstraintsResponse(
                constraints=[
                    constraint.Constraint(),
                ],
                next_page_token="ghi",
            ),
            orgpolicy.ListConstraintsResponse(
                constraints=[
                    constraint.Constraint(),
                    constraint.Constraint(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_constraints(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, constraint.Constraint) for i in responses)


@pytest.mark.asyncio
async def test_list_constraints_async_pages():
    client = OrgPolicyAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_constraints), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            orgpolicy.ListConstraintsResponse(
                constraints=[
                    constraint.Constraint(),
                    constraint.Constraint(),
                    constraint.Constraint(),
                ],
                next_page_token="abc",
            ),
            orgpolicy.ListConstraintsResponse(
                constraints=[],
                next_page_token="def",
            ),
            orgpolicy.ListConstraintsResponse(
                constraints=[
                    constraint.Constraint(),
                ],
                next_page_token="ghi",
            ),
            orgpolicy.ListConstraintsResponse(
                constraints=[
                    constraint.Constraint(),
                    constraint.Constraint(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        # Workaround issue in python 3.9 related to code coverage by adding `# pragma: no branch`
        # See https://github.com/googleapis/gapic-generator-python/pull/1174#issuecomment-1025132372
        async for page_ in (  # pragma: no branch
            await client.list_constraints(request={})
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        orgpolicy.ListPoliciesRequest,
        dict,
    ],
)
def test_list_policies(request_type, transport: str = "grpc"):
    client = OrgPolicyClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_policies), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = orgpolicy.ListPoliciesResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_policies(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == orgpolicy.ListPoliciesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListPoliciesPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_policies_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = OrgPolicyClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_policies), "__call__") as call:
        client.list_policies()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == orgpolicy.ListPoliciesRequest()


@pytest.mark.asyncio
async def test_list_policies_async(
    transport: str = "grpc_asyncio", request_type=orgpolicy.ListPoliciesRequest
):
    client = OrgPolicyAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_policies), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            orgpolicy.ListPoliciesResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_policies(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == orgpolicy.ListPoliciesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListPoliciesAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_policies_async_from_dict():
    await test_list_policies_async(request_type=dict)


def test_list_policies_field_headers():
    client = OrgPolicyClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = orgpolicy.ListPoliciesRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_policies), "__call__") as call:
        call.return_value = orgpolicy.ListPoliciesResponse()
        client.list_policies(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_policies_field_headers_async():
    client = OrgPolicyAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = orgpolicy.ListPoliciesRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_policies), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            orgpolicy.ListPoliciesResponse()
        )
        await client.list_policies(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


def test_list_policies_flattened():
    client = OrgPolicyClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_policies), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = orgpolicy.ListPoliciesResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_policies(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_policies_flattened_error():
    client = OrgPolicyClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_policies(
            orgpolicy.ListPoliciesRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_policies_flattened_async():
    client = OrgPolicyAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_policies), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = orgpolicy.ListPoliciesResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            orgpolicy.ListPoliciesResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_policies(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_list_policies_flattened_error_async():
    client = OrgPolicyAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_policies(
            orgpolicy.ListPoliciesRequest(),
            parent="parent_value",
        )


def test_list_policies_pager(transport_name: str = "grpc"):
    client = OrgPolicyClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_policies), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            orgpolicy.ListPoliciesResponse(
                policies=[
                    orgpolicy.Policy(),
                    orgpolicy.Policy(),
                    orgpolicy.Policy(),
                ],
                next_page_token="abc",
            ),
            orgpolicy.ListPoliciesResponse(
                policies=[],
                next_page_token="def",
            ),
            orgpolicy.ListPoliciesResponse(
                policies=[
                    orgpolicy.Policy(),
                ],
                next_page_token="ghi",
            ),
            orgpolicy.ListPoliciesResponse(
                policies=[
                    orgpolicy.Policy(),
                    orgpolicy.Policy(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_policies(request={})

        assert pager._metadata == metadata

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, orgpolicy.Policy) for i in results)


def test_list_policies_pages(transport_name: str = "grpc"):
    client = OrgPolicyClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_policies), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            orgpolicy.ListPoliciesResponse(
                policies=[
                    orgpolicy.Policy(),
                    orgpolicy.Policy(),
                    orgpolicy.Policy(),
                ],
                next_page_token="abc",
            ),
            orgpolicy.ListPoliciesResponse(
                policies=[],
                next_page_token="def",
            ),
            orgpolicy.ListPoliciesResponse(
                policies=[
                    orgpolicy.Policy(),
                ],
                next_page_token="ghi",
            ),
            orgpolicy.ListPoliciesResponse(
                policies=[
                    orgpolicy.Policy(),
                    orgpolicy.Policy(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_policies(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_policies_async_pager():
    client = OrgPolicyAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_policies), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            orgpolicy.ListPoliciesResponse(
                policies=[
                    orgpolicy.Policy(),
                    orgpolicy.Policy(),
                    orgpolicy.Policy(),
                ],
                next_page_token="abc",
            ),
            orgpolicy.ListPoliciesResponse(
                policies=[],
                next_page_token="def",
            ),
            orgpolicy.ListPoliciesResponse(
                policies=[
                    orgpolicy.Policy(),
                ],
                next_page_token="ghi",
            ),
            orgpolicy.ListPoliciesResponse(
                policies=[
                    orgpolicy.Policy(),
                    orgpolicy.Policy(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_policies(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, orgpolicy.Policy) for i in responses)


@pytest.mark.asyncio
async def test_list_policies_async_pages():
    client = OrgPolicyAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_policies), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            orgpolicy.ListPoliciesResponse(
                policies=[
                    orgpolicy.Policy(),
                    orgpolicy.Policy(),
                    orgpolicy.Policy(),
                ],
                next_page_token="abc",
            ),
            orgpolicy.ListPoliciesResponse(
                policies=[],
                next_page_token="def",
            ),
            orgpolicy.ListPoliciesResponse(
                policies=[
                    orgpolicy.Policy(),
                ],
                next_page_token="ghi",
            ),
            orgpolicy.ListPoliciesResponse(
                policies=[
                    orgpolicy.Policy(),
                    orgpolicy.Policy(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        # Workaround issue in python 3.9 related to code coverage by adding `# pragma: no branch`
        # See https://github.com/googleapis/gapic-generator-python/pull/1174#issuecomment-1025132372
        async for page_ in (  # pragma: no branch
            await client.list_policies(request={})
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        orgpolicy.GetPolicyRequest,
        dict,
    ],
)
def test_get_policy(request_type, transport: str = "grpc"):
    client = OrgPolicyClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_policy), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = orgpolicy.Policy(
            name="name_value",
            etag="etag_value",
        )
        response = client.get_policy(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == orgpolicy.GetPolicyRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, orgpolicy.Policy)
    assert response.name == "name_value"
    assert response.etag == "etag_value"


def test_get_policy_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = OrgPolicyClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_policy), "__call__") as call:
        client.get_policy()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == orgpolicy.GetPolicyRequest()


@pytest.mark.asyncio
async def test_get_policy_async(
    transport: str = "grpc_asyncio", request_type=orgpolicy.GetPolicyRequest
):
    client = OrgPolicyAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_policy), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            orgpolicy.Policy(
                name="name_value",
                etag="etag_value",
            )
        )
        response = await client.get_policy(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == orgpolicy.GetPolicyRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, orgpolicy.Policy)
    assert response.name == "name_value"
    assert response.etag == "etag_value"


@pytest.mark.asyncio
async def test_get_policy_async_from_dict():
    await test_get_policy_async(request_type=dict)


def test_get_policy_field_headers():
    client = OrgPolicyClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = orgpolicy.GetPolicyRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_policy), "__call__") as call:
        call.return_value = orgpolicy.Policy()
        client.get_policy(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_policy_field_headers_async():
    client = OrgPolicyAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = orgpolicy.GetPolicyRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_policy), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(orgpolicy.Policy())
        await client.get_policy(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


def test_get_policy_flattened():
    client = OrgPolicyClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_policy), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = orgpolicy.Policy()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_policy(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_policy_flattened_error():
    client = OrgPolicyClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_policy(
            orgpolicy.GetPolicyRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_policy_flattened_async():
    client = OrgPolicyAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_policy), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = orgpolicy.Policy()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(orgpolicy.Policy())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_policy(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_get_policy_flattened_error_async():
    client = OrgPolicyAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_policy(
            orgpolicy.GetPolicyRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        orgpolicy.GetEffectivePolicyRequest,
        dict,
    ],
)
def test_get_effective_policy(request_type, transport: str = "grpc"):
    client = OrgPolicyClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_effective_policy), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = orgpolicy.Policy(
            name="name_value",
            etag="etag_value",
        )
        response = client.get_effective_policy(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == orgpolicy.GetEffectivePolicyRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, orgpolicy.Policy)
    assert response.name == "name_value"
    assert response.etag == "etag_value"


def test_get_effective_policy_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = OrgPolicyClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_effective_policy), "__call__"
    ) as call:
        client.get_effective_policy()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == orgpolicy.GetEffectivePolicyRequest()


@pytest.mark.asyncio
async def test_get_effective_policy_async(
    transport: str = "grpc_asyncio", request_type=orgpolicy.GetEffectivePolicyRequest
):
    client = OrgPolicyAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_effective_policy), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            orgpolicy.Policy(
                name="name_value",
                etag="etag_value",
            )
        )
        response = await client.get_effective_policy(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == orgpolicy.GetEffectivePolicyRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, orgpolicy.Policy)
    assert response.name == "name_value"
    assert response.etag == "etag_value"


@pytest.mark.asyncio
async def test_get_effective_policy_async_from_dict():
    await test_get_effective_policy_async(request_type=dict)


def test_get_effective_policy_field_headers():
    client = OrgPolicyClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = orgpolicy.GetEffectivePolicyRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_effective_policy), "__call__"
    ) as call:
        call.return_value = orgpolicy.Policy()
        client.get_effective_policy(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_effective_policy_field_headers_async():
    client = OrgPolicyAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = orgpolicy.GetEffectivePolicyRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_effective_policy), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(orgpolicy.Policy())
        await client.get_effective_policy(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


def test_get_effective_policy_flattened():
    client = OrgPolicyClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_effective_policy), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = orgpolicy.Policy()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_effective_policy(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_effective_policy_flattened_error():
    client = OrgPolicyClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_effective_policy(
            orgpolicy.GetEffectivePolicyRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_effective_policy_flattened_async():
    client = OrgPolicyAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_effective_policy), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = orgpolicy.Policy()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(orgpolicy.Policy())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_effective_policy(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_get_effective_policy_flattened_error_async():
    client = OrgPolicyAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_effective_policy(
            orgpolicy.GetEffectivePolicyRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        orgpolicy.CreatePolicyRequest,
        dict,
    ],
)
def test_create_policy(request_type, transport: str = "grpc"):
    client = OrgPolicyClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_policy), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = orgpolicy.Policy(
            name="name_value",
            etag="etag_value",
        )
        response = client.create_policy(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == orgpolicy.CreatePolicyRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, orgpolicy.Policy)
    assert response.name == "name_value"
    assert response.etag == "etag_value"


def test_create_policy_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = OrgPolicyClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_policy), "__call__") as call:
        client.create_policy()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == orgpolicy.CreatePolicyRequest()


@pytest.mark.asyncio
async def test_create_policy_async(
    transport: str = "grpc_asyncio", request_type=orgpolicy.CreatePolicyRequest
):
    client = OrgPolicyAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_policy), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            orgpolicy.Policy(
                name="name_value",
                etag="etag_value",
            )
        )
        response = await client.create_policy(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == orgpolicy.CreatePolicyRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, orgpolicy.Policy)
    assert response.name == "name_value"
    assert response.etag == "etag_value"


@pytest.mark.asyncio
async def test_create_policy_async_from_dict():
    await test_create_policy_async(request_type=dict)


def test_create_policy_field_headers():
    client = OrgPolicyClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = orgpolicy.CreatePolicyRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_policy), "__call__") as call:
        call.return_value = orgpolicy.Policy()
        client.create_policy(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_create_policy_field_headers_async():
    client = OrgPolicyAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = orgpolicy.CreatePolicyRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_policy), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(orgpolicy.Policy())
        await client.create_policy(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


def test_create_policy_flattened():
    client = OrgPolicyClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_policy), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = orgpolicy.Policy()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_policy(
            parent="parent_value",
            policy=orgpolicy.Policy(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].policy
        mock_val = orgpolicy.Policy(name="name_value")
        assert arg == mock_val


def test_create_policy_flattened_error():
    client = OrgPolicyClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_policy(
            orgpolicy.CreatePolicyRequest(),
            parent="parent_value",
            policy=orgpolicy.Policy(name="name_value"),
        )


@pytest.mark.asyncio
async def test_create_policy_flattened_async():
    client = OrgPolicyAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_policy), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = orgpolicy.Policy()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(orgpolicy.Policy())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_policy(
            parent="parent_value",
            policy=orgpolicy.Policy(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].policy
        mock_val = orgpolicy.Policy(name="name_value")
        assert arg == mock_val


@pytest.mark.asyncio
async def test_create_policy_flattened_error_async():
    client = OrgPolicyAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_policy(
            orgpolicy.CreatePolicyRequest(),
            parent="parent_value",
            policy=orgpolicy.Policy(name="name_value"),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        orgpolicy.UpdatePolicyRequest,
        dict,
    ],
)
def test_update_policy(request_type, transport: str = "grpc"):
    client = OrgPolicyClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_policy), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = orgpolicy.Policy(
            name="name_value",
            etag="etag_value",
        )
        response = client.update_policy(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == orgpolicy.UpdatePolicyRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, orgpolicy.Policy)
    assert response.name == "name_value"
    assert response.etag == "etag_value"


def test_update_policy_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = OrgPolicyClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_policy), "__call__") as call:
        client.update_policy()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == orgpolicy.UpdatePolicyRequest()


@pytest.mark.asyncio
async def test_update_policy_async(
    transport: str = "grpc_asyncio", request_type=orgpolicy.UpdatePolicyRequest
):
    client = OrgPolicyAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_policy), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            orgpolicy.Policy(
                name="name_value",
                etag="etag_value",
            )
        )
        response = await client.update_policy(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == orgpolicy.UpdatePolicyRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, orgpolicy.Policy)
    assert response.name == "name_value"
    assert response.etag == "etag_value"


@pytest.mark.asyncio
async def test_update_policy_async_from_dict():
    await test_update_policy_async(request_type=dict)


def test_update_policy_field_headers():
    client = OrgPolicyClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = orgpolicy.UpdatePolicyRequest()

    request.policy.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_policy), "__call__") as call:
        call.return_value = orgpolicy.Policy()
        client.update_policy(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "policy.name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_update_policy_field_headers_async():
    client = OrgPolicyAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = orgpolicy.UpdatePolicyRequest()

    request.policy.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_policy), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(orgpolicy.Policy())
        await client.update_policy(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "policy.name=name_value",
    ) in kw["metadata"]


def test_update_policy_flattened():
    client = OrgPolicyClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_policy), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = orgpolicy.Policy()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_policy(
            policy=orgpolicy.Policy(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].policy
        mock_val = orgpolicy.Policy(name="name_value")
        assert arg == mock_val


def test_update_policy_flattened_error():
    client = OrgPolicyClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_policy(
            orgpolicy.UpdatePolicyRequest(),
            policy=orgpolicy.Policy(name="name_value"),
        )


@pytest.mark.asyncio
async def test_update_policy_flattened_async():
    client = OrgPolicyAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_policy), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = orgpolicy.Policy()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(orgpolicy.Policy())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_policy(
            policy=orgpolicy.Policy(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].policy
        mock_val = orgpolicy.Policy(name="name_value")
        assert arg == mock_val


@pytest.mark.asyncio
async def test_update_policy_flattened_error_async():
    client = OrgPolicyAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_policy(
            orgpolicy.UpdatePolicyRequest(),
            policy=orgpolicy.Policy(name="name_value"),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        orgpolicy.DeletePolicyRequest,
        dict,
    ],
)
def test_delete_policy(request_type, transport: str = "grpc"):
    client = OrgPolicyClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_policy), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        response = client.delete_policy(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == orgpolicy.DeletePolicyRequest()

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_policy_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = OrgPolicyClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_policy), "__call__") as call:
        client.delete_policy()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == orgpolicy.DeletePolicyRequest()


@pytest.mark.asyncio
async def test_delete_policy_async(
    transport: str = "grpc_asyncio", request_type=orgpolicy.DeletePolicyRequest
):
    client = OrgPolicyAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_policy), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        response = await client.delete_policy(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == orgpolicy.DeletePolicyRequest()

    # Establish that the response is the type that we expect.
    assert response is None


@pytest.mark.asyncio
async def test_delete_policy_async_from_dict():
    await test_delete_policy_async(request_type=dict)


def test_delete_policy_field_headers():
    client = OrgPolicyClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = orgpolicy.DeletePolicyRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_policy), "__call__") as call:
        call.return_value = None
        client.delete_policy(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_delete_policy_field_headers_async():
    client = OrgPolicyAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = orgpolicy.DeletePolicyRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_policy), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        await client.delete_policy(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


def test_delete_policy_flattened():
    client = OrgPolicyClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_policy), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_policy(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_delete_policy_flattened_error():
    client = OrgPolicyClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_policy(
            orgpolicy.DeletePolicyRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_policy_flattened_async():
    client = OrgPolicyAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_policy), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_policy(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_delete_policy_flattened_error_async():
    client = OrgPolicyAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_policy(
            orgpolicy.DeletePolicyRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        orgpolicy.CreateCustomConstraintRequest,
        dict,
    ],
)
def test_create_custom_constraint(request_type, transport: str = "grpc"):
    client = OrgPolicyClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_custom_constraint), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = constraint.CustomConstraint(
            name="name_value",
            resource_types=["resource_types_value"],
            method_types=[constraint.CustomConstraint.MethodType.CREATE],
            condition="condition_value",
            action_type=constraint.CustomConstraint.ActionType.ALLOW,
            display_name="display_name_value",
            description="description_value",
        )
        response = client.create_custom_constraint(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == orgpolicy.CreateCustomConstraintRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, constraint.CustomConstraint)
    assert response.name == "name_value"
    assert response.resource_types == ["resource_types_value"]
    assert response.method_types == [constraint.CustomConstraint.MethodType.CREATE]
    assert response.condition == "condition_value"
    assert response.action_type == constraint.CustomConstraint.ActionType.ALLOW
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"


def test_create_custom_constraint_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = OrgPolicyClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_custom_constraint), "__call__"
    ) as call:
        client.create_custom_constraint()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == orgpolicy.CreateCustomConstraintRequest()


@pytest.mark.asyncio
async def test_create_custom_constraint_async(
    transport: str = "grpc_asyncio",
    request_type=orgpolicy.CreateCustomConstraintRequest,
):
    client = OrgPolicyAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_custom_constraint), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            constraint.CustomConstraint(
                name="name_value",
                resource_types=["resource_types_value"],
                method_types=[constraint.CustomConstraint.MethodType.CREATE],
                condition="condition_value",
                action_type=constraint.CustomConstraint.ActionType.ALLOW,
                display_name="display_name_value",
                description="description_value",
            )
        )
        response = await client.create_custom_constraint(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == orgpolicy.CreateCustomConstraintRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, constraint.CustomConstraint)
    assert response.name == "name_value"
    assert response.resource_types == ["resource_types_value"]
    assert response.method_types == [constraint.CustomConstraint.MethodType.CREATE]
    assert response.condition == "condition_value"
    assert response.action_type == constraint.CustomConstraint.ActionType.ALLOW
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"


@pytest.mark.asyncio
async def test_create_custom_constraint_async_from_dict():
    await test_create_custom_constraint_async(request_type=dict)


def test_create_custom_constraint_field_headers():
    client = OrgPolicyClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = orgpolicy.CreateCustomConstraintRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_custom_constraint), "__call__"
    ) as call:
        call.return_value = constraint.CustomConstraint()
        client.create_custom_constraint(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_create_custom_constraint_field_headers_async():
    client = OrgPolicyAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = orgpolicy.CreateCustomConstraintRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_custom_constraint), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            constraint.CustomConstraint()
        )
        await client.create_custom_constraint(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


def test_create_custom_constraint_flattened():
    client = OrgPolicyClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_custom_constraint), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = constraint.CustomConstraint()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_custom_constraint(
            parent="parent_value",
            custom_constraint=constraint.CustomConstraint(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].custom_constraint
        mock_val = constraint.CustomConstraint(name="name_value")
        assert arg == mock_val


def test_create_custom_constraint_flattened_error():
    client = OrgPolicyClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_custom_constraint(
            orgpolicy.CreateCustomConstraintRequest(),
            parent="parent_value",
            custom_constraint=constraint.CustomConstraint(name="name_value"),
        )


@pytest.mark.asyncio
async def test_create_custom_constraint_flattened_async():
    client = OrgPolicyAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_custom_constraint), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = constraint.CustomConstraint()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            constraint.CustomConstraint()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_custom_constraint(
            parent="parent_value",
            custom_constraint=constraint.CustomConstraint(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].custom_constraint
        mock_val = constraint.CustomConstraint(name="name_value")
        assert arg == mock_val


@pytest.mark.asyncio
async def test_create_custom_constraint_flattened_error_async():
    client = OrgPolicyAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_custom_constraint(
            orgpolicy.CreateCustomConstraintRequest(),
            parent="parent_value",
            custom_constraint=constraint.CustomConstraint(name="name_value"),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        orgpolicy.UpdateCustomConstraintRequest,
        dict,
    ],
)
def test_update_custom_constraint(request_type, transport: str = "grpc"):
    client = OrgPolicyClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_custom_constraint), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = constraint.CustomConstraint(
            name="name_value",
            resource_types=["resource_types_value"],
            method_types=[constraint.CustomConstraint.MethodType.CREATE],
            condition="condition_value",
            action_type=constraint.CustomConstraint.ActionType.ALLOW,
            display_name="display_name_value",
            description="description_value",
        )
        response = client.update_custom_constraint(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == orgpolicy.UpdateCustomConstraintRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, constraint.CustomConstraint)
    assert response.name == "name_value"
    assert response.resource_types == ["resource_types_value"]
    assert response.method_types == [constraint.CustomConstraint.MethodType.CREATE]
    assert response.condition == "condition_value"
    assert response.action_type == constraint.CustomConstraint.ActionType.ALLOW
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"


def test_update_custom_constraint_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = OrgPolicyClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_custom_constraint), "__call__"
    ) as call:
        client.update_custom_constraint()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == orgpolicy.UpdateCustomConstraintRequest()


@pytest.mark.asyncio
async def test_update_custom_constraint_async(
    transport: str = "grpc_asyncio",
    request_type=orgpolicy.UpdateCustomConstraintRequest,
):
    client = OrgPolicyAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_custom_constraint), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            constraint.CustomConstraint(
                name="name_value",
                resource_types=["resource_types_value"],
                method_types=[constraint.CustomConstraint.MethodType.CREATE],
                condition="condition_value",
                action_type=constraint.CustomConstraint.ActionType.ALLOW,
                display_name="display_name_value",
                description="description_value",
            )
        )
        response = await client.update_custom_constraint(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == orgpolicy.UpdateCustomConstraintRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, constraint.CustomConstraint)
    assert response.name == "name_value"
    assert response.resource_types == ["resource_types_value"]
    assert response.method_types == [constraint.CustomConstraint.MethodType.CREATE]
    assert response.condition == "condition_value"
    assert response.action_type == constraint.CustomConstraint.ActionType.ALLOW
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"


@pytest.mark.asyncio
async def test_update_custom_constraint_async_from_dict():
    await test_update_custom_constraint_async(request_type=dict)


def test_update_custom_constraint_field_headers():
    client = OrgPolicyClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = orgpolicy.UpdateCustomConstraintRequest()

    request.custom_constraint.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_custom_constraint), "__call__"
    ) as call:
        call.return_value = constraint.CustomConstraint()
        client.update_custom_constraint(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "custom_constraint.name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_update_custom_constraint_field_headers_async():
    client = OrgPolicyAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = orgpolicy.UpdateCustomConstraintRequest()

    request.custom_constraint.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_custom_constraint), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            constraint.CustomConstraint()
        )
        await client.update_custom_constraint(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "custom_constraint.name=name_value",
    ) in kw["metadata"]


def test_update_custom_constraint_flattened():
    client = OrgPolicyClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_custom_constraint), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = constraint.CustomConstraint()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_custom_constraint(
            custom_constraint=constraint.CustomConstraint(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].custom_constraint
        mock_val = constraint.CustomConstraint(name="name_value")
        assert arg == mock_val


def test_update_custom_constraint_flattened_error():
    client = OrgPolicyClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_custom_constraint(
            orgpolicy.UpdateCustomConstraintRequest(),
            custom_constraint=constraint.CustomConstraint(name="name_value"),
        )


@pytest.mark.asyncio
async def test_update_custom_constraint_flattened_async():
    client = OrgPolicyAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_custom_constraint), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = constraint.CustomConstraint()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            constraint.CustomConstraint()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_custom_constraint(
            custom_constraint=constraint.CustomConstraint(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].custom_constraint
        mock_val = constraint.CustomConstraint(name="name_value")
        assert arg == mock_val


@pytest.mark.asyncio
async def test_update_custom_constraint_flattened_error_async():
    client = OrgPolicyAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_custom_constraint(
            orgpolicy.UpdateCustomConstraintRequest(),
            custom_constraint=constraint.CustomConstraint(name="name_value"),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        orgpolicy.GetCustomConstraintRequest,
        dict,
    ],
)
def test_get_custom_constraint(request_type, transport: str = "grpc"):
    client = OrgPolicyClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_custom_constraint), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = constraint.CustomConstraint(
            name="name_value",
            resource_types=["resource_types_value"],
            method_types=[constraint.CustomConstraint.MethodType.CREATE],
            condition="condition_value",
            action_type=constraint.CustomConstraint.ActionType.ALLOW,
            display_name="display_name_value",
            description="description_value",
        )
        response = client.get_custom_constraint(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == orgpolicy.GetCustomConstraintRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, constraint.CustomConstraint)
    assert response.name == "name_value"
    assert response.resource_types == ["resource_types_value"]
    assert response.method_types == [constraint.CustomConstraint.MethodType.CREATE]
    assert response.condition == "condition_value"
    assert response.action_type == constraint.CustomConstraint.ActionType.ALLOW
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"


def test_get_custom_constraint_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = OrgPolicyClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_custom_constraint), "__call__"
    ) as call:
        client.get_custom_constraint()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == orgpolicy.GetCustomConstraintRequest()


@pytest.mark.asyncio
async def test_get_custom_constraint_async(
    transport: str = "grpc_asyncio", request_type=orgpolicy.GetCustomConstraintRequest
):
    client = OrgPolicyAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_custom_constraint), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            constraint.CustomConstraint(
                name="name_value",
                resource_types=["resource_types_value"],
                method_types=[constraint.CustomConstraint.MethodType.CREATE],
                condition="condition_value",
                action_type=constraint.CustomConstraint.ActionType.ALLOW,
                display_name="display_name_value",
                description="description_value",
            )
        )
        response = await client.get_custom_constraint(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == orgpolicy.GetCustomConstraintRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, constraint.CustomConstraint)
    assert response.name == "name_value"
    assert response.resource_types == ["resource_types_value"]
    assert response.method_types == [constraint.CustomConstraint.MethodType.CREATE]
    assert response.condition == "condition_value"
    assert response.action_type == constraint.CustomConstraint.ActionType.ALLOW
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"


@pytest.mark.asyncio
async def test_get_custom_constraint_async_from_dict():
    await test_get_custom_constraint_async(request_type=dict)


def test_get_custom_constraint_field_headers():
    client = OrgPolicyClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = orgpolicy.GetCustomConstraintRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_custom_constraint), "__call__"
    ) as call:
        call.return_value = constraint.CustomConstraint()
        client.get_custom_constraint(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_custom_constraint_field_headers_async():
    client = OrgPolicyAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = orgpolicy.GetCustomConstraintRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_custom_constraint), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            constraint.CustomConstraint()
        )
        await client.get_custom_constraint(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


def test_get_custom_constraint_flattened():
    client = OrgPolicyClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_custom_constraint), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = constraint.CustomConstraint()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_custom_constraint(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_custom_constraint_flattened_error():
    client = OrgPolicyClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_custom_constraint(
            orgpolicy.GetCustomConstraintRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_custom_constraint_flattened_async():
    client = OrgPolicyAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_custom_constraint), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = constraint.CustomConstraint()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            constraint.CustomConstraint()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_custom_constraint(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_get_custom_constraint_flattened_error_async():
    client = OrgPolicyAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_custom_constraint(
            orgpolicy.GetCustomConstraintRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        orgpolicy.ListCustomConstraintsRequest,
        dict,
    ],
)
def test_list_custom_constraints(request_type, transport: str = "grpc"):
    client = OrgPolicyClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_custom_constraints), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = orgpolicy.ListCustomConstraintsResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_custom_constraints(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == orgpolicy.ListCustomConstraintsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListCustomConstraintsPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_custom_constraints_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = OrgPolicyClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_custom_constraints), "__call__"
    ) as call:
        client.list_custom_constraints()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == orgpolicy.ListCustomConstraintsRequest()


@pytest.mark.asyncio
async def test_list_custom_constraints_async(
    transport: str = "grpc_asyncio", request_type=orgpolicy.ListCustomConstraintsRequest
):
    client = OrgPolicyAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_custom_constraints), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            orgpolicy.ListCustomConstraintsResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_custom_constraints(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == orgpolicy.ListCustomConstraintsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListCustomConstraintsAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_custom_constraints_async_from_dict():
    await test_list_custom_constraints_async(request_type=dict)


def test_list_custom_constraints_field_headers():
    client = OrgPolicyClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = orgpolicy.ListCustomConstraintsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_custom_constraints), "__call__"
    ) as call:
        call.return_value = orgpolicy.ListCustomConstraintsResponse()
        client.list_custom_constraints(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_custom_constraints_field_headers_async():
    client = OrgPolicyAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = orgpolicy.ListCustomConstraintsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_custom_constraints), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            orgpolicy.ListCustomConstraintsResponse()
        )
        await client.list_custom_constraints(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


def test_list_custom_constraints_flattened():
    client = OrgPolicyClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_custom_constraints), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = orgpolicy.ListCustomConstraintsResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_custom_constraints(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_custom_constraints_flattened_error():
    client = OrgPolicyClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_custom_constraints(
            orgpolicy.ListCustomConstraintsRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_custom_constraints_flattened_async():
    client = OrgPolicyAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_custom_constraints), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = orgpolicy.ListCustomConstraintsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            orgpolicy.ListCustomConstraintsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_custom_constraints(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_list_custom_constraints_flattened_error_async():
    client = OrgPolicyAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_custom_constraints(
            orgpolicy.ListCustomConstraintsRequest(),
            parent="parent_value",
        )


def test_list_custom_constraints_pager(transport_name: str = "grpc"):
    client = OrgPolicyClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_custom_constraints), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            orgpolicy.ListCustomConstraintsResponse(
                custom_constraints=[
                    constraint.CustomConstraint(),
                    constraint.CustomConstraint(),
                    constraint.CustomConstraint(),
                ],
                next_page_token="abc",
            ),
            orgpolicy.ListCustomConstraintsResponse(
                custom_constraints=[],
                next_page_token="def",
            ),
            orgpolicy.ListCustomConstraintsResponse(
                custom_constraints=[
                    constraint.CustomConstraint(),
                ],
                next_page_token="ghi",
            ),
            orgpolicy.ListCustomConstraintsResponse(
                custom_constraints=[
                    constraint.CustomConstraint(),
                    constraint.CustomConstraint(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_custom_constraints(request={})

        assert pager._metadata == metadata

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, constraint.CustomConstraint) for i in results)


def test_list_custom_constraints_pages(transport_name: str = "grpc"):
    client = OrgPolicyClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_custom_constraints), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            orgpolicy.ListCustomConstraintsResponse(
                custom_constraints=[
                    constraint.CustomConstraint(),
                    constraint.CustomConstraint(),
                    constraint.CustomConstraint(),
                ],
                next_page_token="abc",
            ),
            orgpolicy.ListCustomConstraintsResponse(
                custom_constraints=[],
                next_page_token="def",
            ),
            orgpolicy.ListCustomConstraintsResponse(
                custom_constraints=[
                    constraint.CustomConstraint(),
                ],
                next_page_token="ghi",
            ),
            orgpolicy.ListCustomConstraintsResponse(
                custom_constraints=[
                    constraint.CustomConstraint(),
                    constraint.CustomConstraint(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_custom_constraints(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_custom_constraints_async_pager():
    client = OrgPolicyAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_custom_constraints),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            orgpolicy.ListCustomConstraintsResponse(
                custom_constraints=[
                    constraint.CustomConstraint(),
                    constraint.CustomConstraint(),
                    constraint.CustomConstraint(),
                ],
                next_page_token="abc",
            ),
            orgpolicy.ListCustomConstraintsResponse(
                custom_constraints=[],
                next_page_token="def",
            ),
            orgpolicy.ListCustomConstraintsResponse(
                custom_constraints=[
                    constraint.CustomConstraint(),
                ],
                next_page_token="ghi",
            ),
            orgpolicy.ListCustomConstraintsResponse(
                custom_constraints=[
                    constraint.CustomConstraint(),
                    constraint.CustomConstraint(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_custom_constraints(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, constraint.CustomConstraint) for i in responses)


@pytest.mark.asyncio
async def test_list_custom_constraints_async_pages():
    client = OrgPolicyAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_custom_constraints),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            orgpolicy.ListCustomConstraintsResponse(
                custom_constraints=[
                    constraint.CustomConstraint(),
                    constraint.CustomConstraint(),
                    constraint.CustomConstraint(),
                ],
                next_page_token="abc",
            ),
            orgpolicy.ListCustomConstraintsResponse(
                custom_constraints=[],
                next_page_token="def",
            ),
            orgpolicy.ListCustomConstraintsResponse(
                custom_constraints=[
                    constraint.CustomConstraint(),
                ],
                next_page_token="ghi",
            ),
            orgpolicy.ListCustomConstraintsResponse(
                custom_constraints=[
                    constraint.CustomConstraint(),
                    constraint.CustomConstraint(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        # Workaround issue in python 3.9 related to code coverage by adding `# pragma: no branch`
        # See https://github.com/googleapis/gapic-generator-python/pull/1174#issuecomment-1025132372
        async for page_ in (  # pragma: no branch
            await client.list_custom_constraints(request={})
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        orgpolicy.DeleteCustomConstraintRequest,
        dict,
    ],
)
def test_delete_custom_constraint(request_type, transport: str = "grpc"):
    client = OrgPolicyClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_custom_constraint), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        response = client.delete_custom_constraint(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == orgpolicy.DeleteCustomConstraintRequest()

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_custom_constraint_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = OrgPolicyClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_custom_constraint), "__call__"
    ) as call:
        client.delete_custom_constraint()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == orgpolicy.DeleteCustomConstraintRequest()


@pytest.mark.asyncio
async def test_delete_custom_constraint_async(
    transport: str = "grpc_asyncio",
    request_type=orgpolicy.DeleteCustomConstraintRequest,
):
    client = OrgPolicyAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_custom_constraint), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        response = await client.delete_custom_constraint(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == orgpolicy.DeleteCustomConstraintRequest()

    # Establish that the response is the type that we expect.
    assert response is None


@pytest.mark.asyncio
async def test_delete_custom_constraint_async_from_dict():
    await test_delete_custom_constraint_async(request_type=dict)


def test_delete_custom_constraint_field_headers():
    client = OrgPolicyClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = orgpolicy.DeleteCustomConstraintRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_custom_constraint), "__call__"
    ) as call:
        call.return_value = None
        client.delete_custom_constraint(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_delete_custom_constraint_field_headers_async():
    client = OrgPolicyAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = orgpolicy.DeleteCustomConstraintRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_custom_constraint), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        await client.delete_custom_constraint(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


def test_delete_custom_constraint_flattened():
    client = OrgPolicyClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_custom_constraint), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_custom_constraint(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_delete_custom_constraint_flattened_error():
    client = OrgPolicyClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_custom_constraint(
            orgpolicy.DeleteCustomConstraintRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_custom_constraint_flattened_async():
    client = OrgPolicyAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_custom_constraint), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_custom_constraint(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_delete_custom_constraint_flattened_error_async():
    client = OrgPolicyAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_custom_constraint(
            orgpolicy.DeleteCustomConstraintRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        orgpolicy.ListConstraintsRequest,
        dict,
    ],
)
def test_list_constraints_rest(request_type):
    client = OrgPolicyClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = orgpolicy.ListConstraintsResponse(
            next_page_token="next_page_token_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = orgpolicy.ListConstraintsResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.list_constraints(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListConstraintsPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_constraints_rest_required_fields(
    request_type=orgpolicy.ListConstraintsRequest,
):
    transport_class = transports.OrgPolicyRestTransport

    request_init = {}
    request_init["parent"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(
            pb_request,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_constraints._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = "parent_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_constraints._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(
        (
            "page_size",
            "page_token",
        )
    )
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == "parent_value"

    client = OrgPolicyClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = orgpolicy.ListConstraintsResponse()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "get",
                "query_params": pb_request,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            # Convert return value to protobuf type
            return_value = orgpolicy.ListConstraintsResponse.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.list_constraints(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_list_constraints_rest_unset_required_fields():
    transport = transports.OrgPolicyRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.list_constraints._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(
            (
                "pageSize",
                "pageToken",
            )
        )
        & set(("parent",))
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_list_constraints_rest_interceptors(null_interceptor):
    transport = transports.OrgPolicyRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.OrgPolicyRestInterceptor(),
    )
    client = OrgPolicyClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.OrgPolicyRestInterceptor, "post_list_constraints"
    ) as post, mock.patch.object(
        transports.OrgPolicyRestInterceptor, "pre_list_constraints"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = orgpolicy.ListConstraintsRequest.pb(
            orgpolicy.ListConstraintsRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = orgpolicy.ListConstraintsResponse.to_json(
            orgpolicy.ListConstraintsResponse()
        )

        request = orgpolicy.ListConstraintsRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = orgpolicy.ListConstraintsResponse()

        client.list_constraints(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_list_constraints_rest_bad_request(
    transport: str = "rest", request_type=orgpolicy.ListConstraintsRequest
):
    client = OrgPolicyClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.list_constraints(request)


def test_list_constraints_rest_flattened():
    client = OrgPolicyClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = orgpolicy.ListConstraintsResponse()

        # get arguments that satisfy an http rule for this method
        sample_request = {"parent": "projects/sample1"}

        # get truthy value for each flattened field
        mock_args = dict(
            parent="parent_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = orgpolicy.ListConstraintsResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.list_constraints(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v2/{parent=projects/*}/constraints" % client.transport._host, args[1]
        )


def test_list_constraints_rest_flattened_error(transport: str = "rest"):
    client = OrgPolicyClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_constraints(
            orgpolicy.ListConstraintsRequest(),
            parent="parent_value",
        )


def test_list_constraints_rest_pager(transport: str = "rest"):
    client = OrgPolicyClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # TODO(kbandes): remove this mock unless there's a good reason for it.
        # with mock.patch.object(path_template, 'transcode') as transcode:
        # Set the response as a series of pages
        response = (
            orgpolicy.ListConstraintsResponse(
                constraints=[
                    constraint.Constraint(),
                    constraint.Constraint(),
                    constraint.Constraint(),
                ],
                next_page_token="abc",
            ),
            orgpolicy.ListConstraintsResponse(
                constraints=[],
                next_page_token="def",
            ),
            orgpolicy.ListConstraintsResponse(
                constraints=[
                    constraint.Constraint(),
                ],
                next_page_token="ghi",
            ),
            orgpolicy.ListConstraintsResponse(
                constraints=[
                    constraint.Constraint(),
                    constraint.Constraint(),
                ],
            ),
        )
        # Two responses for two calls
        response = response + response

        # Wrap the values into proper Response objs
        response = tuple(orgpolicy.ListConstraintsResponse.to_json(x) for x in response)
        return_values = tuple(Response() for i in response)
        for return_val, response_val in zip(return_values, response):
            return_val._content = response_val.encode("UTF-8")
            return_val.status_code = 200
        req.side_effect = return_values

        sample_request = {"parent": "projects/sample1"}

        pager = client.list_constraints(request=sample_request)

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, constraint.Constraint) for i in results)

        pages = list(client.list_constraints(request=sample_request).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        orgpolicy.ListPoliciesRequest,
        dict,
    ],
)
def test_list_policies_rest(request_type):
    client = OrgPolicyClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = orgpolicy.ListPoliciesResponse(
            next_page_token="next_page_token_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = orgpolicy.ListPoliciesResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.list_policies(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListPoliciesPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_policies_rest_required_fields(request_type=orgpolicy.ListPoliciesRequest):
    transport_class = transports.OrgPolicyRestTransport

    request_init = {}
    request_init["parent"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(
            pb_request,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_policies._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = "parent_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_policies._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(
        (
            "page_size",
            "page_token",
        )
    )
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == "parent_value"

    client = OrgPolicyClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = orgpolicy.ListPoliciesResponse()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "get",
                "query_params": pb_request,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            # Convert return value to protobuf type
            return_value = orgpolicy.ListPoliciesResponse.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.list_policies(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_list_policies_rest_unset_required_fields():
    transport = transports.OrgPolicyRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.list_policies._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(
            (
                "pageSize",
                "pageToken",
            )
        )
        & set(("parent",))
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_list_policies_rest_interceptors(null_interceptor):
    transport = transports.OrgPolicyRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.OrgPolicyRestInterceptor(),
    )
    client = OrgPolicyClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.OrgPolicyRestInterceptor, "post_list_policies"
    ) as post, mock.patch.object(
        transports.OrgPolicyRestInterceptor, "pre_list_policies"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = orgpolicy.ListPoliciesRequest.pb(orgpolicy.ListPoliciesRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = orgpolicy.ListPoliciesResponse.to_json(
            orgpolicy.ListPoliciesResponse()
        )

        request = orgpolicy.ListPoliciesRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = orgpolicy.ListPoliciesResponse()

        client.list_policies(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_list_policies_rest_bad_request(
    transport: str = "rest", request_type=orgpolicy.ListPoliciesRequest
):
    client = OrgPolicyClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.list_policies(request)


def test_list_policies_rest_flattened():
    client = OrgPolicyClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = orgpolicy.ListPoliciesResponse()

        # get arguments that satisfy an http rule for this method
        sample_request = {"parent": "projects/sample1"}

        # get truthy value for each flattened field
        mock_args = dict(
            parent="parent_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = orgpolicy.ListPoliciesResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.list_policies(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v2/{parent=projects/*}/policies" % client.transport._host, args[1]
        )


def test_list_policies_rest_flattened_error(transport: str = "rest"):
    client = OrgPolicyClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_policies(
            orgpolicy.ListPoliciesRequest(),
            parent="parent_value",
        )


def test_list_policies_rest_pager(transport: str = "rest"):
    client = OrgPolicyClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # TODO(kbandes): remove this mock unless there's a good reason for it.
        # with mock.patch.object(path_template, 'transcode') as transcode:
        # Set the response as a series of pages
        response = (
            orgpolicy.ListPoliciesResponse(
                policies=[
                    orgpolicy.Policy(),
                    orgpolicy.Policy(),
                    orgpolicy.Policy(),
                ],
                next_page_token="abc",
            ),
            orgpolicy.ListPoliciesResponse(
                policies=[],
                next_page_token="def",
            ),
            orgpolicy.ListPoliciesResponse(
                policies=[
                    orgpolicy.Policy(),
                ],
                next_page_token="ghi",
            ),
            orgpolicy.ListPoliciesResponse(
                policies=[
                    orgpolicy.Policy(),
                    orgpolicy.Policy(),
                ],
            ),
        )
        # Two responses for two calls
        response = response + response

        # Wrap the values into proper Response objs
        response = tuple(orgpolicy.ListPoliciesResponse.to_json(x) for x in response)
        return_values = tuple(Response() for i in response)
        for return_val, response_val in zip(return_values, response):
            return_val._content = response_val.encode("UTF-8")
            return_val.status_code = 200
        req.side_effect = return_values

        sample_request = {"parent": "projects/sample1"}

        pager = client.list_policies(request=sample_request)

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, orgpolicy.Policy) for i in results)

        pages = list(client.list_policies(request=sample_request).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        orgpolicy.GetPolicyRequest,
        dict,
    ],
)
def test_get_policy_rest(request_type):
    client = OrgPolicyClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/policies/sample2"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = orgpolicy.Policy(
            name="name_value",
            etag="etag_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = orgpolicy.Policy.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.get_policy(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, orgpolicy.Policy)
    assert response.name == "name_value"
    assert response.etag == "etag_value"


def test_get_policy_rest_required_fields(request_type=orgpolicy.GetPolicyRequest):
    transport_class = transports.OrgPolicyRestTransport

    request_init = {}
    request_init["name"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(
            pb_request,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get_policy._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get_policy._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = OrgPolicyClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = orgpolicy.Policy()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "get",
                "query_params": pb_request,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            # Convert return value to protobuf type
            return_value = orgpolicy.Policy.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.get_policy(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_get_policy_rest_unset_required_fields():
    transport = transports.OrgPolicyRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.get_policy._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_get_policy_rest_interceptors(null_interceptor):
    transport = transports.OrgPolicyRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.OrgPolicyRestInterceptor(),
    )
    client = OrgPolicyClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.OrgPolicyRestInterceptor, "post_get_policy"
    ) as post, mock.patch.object(
        transports.OrgPolicyRestInterceptor, "pre_get_policy"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = orgpolicy.GetPolicyRequest.pb(orgpolicy.GetPolicyRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = orgpolicy.Policy.to_json(orgpolicy.Policy())

        request = orgpolicy.GetPolicyRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = orgpolicy.Policy()

        client.get_policy(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_get_policy_rest_bad_request(
    transport: str = "rest", request_type=orgpolicy.GetPolicyRequest
):
    client = OrgPolicyClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/policies/sample2"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.get_policy(request)


def test_get_policy_rest_flattened():
    client = OrgPolicyClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = orgpolicy.Policy()

        # get arguments that satisfy an http rule for this method
        sample_request = {"name": "projects/sample1/policies/sample2"}

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = orgpolicy.Policy.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.get_policy(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v2/{name=projects/*/policies/*}" % client.transport._host, args[1]
        )


def test_get_policy_rest_flattened_error(transport: str = "rest"):
    client = OrgPolicyClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_policy(
            orgpolicy.GetPolicyRequest(),
            name="name_value",
        )


def test_get_policy_rest_error():
    client = OrgPolicyClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        orgpolicy.GetEffectivePolicyRequest,
        dict,
    ],
)
def test_get_effective_policy_rest(request_type):
    client = OrgPolicyClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/policies/sample2"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = orgpolicy.Policy(
            name="name_value",
            etag="etag_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = orgpolicy.Policy.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.get_effective_policy(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, orgpolicy.Policy)
    assert response.name == "name_value"
    assert response.etag == "etag_value"


def test_get_effective_policy_rest_required_fields(
    request_type=orgpolicy.GetEffectivePolicyRequest,
):
    transport_class = transports.OrgPolicyRestTransport

    request_init = {}
    request_init["name"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(
            pb_request,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get_effective_policy._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get_effective_policy._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = OrgPolicyClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = orgpolicy.Policy()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "get",
                "query_params": pb_request,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            # Convert return value to protobuf type
            return_value = orgpolicy.Policy.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.get_effective_policy(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_get_effective_policy_rest_unset_required_fields():
    transport = transports.OrgPolicyRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.get_effective_policy._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_get_effective_policy_rest_interceptors(null_interceptor):
    transport = transports.OrgPolicyRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.OrgPolicyRestInterceptor(),
    )
    client = OrgPolicyClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.OrgPolicyRestInterceptor, "post_get_effective_policy"
    ) as post, mock.patch.object(
        transports.OrgPolicyRestInterceptor, "pre_get_effective_policy"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = orgpolicy.GetEffectivePolicyRequest.pb(
            orgpolicy.GetEffectivePolicyRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = orgpolicy.Policy.to_json(orgpolicy.Policy())

        request = orgpolicy.GetEffectivePolicyRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = orgpolicy.Policy()

        client.get_effective_policy(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_get_effective_policy_rest_bad_request(
    transport: str = "rest", request_type=orgpolicy.GetEffectivePolicyRequest
):
    client = OrgPolicyClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/policies/sample2"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.get_effective_policy(request)


def test_get_effective_policy_rest_flattened():
    client = OrgPolicyClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = orgpolicy.Policy()

        # get arguments that satisfy an http rule for this method
        sample_request = {"name": "projects/sample1/policies/sample2"}

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = orgpolicy.Policy.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.get_effective_policy(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v2/{name=projects/*/policies/*}:getEffectivePolicy"
            % client.transport._host,
            args[1],
        )


def test_get_effective_policy_rest_flattened_error(transport: str = "rest"):
    client = OrgPolicyClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_effective_policy(
            orgpolicy.GetEffectivePolicyRequest(),
            name="name_value",
        )


def test_get_effective_policy_rest_error():
    client = OrgPolicyClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        orgpolicy.CreatePolicyRequest,
        dict,
    ],
)
def test_create_policy_rest(request_type):
    client = OrgPolicyClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1"}
    request_init["policy"] = {
        "name": "name_value",
        "spec": {
            "etag": "etag_value",
            "update_time": {"seconds": 751, "nanos": 543},
            "rules": [
                {
                    "values": {
                        "allowed_values": [
                            "allowed_values_value1",
                            "allowed_values_value2",
                        ],
                        "denied_values": [
                            "denied_values_value1",
                            "denied_values_value2",
                        ],
                    },
                    "allow_all": True,
                    "deny_all": True,
                    "enforce": True,
                    "condition": {
                        "expression": "expression_value",
                        "title": "title_value",
                        "description": "description_value",
                        "location": "location_value",
                    },
                }
            ],
            "inherit_from_parent": True,
            "reset": True,
        },
        "alternate": {"launch": "launch_value", "spec": {}},
        "dry_run_spec": {},
        "etag": "etag_value",
    }
    # The version of a generated dependency at test runtime may differ from the version used during generation.
    # Delete any fields which are not present in the current runtime dependency
    # See https://github.com/googleapis/gapic-generator-python/issues/1748

    # Determine if the message type is proto-plus or protobuf
    test_field = orgpolicy.CreatePolicyRequest.meta.fields["policy"]

    def get_message_fields(field):
        # Given a field which is a message (composite type), return a list with
        # all the fields of the message.
        # If the field is not a composite type, return an empty list.
        message_fields = []

        if hasattr(field, "message") and field.message:
            is_field_type_proto_plus_type = not hasattr(field.message, "DESCRIPTOR")

            if is_field_type_proto_plus_type:
                message_fields = field.message.meta.fields.values()
            # Add `# pragma: NO COVER` because there may not be any `*_pb2` field types
            else:  # pragma: NO COVER
                message_fields = field.message.DESCRIPTOR.fields
        return message_fields

    runtime_nested_fields = [
        (field.name, nested_field.name)
        for field in get_message_fields(test_field)
        for nested_field in get_message_fields(field)
    ]

    subfields_not_in_runtime = []

    # For each item in the sample request, create a list of sub fields which are not present at runtime
    # Add `# pragma: NO COVER` because this test code will not run if all subfields are present at runtime
    for field, value in request_init["policy"].items():  # pragma: NO COVER
        result = None
        is_repeated = False
        # For repeated fields
        if isinstance(value, list) and len(value):
            is_repeated = True
            result = value[0]
        # For fields where the type is another message
        if isinstance(value, dict):
            result = value

        if result and hasattr(result, "keys"):
            for subfield in result.keys():
                if (field, subfield) not in runtime_nested_fields:
                    subfields_not_in_runtime.append(
                        {
                            "field": field,
                            "subfield": subfield,
                            "is_repeated": is_repeated,
                        }
                    )

    # Remove fields from the sample request which are not present in the runtime version of the dependency
    # Add `# pragma: NO COVER` because this test code will not run if all subfields are present at runtime
    for subfield_to_delete in subfields_not_in_runtime:  # pragma: NO COVER
        field = subfield_to_delete.get("field")
        field_repeated = subfield_to_delete.get("is_repeated")
        subfield = subfield_to_delete.get("subfield")
        if subfield:
            if field_repeated:
                for i in range(0, len(request_init["policy"][field])):
                    del request_init["policy"][field][i][subfield]
            else:
                del request_init["policy"][field][subfield]
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = orgpolicy.Policy(
            name="name_value",
            etag="etag_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = orgpolicy.Policy.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.create_policy(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, orgpolicy.Policy)
    assert response.name == "name_value"
    assert response.etag == "etag_value"


def test_create_policy_rest_required_fields(request_type=orgpolicy.CreatePolicyRequest):
    transport_class = transports.OrgPolicyRestTransport

    request_init = {}
    request_init["parent"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(
            pb_request,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).create_policy._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = "parent_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).create_policy._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == "parent_value"

    client = OrgPolicyClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = orgpolicy.Policy()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "post",
                "query_params": pb_request,
            }
            transcode_result["body"] = pb_request
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            # Convert return value to protobuf type
            return_value = orgpolicy.Policy.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.create_policy(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_create_policy_rest_unset_required_fields():
    transport = transports.OrgPolicyRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.create_policy._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(())
        & set(
            (
                "parent",
                "policy",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_create_policy_rest_interceptors(null_interceptor):
    transport = transports.OrgPolicyRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.OrgPolicyRestInterceptor(),
    )
    client = OrgPolicyClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.OrgPolicyRestInterceptor, "post_create_policy"
    ) as post, mock.patch.object(
        transports.OrgPolicyRestInterceptor, "pre_create_policy"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = orgpolicy.CreatePolicyRequest.pb(orgpolicy.CreatePolicyRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = orgpolicy.Policy.to_json(orgpolicy.Policy())

        request = orgpolicy.CreatePolicyRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = orgpolicy.Policy()

        client.create_policy(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_create_policy_rest_bad_request(
    transport: str = "rest", request_type=orgpolicy.CreatePolicyRequest
):
    client = OrgPolicyClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.create_policy(request)


def test_create_policy_rest_flattened():
    client = OrgPolicyClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = orgpolicy.Policy()

        # get arguments that satisfy an http rule for this method
        sample_request = {"parent": "projects/sample1"}

        # get truthy value for each flattened field
        mock_args = dict(
            parent="parent_value",
            policy=orgpolicy.Policy(name="name_value"),
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = orgpolicy.Policy.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.create_policy(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v2/{parent=projects/*}/policies" % client.transport._host, args[1]
        )


def test_create_policy_rest_flattened_error(transport: str = "rest"):
    client = OrgPolicyClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_policy(
            orgpolicy.CreatePolicyRequest(),
            parent="parent_value",
            policy=orgpolicy.Policy(name="name_value"),
        )


def test_create_policy_rest_error():
    client = OrgPolicyClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        orgpolicy.UpdatePolicyRequest,
        dict,
    ],
)
def test_update_policy_rest(request_type):
    client = OrgPolicyClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"policy": {"name": "projects/sample1/policies/sample2"}}
    request_init["policy"] = {
        "name": "projects/sample1/policies/sample2",
        "spec": {
            "etag": "etag_value",
            "update_time": {"seconds": 751, "nanos": 543},
            "rules": [
                {
                    "values": {
                        "allowed_values": [
                            "allowed_values_value1",
                            "allowed_values_value2",
                        ],
                        "denied_values": [
                            "denied_values_value1",
                            "denied_values_value2",
                        ],
                    },
                    "allow_all": True,
                    "deny_all": True,
                    "enforce": True,
                    "condition": {
                        "expression": "expression_value",
                        "title": "title_value",
                        "description": "description_value",
                        "location": "location_value",
                    },
                }
            ],
            "inherit_from_parent": True,
            "reset": True,
        },
        "alternate": {"launch": "launch_value", "spec": {}},
        "dry_run_spec": {},
        "etag": "etag_value",
    }
    # The version of a generated dependency at test runtime may differ from the version used during generation.
    # Delete any fields which are not present in the current runtime dependency
    # See https://github.com/googleapis/gapic-generator-python/issues/1748

    # Determine if the message type is proto-plus or protobuf
    test_field = orgpolicy.UpdatePolicyRequest.meta.fields["policy"]

    def get_message_fields(field):
        # Given a field which is a message (composite type), return a list with
        # all the fields of the message.
        # If the field is not a composite type, return an empty list.
        message_fields = []

        if hasattr(field, "message") and field.message:
            is_field_type_proto_plus_type = not hasattr(field.message, "DESCRIPTOR")

            if is_field_type_proto_plus_type:
                message_fields = field.message.meta.fields.values()
            # Add `# pragma: NO COVER` because there may not be any `*_pb2` field types
            else:  # pragma: NO COVER
                message_fields = field.message.DESCRIPTOR.fields
        return message_fields

    runtime_nested_fields = [
        (field.name, nested_field.name)
        for field in get_message_fields(test_field)
        for nested_field in get_message_fields(field)
    ]

    subfields_not_in_runtime = []

    # For each item in the sample request, create a list of sub fields which are not present at runtime
    # Add `# pragma: NO COVER` because this test code will not run if all subfields are present at runtime
    for field, value in request_init["policy"].items():  # pragma: NO COVER
        result = None
        is_repeated = False
        # For repeated fields
        if isinstance(value, list) and len(value):
            is_repeated = True
            result = value[0]
        # For fields where the type is another message
        if isinstance(value, dict):
            result = value

        if result and hasattr(result, "keys"):
            for subfield in result.keys():
                if (field, subfield) not in runtime_nested_fields:
                    subfields_not_in_runtime.append(
                        {
                            "field": field,
                            "subfield": subfield,
                            "is_repeated": is_repeated,
                        }
                    )

    # Remove fields from the sample request which are not present in the runtime version of the dependency
    # Add `# pragma: NO COVER` because this test code will not run if all subfields are present at runtime
    for subfield_to_delete in subfields_not_in_runtime:  # pragma: NO COVER
        field = subfield_to_delete.get("field")
        field_repeated = subfield_to_delete.get("is_repeated")
        subfield = subfield_to_delete.get("subfield")
        if subfield:
            if field_repeated:
                for i in range(0, len(request_init["policy"][field])):
                    del request_init["policy"][field][i][subfield]
            else:
                del request_init["policy"][field][subfield]
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = orgpolicy.Policy(
            name="name_value",
            etag="etag_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = orgpolicy.Policy.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.update_policy(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, orgpolicy.Policy)
    assert response.name == "name_value"
    assert response.etag == "etag_value"


def test_update_policy_rest_required_fields(request_type=orgpolicy.UpdatePolicyRequest):
    transport_class = transports.OrgPolicyRestTransport

    request_init = {}
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(
            pb_request,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).update_policy._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).update_policy._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("update_mask",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone

    client = OrgPolicyClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = orgpolicy.Policy()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "patch",
                "query_params": pb_request,
            }
            transcode_result["body"] = pb_request
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            # Convert return value to protobuf type
            return_value = orgpolicy.Policy.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.update_policy(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_update_policy_rest_unset_required_fields():
    transport = transports.OrgPolicyRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.update_policy._get_unset_required_fields({})
    assert set(unset_fields) == (set(("updateMask",)) & set(("policy",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_update_policy_rest_interceptors(null_interceptor):
    transport = transports.OrgPolicyRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.OrgPolicyRestInterceptor(),
    )
    client = OrgPolicyClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.OrgPolicyRestInterceptor, "post_update_policy"
    ) as post, mock.patch.object(
        transports.OrgPolicyRestInterceptor, "pre_update_policy"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = orgpolicy.UpdatePolicyRequest.pb(orgpolicy.UpdatePolicyRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = orgpolicy.Policy.to_json(orgpolicy.Policy())

        request = orgpolicy.UpdatePolicyRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = orgpolicy.Policy()

        client.update_policy(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_update_policy_rest_bad_request(
    transport: str = "rest", request_type=orgpolicy.UpdatePolicyRequest
):
    client = OrgPolicyClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"policy": {"name": "projects/sample1/policies/sample2"}}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.update_policy(request)


def test_update_policy_rest_flattened():
    client = OrgPolicyClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = orgpolicy.Policy()

        # get arguments that satisfy an http rule for this method
        sample_request = {"policy": {"name": "projects/sample1/policies/sample2"}}

        # get truthy value for each flattened field
        mock_args = dict(
            policy=orgpolicy.Policy(name="name_value"),
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = orgpolicy.Policy.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.update_policy(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v2/{policy.name=projects/*/policies/*}" % client.transport._host,
            args[1],
        )


def test_update_policy_rest_flattened_error(transport: str = "rest"):
    client = OrgPolicyClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_policy(
            orgpolicy.UpdatePolicyRequest(),
            policy=orgpolicy.Policy(name="name_value"),
        )


def test_update_policy_rest_error():
    client = OrgPolicyClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        orgpolicy.DeletePolicyRequest,
        dict,
    ],
)
def test_delete_policy_rest(request_type):
    client = OrgPolicyClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/policies/sample2"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = None

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = ""

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.delete_policy(request)

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_policy_rest_required_fields(request_type=orgpolicy.DeletePolicyRequest):
    transport_class = transports.OrgPolicyRestTransport

    request_init = {}
    request_init["name"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(
            pb_request,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).delete_policy._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).delete_policy._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("etag",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = OrgPolicyClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = None
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "delete",
                "query_params": pb_request,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200
            json_return_value = ""

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.delete_policy(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_delete_policy_rest_unset_required_fields():
    transport = transports.OrgPolicyRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.delete_policy._get_unset_required_fields({})
    assert set(unset_fields) == (set(("etag",)) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_delete_policy_rest_interceptors(null_interceptor):
    transport = transports.OrgPolicyRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.OrgPolicyRestInterceptor(),
    )
    client = OrgPolicyClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.OrgPolicyRestInterceptor, "pre_delete_policy"
    ) as pre:
        pre.assert_not_called()
        pb_message = orgpolicy.DeletePolicyRequest.pb(orgpolicy.DeletePolicyRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()

        request = orgpolicy.DeletePolicyRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata

        client.delete_policy(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()


def test_delete_policy_rest_bad_request(
    transport: str = "rest", request_type=orgpolicy.DeletePolicyRequest
):
    client = OrgPolicyClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/policies/sample2"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.delete_policy(request)


def test_delete_policy_rest_flattened():
    client = OrgPolicyClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = None

        # get arguments that satisfy an http rule for this method
        sample_request = {"name": "projects/sample1/policies/sample2"}

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = ""
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.delete_policy(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v2/{name=projects/*/policies/*}" % client.transport._host, args[1]
        )


def test_delete_policy_rest_flattened_error(transport: str = "rest"):
    client = OrgPolicyClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_policy(
            orgpolicy.DeletePolicyRequest(),
            name="name_value",
        )


def test_delete_policy_rest_error():
    client = OrgPolicyClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        orgpolicy.CreateCustomConstraintRequest,
        dict,
    ],
)
def test_create_custom_constraint_rest(request_type):
    client = OrgPolicyClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "organizations/sample1"}
    request_init["custom_constraint"] = {
        "name": "name_value",
        "resource_types": ["resource_types_value1", "resource_types_value2"],
        "method_types": [1],
        "condition": "condition_value",
        "action_type": 1,
        "display_name": "display_name_value",
        "description": "description_value",
        "update_time": {"seconds": 751, "nanos": 543},
    }
    # The version of a generated dependency at test runtime may differ from the version used during generation.
    # Delete any fields which are not present in the current runtime dependency
    # See https://github.com/googleapis/gapic-generator-python/issues/1748

    # Determine if the message type is proto-plus or protobuf
    test_field = orgpolicy.CreateCustomConstraintRequest.meta.fields[
        "custom_constraint"
    ]

    def get_message_fields(field):
        # Given a field which is a message (composite type), return a list with
        # all the fields of the message.
        # If the field is not a composite type, return an empty list.
        message_fields = []

        if hasattr(field, "message") and field.message:
            is_field_type_proto_plus_type = not hasattr(field.message, "DESCRIPTOR")

            if is_field_type_proto_plus_type:
                message_fields = field.message.meta.fields.values()
            # Add `# pragma: NO COVER` because there may not be any `*_pb2` field types
            else:  # pragma: NO COVER
                message_fields = field.message.DESCRIPTOR.fields
        return message_fields

    runtime_nested_fields = [
        (field.name, nested_field.name)
        for field in get_message_fields(test_field)
        for nested_field in get_message_fields(field)
    ]

    subfields_not_in_runtime = []

    # For each item in the sample request, create a list of sub fields which are not present at runtime
    # Add `# pragma: NO COVER` because this test code will not run if all subfields are present at runtime
    for field, value in request_init["custom_constraint"].items():  # pragma: NO COVER
        result = None
        is_repeated = False
        # For repeated fields
        if isinstance(value, list) and len(value):
            is_repeated = True
            result = value[0]
        # For fields where the type is another message
        if isinstance(value, dict):
            result = value

        if result and hasattr(result, "keys"):
            for subfield in result.keys():
                if (field, subfield) not in runtime_nested_fields:
                    subfields_not_in_runtime.append(
                        {
                            "field": field,
                            "subfield": subfield,
                            "is_repeated": is_repeated,
                        }
                    )

    # Remove fields from the sample request which are not present in the runtime version of the dependency
    # Add `# pragma: NO COVER` because this test code will not run if all subfields are present at runtime
    for subfield_to_delete in subfields_not_in_runtime:  # pragma: NO COVER
        field = subfield_to_delete.get("field")
        field_repeated = subfield_to_delete.get("is_repeated")
        subfield = subfield_to_delete.get("subfield")
        if subfield:
            if field_repeated:
                for i in range(0, len(request_init["custom_constraint"][field])):
                    del request_init["custom_constraint"][field][i][subfield]
            else:
                del request_init["custom_constraint"][field][subfield]
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = constraint.CustomConstraint(
            name="name_value",
            resource_types=["resource_types_value"],
            method_types=[constraint.CustomConstraint.MethodType.CREATE],
            condition="condition_value",
            action_type=constraint.CustomConstraint.ActionType.ALLOW,
            display_name="display_name_value",
            description="description_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = constraint.CustomConstraint.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.create_custom_constraint(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, constraint.CustomConstraint)
    assert response.name == "name_value"
    assert response.resource_types == ["resource_types_value"]
    assert response.method_types == [constraint.CustomConstraint.MethodType.CREATE]
    assert response.condition == "condition_value"
    assert response.action_type == constraint.CustomConstraint.ActionType.ALLOW
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"


def test_create_custom_constraint_rest_required_fields(
    request_type=orgpolicy.CreateCustomConstraintRequest,
):
    transport_class = transports.OrgPolicyRestTransport

    request_init = {}
    request_init["parent"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(
            pb_request,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).create_custom_constraint._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = "parent_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).create_custom_constraint._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == "parent_value"

    client = OrgPolicyClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = constraint.CustomConstraint()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "post",
                "query_params": pb_request,
            }
            transcode_result["body"] = pb_request
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            # Convert return value to protobuf type
            return_value = constraint.CustomConstraint.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.create_custom_constraint(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_create_custom_constraint_rest_unset_required_fields():
    transport = transports.OrgPolicyRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.create_custom_constraint._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(())
        & set(
            (
                "parent",
                "customConstraint",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_create_custom_constraint_rest_interceptors(null_interceptor):
    transport = transports.OrgPolicyRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.OrgPolicyRestInterceptor(),
    )
    client = OrgPolicyClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.OrgPolicyRestInterceptor, "post_create_custom_constraint"
    ) as post, mock.patch.object(
        transports.OrgPolicyRestInterceptor, "pre_create_custom_constraint"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = orgpolicy.CreateCustomConstraintRequest.pb(
            orgpolicy.CreateCustomConstraintRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = constraint.CustomConstraint.to_json(
            constraint.CustomConstraint()
        )

        request = orgpolicy.CreateCustomConstraintRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = constraint.CustomConstraint()

        client.create_custom_constraint(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_create_custom_constraint_rest_bad_request(
    transport: str = "rest", request_type=orgpolicy.CreateCustomConstraintRequest
):
    client = OrgPolicyClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "organizations/sample1"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.create_custom_constraint(request)


def test_create_custom_constraint_rest_flattened():
    client = OrgPolicyClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = constraint.CustomConstraint()

        # get arguments that satisfy an http rule for this method
        sample_request = {"parent": "organizations/sample1"}

        # get truthy value for each flattened field
        mock_args = dict(
            parent="parent_value",
            custom_constraint=constraint.CustomConstraint(name="name_value"),
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = constraint.CustomConstraint.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.create_custom_constraint(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v2/{parent=organizations/*}/customConstraints" % client.transport._host,
            args[1],
        )


def test_create_custom_constraint_rest_flattened_error(transport: str = "rest"):
    client = OrgPolicyClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_custom_constraint(
            orgpolicy.CreateCustomConstraintRequest(),
            parent="parent_value",
            custom_constraint=constraint.CustomConstraint(name="name_value"),
        )


def test_create_custom_constraint_rest_error():
    client = OrgPolicyClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        orgpolicy.UpdateCustomConstraintRequest,
        dict,
    ],
)
def test_update_custom_constraint_rest(request_type):
    client = OrgPolicyClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "custom_constraint": {"name": "organizations/sample1/customConstraints/sample2"}
    }
    request_init["custom_constraint"] = {
        "name": "organizations/sample1/customConstraints/sample2",
        "resource_types": ["resource_types_value1", "resource_types_value2"],
        "method_types": [1],
        "condition": "condition_value",
        "action_type": 1,
        "display_name": "display_name_value",
        "description": "description_value",
        "update_time": {"seconds": 751, "nanos": 543},
    }
    # The version of a generated dependency at test runtime may differ from the version used during generation.
    # Delete any fields which are not present in the current runtime dependency
    # See https://github.com/googleapis/gapic-generator-python/issues/1748

    # Determine if the message type is proto-plus or protobuf
    test_field = orgpolicy.UpdateCustomConstraintRequest.meta.fields[
        "custom_constraint"
    ]

    def get_message_fields(field):
        # Given a field which is a message (composite type), return a list with
        # all the fields of the message.
        # If the field is not a composite type, return an empty list.
        message_fields = []

        if hasattr(field, "message") and field.message:
            is_field_type_proto_plus_type = not hasattr(field.message, "DESCRIPTOR")

            if is_field_type_proto_plus_type:
                message_fields = field.message.meta.fields.values()
            # Add `# pragma: NO COVER` because there may not be any `*_pb2` field types
            else:  # pragma: NO COVER
                message_fields = field.message.DESCRIPTOR.fields
        return message_fields

    runtime_nested_fields = [
        (field.name, nested_field.name)
        for field in get_message_fields(test_field)
        for nested_field in get_message_fields(field)
    ]

    subfields_not_in_runtime = []

    # For each item in the sample request, create a list of sub fields which are not present at runtime
    # Add `# pragma: NO COVER` because this test code will not run if all subfields are present at runtime
    for field, value in request_init["custom_constraint"].items():  # pragma: NO COVER
        result = None
        is_repeated = False
        # For repeated fields
        if isinstance(value, list) and len(value):
            is_repeated = True
            result = value[0]
        # For fields where the type is another message
        if isinstance(value, dict):
            result = value

        if result and hasattr(result, "keys"):
            for subfield in result.keys():
                if (field, subfield) not in runtime_nested_fields:
                    subfields_not_in_runtime.append(
                        {
                            "field": field,
                            "subfield": subfield,
                            "is_repeated": is_repeated,
                        }
                    )

    # Remove fields from the sample request which are not present in the runtime version of the dependency
    # Add `# pragma: NO COVER` because this test code will not run if all subfields are present at runtime
    for subfield_to_delete in subfields_not_in_runtime:  # pragma: NO COVER
        field = subfield_to_delete.get("field")
        field_repeated = subfield_to_delete.get("is_repeated")
        subfield = subfield_to_delete.get("subfield")
        if subfield:
            if field_repeated:
                for i in range(0, len(request_init["custom_constraint"][field])):
                    del request_init["custom_constraint"][field][i][subfield]
            else:
                del request_init["custom_constraint"][field][subfield]
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = constraint.CustomConstraint(
            name="name_value",
            resource_types=["resource_types_value"],
            method_types=[constraint.CustomConstraint.MethodType.CREATE],
            condition="condition_value",
            action_type=constraint.CustomConstraint.ActionType.ALLOW,
            display_name="display_name_value",
            description="description_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = constraint.CustomConstraint.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.update_custom_constraint(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, constraint.CustomConstraint)
    assert response.name == "name_value"
    assert response.resource_types == ["resource_types_value"]
    assert response.method_types == [constraint.CustomConstraint.MethodType.CREATE]
    assert response.condition == "condition_value"
    assert response.action_type == constraint.CustomConstraint.ActionType.ALLOW
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"


def test_update_custom_constraint_rest_required_fields(
    request_type=orgpolicy.UpdateCustomConstraintRequest,
):
    transport_class = transports.OrgPolicyRestTransport

    request_init = {}
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(
            pb_request,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).update_custom_constraint._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).update_custom_constraint._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone

    client = OrgPolicyClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = constraint.CustomConstraint()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "patch",
                "query_params": pb_request,
            }
            transcode_result["body"] = pb_request
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            # Convert return value to protobuf type
            return_value = constraint.CustomConstraint.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.update_custom_constraint(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_update_custom_constraint_rest_unset_required_fields():
    transport = transports.OrgPolicyRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.update_custom_constraint._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("customConstraint",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_update_custom_constraint_rest_interceptors(null_interceptor):
    transport = transports.OrgPolicyRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.OrgPolicyRestInterceptor(),
    )
    client = OrgPolicyClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.OrgPolicyRestInterceptor, "post_update_custom_constraint"
    ) as post, mock.patch.object(
        transports.OrgPolicyRestInterceptor, "pre_update_custom_constraint"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = orgpolicy.UpdateCustomConstraintRequest.pb(
            orgpolicy.UpdateCustomConstraintRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = constraint.CustomConstraint.to_json(
            constraint.CustomConstraint()
        )

        request = orgpolicy.UpdateCustomConstraintRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = constraint.CustomConstraint()

        client.update_custom_constraint(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_update_custom_constraint_rest_bad_request(
    transport: str = "rest", request_type=orgpolicy.UpdateCustomConstraintRequest
):
    client = OrgPolicyClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "custom_constraint": {"name": "organizations/sample1/customConstraints/sample2"}
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.update_custom_constraint(request)


def test_update_custom_constraint_rest_flattened():
    client = OrgPolicyClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = constraint.CustomConstraint()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "custom_constraint": {
                "name": "organizations/sample1/customConstraints/sample2"
            }
        }

        # get truthy value for each flattened field
        mock_args = dict(
            custom_constraint=constraint.CustomConstraint(name="name_value"),
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = constraint.CustomConstraint.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.update_custom_constraint(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v2/{custom_constraint.name=organizations/*/customConstraints/*}"
            % client.transport._host,
            args[1],
        )


def test_update_custom_constraint_rest_flattened_error(transport: str = "rest"):
    client = OrgPolicyClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_custom_constraint(
            orgpolicy.UpdateCustomConstraintRequest(),
            custom_constraint=constraint.CustomConstraint(name="name_value"),
        )


def test_update_custom_constraint_rest_error():
    client = OrgPolicyClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        orgpolicy.GetCustomConstraintRequest,
        dict,
    ],
)
def test_get_custom_constraint_rest(request_type):
    client = OrgPolicyClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "organizations/sample1/customConstraints/sample2"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = constraint.CustomConstraint(
            name="name_value",
            resource_types=["resource_types_value"],
            method_types=[constraint.CustomConstraint.MethodType.CREATE],
            condition="condition_value",
            action_type=constraint.CustomConstraint.ActionType.ALLOW,
            display_name="display_name_value",
            description="description_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = constraint.CustomConstraint.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.get_custom_constraint(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, constraint.CustomConstraint)
    assert response.name == "name_value"
    assert response.resource_types == ["resource_types_value"]
    assert response.method_types == [constraint.CustomConstraint.MethodType.CREATE]
    assert response.condition == "condition_value"
    assert response.action_type == constraint.CustomConstraint.ActionType.ALLOW
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"


def test_get_custom_constraint_rest_required_fields(
    request_type=orgpolicy.GetCustomConstraintRequest,
):
    transport_class = transports.OrgPolicyRestTransport

    request_init = {}
    request_init["name"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(
            pb_request,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get_custom_constraint._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get_custom_constraint._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = OrgPolicyClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = constraint.CustomConstraint()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "get",
                "query_params": pb_request,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            # Convert return value to protobuf type
            return_value = constraint.CustomConstraint.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.get_custom_constraint(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_get_custom_constraint_rest_unset_required_fields():
    transport = transports.OrgPolicyRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.get_custom_constraint._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_get_custom_constraint_rest_interceptors(null_interceptor):
    transport = transports.OrgPolicyRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.OrgPolicyRestInterceptor(),
    )
    client = OrgPolicyClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.OrgPolicyRestInterceptor, "post_get_custom_constraint"
    ) as post, mock.patch.object(
        transports.OrgPolicyRestInterceptor, "pre_get_custom_constraint"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = orgpolicy.GetCustomConstraintRequest.pb(
            orgpolicy.GetCustomConstraintRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = constraint.CustomConstraint.to_json(
            constraint.CustomConstraint()
        )

        request = orgpolicy.GetCustomConstraintRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = constraint.CustomConstraint()

        client.get_custom_constraint(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_get_custom_constraint_rest_bad_request(
    transport: str = "rest", request_type=orgpolicy.GetCustomConstraintRequest
):
    client = OrgPolicyClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "organizations/sample1/customConstraints/sample2"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.get_custom_constraint(request)


def test_get_custom_constraint_rest_flattened():
    client = OrgPolicyClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = constraint.CustomConstraint()

        # get arguments that satisfy an http rule for this method
        sample_request = {"name": "organizations/sample1/customConstraints/sample2"}

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = constraint.CustomConstraint.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.get_custom_constraint(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v2/{name=organizations/*/customConstraints/*}" % client.transport._host,
            args[1],
        )


def test_get_custom_constraint_rest_flattened_error(transport: str = "rest"):
    client = OrgPolicyClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_custom_constraint(
            orgpolicy.GetCustomConstraintRequest(),
            name="name_value",
        )


def test_get_custom_constraint_rest_error():
    client = OrgPolicyClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        orgpolicy.ListCustomConstraintsRequest,
        dict,
    ],
)
def test_list_custom_constraints_rest(request_type):
    client = OrgPolicyClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "organizations/sample1"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = orgpolicy.ListCustomConstraintsResponse(
            next_page_token="next_page_token_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = orgpolicy.ListCustomConstraintsResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.list_custom_constraints(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListCustomConstraintsPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_custom_constraints_rest_required_fields(
    request_type=orgpolicy.ListCustomConstraintsRequest,
):
    transport_class = transports.OrgPolicyRestTransport

    request_init = {}
    request_init["parent"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(
            pb_request,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_custom_constraints._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = "parent_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_custom_constraints._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(
        (
            "page_size",
            "page_token",
        )
    )
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == "parent_value"

    client = OrgPolicyClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = orgpolicy.ListCustomConstraintsResponse()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "get",
                "query_params": pb_request,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            # Convert return value to protobuf type
            return_value = orgpolicy.ListCustomConstraintsResponse.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.list_custom_constraints(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_list_custom_constraints_rest_unset_required_fields():
    transport = transports.OrgPolicyRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.list_custom_constraints._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(
            (
                "pageSize",
                "pageToken",
            )
        )
        & set(("parent",))
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_list_custom_constraints_rest_interceptors(null_interceptor):
    transport = transports.OrgPolicyRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.OrgPolicyRestInterceptor(),
    )
    client = OrgPolicyClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.OrgPolicyRestInterceptor, "post_list_custom_constraints"
    ) as post, mock.patch.object(
        transports.OrgPolicyRestInterceptor, "pre_list_custom_constraints"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = orgpolicy.ListCustomConstraintsRequest.pb(
            orgpolicy.ListCustomConstraintsRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = orgpolicy.ListCustomConstraintsResponse.to_json(
            orgpolicy.ListCustomConstraintsResponse()
        )

        request = orgpolicy.ListCustomConstraintsRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = orgpolicy.ListCustomConstraintsResponse()

        client.list_custom_constraints(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_list_custom_constraints_rest_bad_request(
    transport: str = "rest", request_type=orgpolicy.ListCustomConstraintsRequest
):
    client = OrgPolicyClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "organizations/sample1"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.list_custom_constraints(request)


def test_list_custom_constraints_rest_flattened():
    client = OrgPolicyClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = orgpolicy.ListCustomConstraintsResponse()

        # get arguments that satisfy an http rule for this method
        sample_request = {"parent": "organizations/sample1"}

        # get truthy value for each flattened field
        mock_args = dict(
            parent="parent_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = orgpolicy.ListCustomConstraintsResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.list_custom_constraints(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v2/{parent=organizations/*}/customConstraints" % client.transport._host,
            args[1],
        )


def test_list_custom_constraints_rest_flattened_error(transport: str = "rest"):
    client = OrgPolicyClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_custom_constraints(
            orgpolicy.ListCustomConstraintsRequest(),
            parent="parent_value",
        )


def test_list_custom_constraints_rest_pager(transport: str = "rest"):
    client = OrgPolicyClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # TODO(kbandes): remove this mock unless there's a good reason for it.
        # with mock.patch.object(path_template, 'transcode') as transcode:
        # Set the response as a series of pages
        response = (
            orgpolicy.ListCustomConstraintsResponse(
                custom_constraints=[
                    constraint.CustomConstraint(),
                    constraint.CustomConstraint(),
                    constraint.CustomConstraint(),
                ],
                next_page_token="abc",
            ),
            orgpolicy.ListCustomConstraintsResponse(
                custom_constraints=[],
                next_page_token="def",
            ),
            orgpolicy.ListCustomConstraintsResponse(
                custom_constraints=[
                    constraint.CustomConstraint(),
                ],
                next_page_token="ghi",
            ),
            orgpolicy.ListCustomConstraintsResponse(
                custom_constraints=[
                    constraint.CustomConstraint(),
                    constraint.CustomConstraint(),
                ],
            ),
        )
        # Two responses for two calls
        response = response + response

        # Wrap the values into proper Response objs
        response = tuple(
            orgpolicy.ListCustomConstraintsResponse.to_json(x) for x in response
        )
        return_values = tuple(Response() for i in response)
        for return_val, response_val in zip(return_values, response):
            return_val._content = response_val.encode("UTF-8")
            return_val.status_code = 200
        req.side_effect = return_values

        sample_request = {"parent": "organizations/sample1"}

        pager = client.list_custom_constraints(request=sample_request)

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, constraint.CustomConstraint) for i in results)

        pages = list(client.list_custom_constraints(request=sample_request).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        orgpolicy.DeleteCustomConstraintRequest,
        dict,
    ],
)
def test_delete_custom_constraint_rest(request_type):
    client = OrgPolicyClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "organizations/sample1/customConstraints/sample2"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = None

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = ""

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.delete_custom_constraint(request)

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_custom_constraint_rest_required_fields(
    request_type=orgpolicy.DeleteCustomConstraintRequest,
):
    transport_class = transports.OrgPolicyRestTransport

    request_init = {}
    request_init["name"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(
            pb_request,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).delete_custom_constraint._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).delete_custom_constraint._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = OrgPolicyClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = None
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "delete",
                "query_params": pb_request,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200
            json_return_value = ""

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.delete_custom_constraint(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_delete_custom_constraint_rest_unset_required_fields():
    transport = transports.OrgPolicyRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.delete_custom_constraint._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_delete_custom_constraint_rest_interceptors(null_interceptor):
    transport = transports.OrgPolicyRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.OrgPolicyRestInterceptor(),
    )
    client = OrgPolicyClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.OrgPolicyRestInterceptor, "pre_delete_custom_constraint"
    ) as pre:
        pre.assert_not_called()
        pb_message = orgpolicy.DeleteCustomConstraintRequest.pb(
            orgpolicy.DeleteCustomConstraintRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()

        request = orgpolicy.DeleteCustomConstraintRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata

        client.delete_custom_constraint(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()


def test_delete_custom_constraint_rest_bad_request(
    transport: str = "rest", request_type=orgpolicy.DeleteCustomConstraintRequest
):
    client = OrgPolicyClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "organizations/sample1/customConstraints/sample2"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.delete_custom_constraint(request)


def test_delete_custom_constraint_rest_flattened():
    client = OrgPolicyClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = None

        # get arguments that satisfy an http rule for this method
        sample_request = {"name": "organizations/sample1/customConstraints/sample2"}

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = ""
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.delete_custom_constraint(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v2/{name=organizations/*/customConstraints/*}" % client.transport._host,
            args[1],
        )


def test_delete_custom_constraint_rest_flattened_error(transport: str = "rest"):
    client = OrgPolicyClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_custom_constraint(
            orgpolicy.DeleteCustomConstraintRequest(),
            name="name_value",
        )


def test_delete_custom_constraint_rest_error():
    client = OrgPolicyClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


def test_credentials_transport_error():
    # It is an error to provide credentials and a transport instance.
    transport = transports.OrgPolicyGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = OrgPolicyClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport,
        )

    # It is an error to provide a credentials file and a transport instance.
    transport = transports.OrgPolicyGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = OrgPolicyClient(
            client_options={"credentials_file": "credentials.json"},
            transport=transport,
        )

    # It is an error to provide an api_key and a transport instance.
    transport = transports.OrgPolicyGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    options = client_options.ClientOptions()
    options.api_key = "api_key"
    with pytest.raises(ValueError):
        client = OrgPolicyClient(
            client_options=options,
            transport=transport,
        )

    # It is an error to provide an api_key and a credential.
    options = mock.Mock()
    options.api_key = "api_key"
    with pytest.raises(ValueError):
        client = OrgPolicyClient(
            client_options=options, credentials=ga_credentials.AnonymousCredentials()
        )

    # It is an error to provide scopes and a transport instance.
    transport = transports.OrgPolicyGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = OrgPolicyClient(
            client_options={"scopes": ["1", "2"]},
            transport=transport,
        )


def test_transport_instance():
    # A client may be instantiated with a custom transport instance.
    transport = transports.OrgPolicyGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    client = OrgPolicyClient(transport=transport)
    assert client.transport is transport


def test_transport_get_channel():
    # A client may be instantiated with a custom transport instance.
    transport = transports.OrgPolicyGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel

    transport = transports.OrgPolicyGrpcAsyncIOTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.OrgPolicyGrpcTransport,
        transports.OrgPolicyGrpcAsyncIOTransport,
        transports.OrgPolicyRestTransport,
    ],
)
def test_transport_adc(transport_class):
    # Test default credentials are used if not provided.
    with mock.patch.object(google.auth, "default") as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport_class()
        adc.assert_called_once()


@pytest.mark.parametrize(
    "transport_name",
    [
        "grpc",
        "rest",
    ],
)
def test_transport_kind(transport_name):
    transport = OrgPolicyClient.get_transport_class(transport_name)(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    assert transport.kind == transport_name


def test_transport_grpc_default():
    # A client should use the gRPC transport by default.
    client = OrgPolicyClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    assert isinstance(
        client.transport,
        transports.OrgPolicyGrpcTransport,
    )


def test_org_policy_base_transport_error():
    # Passing both a credentials object and credentials_file should raise an error
    with pytest.raises(core_exceptions.DuplicateCredentialArgs):
        transport = transports.OrgPolicyTransport(
            credentials=ga_credentials.AnonymousCredentials(),
            credentials_file="credentials.json",
        )


def test_org_policy_base_transport():
    # Instantiate the base transport.
    with mock.patch(
        "google.cloud.orgpolicy_v2.services.org_policy.transports.OrgPolicyTransport.__init__"
    ) as Transport:
        Transport.return_value = None
        transport = transports.OrgPolicyTransport(
            credentials=ga_credentials.AnonymousCredentials(),
        )

    # Every method on the transport should just blindly
    # raise NotImplementedError.
    methods = (
        "list_constraints",
        "list_policies",
        "get_policy",
        "get_effective_policy",
        "create_policy",
        "update_policy",
        "delete_policy",
        "create_custom_constraint",
        "update_custom_constraint",
        "get_custom_constraint",
        "list_custom_constraints",
        "delete_custom_constraint",
    )
    for method in methods:
        with pytest.raises(NotImplementedError):
            getattr(transport, method)(request=object())

    with pytest.raises(NotImplementedError):
        transport.close()

    # Catch all for all remaining methods and properties
    remainder = [
        "kind",
    ]
    for r in remainder:
        with pytest.raises(NotImplementedError):
            getattr(transport, r)()


def test_org_policy_base_transport_with_credentials_file():
    # Instantiate the base transport with a credentials file
    with mock.patch.object(
        google.auth, "load_credentials_from_file", autospec=True
    ) as load_creds, mock.patch(
        "google.cloud.orgpolicy_v2.services.org_policy.transports.OrgPolicyTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        load_creds.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.OrgPolicyTransport(
            credentials_file="credentials.json",
            quota_project_id="octopus",
        )
        load_creds.assert_called_once_with(
            "credentials.json",
            scopes=None,
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            quota_project_id="octopus",
        )


def test_org_policy_base_transport_with_adc():
    # Test the default credentials are used if credentials and credentials_file are None.
    with mock.patch.object(google.auth, "default", autospec=True) as adc, mock.patch(
        "google.cloud.orgpolicy_v2.services.org_policy.transports.OrgPolicyTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.OrgPolicyTransport()
        adc.assert_called_once()


def test_org_policy_auth_adc():
    # If no credentials are provided, we should use ADC credentials.
    with mock.patch.object(google.auth, "default", autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        OrgPolicyClient()
        adc.assert_called_once_with(
            scopes=None,
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            quota_project_id=None,
        )


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.OrgPolicyGrpcTransport,
        transports.OrgPolicyGrpcAsyncIOTransport,
    ],
)
def test_org_policy_transport_auth_adc(transport_class):
    # If credentials and host are not provided, the transport class should use
    # ADC credentials.
    with mock.patch.object(google.auth, "default", autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport_class(quota_project_id="octopus", scopes=["1", "2"])
        adc.assert_called_once_with(
            scopes=["1", "2"],
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            quota_project_id="octopus",
        )


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.OrgPolicyGrpcTransport,
        transports.OrgPolicyGrpcAsyncIOTransport,
        transports.OrgPolicyRestTransport,
    ],
)
def test_org_policy_transport_auth_gdch_credentials(transport_class):
    host = "https://language.com"
    api_audience_tests = [None, "https://language2.com"]
    api_audience_expect = [host, "https://language2.com"]
    for t, e in zip(api_audience_tests, api_audience_expect):
        with mock.patch.object(google.auth, "default", autospec=True) as adc:
            gdch_mock = mock.MagicMock()
            type(gdch_mock).with_gdch_audience = mock.PropertyMock(
                return_value=gdch_mock
            )
            adc.return_value = (gdch_mock, None)
            transport_class(host=host, api_audience=t)
            gdch_mock.with_gdch_audience.assert_called_once_with(e)


@pytest.mark.parametrize(
    "transport_class,grpc_helpers",
    [
        (transports.OrgPolicyGrpcTransport, grpc_helpers),
        (transports.OrgPolicyGrpcAsyncIOTransport, grpc_helpers_async),
    ],
)
def test_org_policy_transport_create_channel(transport_class, grpc_helpers):
    # If credentials and host are not provided, the transport class should use
    # ADC credentials.
    with mock.patch.object(
        google.auth, "default", autospec=True
    ) as adc, mock.patch.object(
        grpc_helpers, "create_channel", autospec=True
    ) as create_channel:
        creds = ga_credentials.AnonymousCredentials()
        adc.return_value = (creds, None)
        transport_class(quota_project_id="octopus", scopes=["1", "2"])

        create_channel.assert_called_with(
            "orgpolicy.googleapis.com:443",
            credentials=creds,
            credentials_file=None,
            quota_project_id="octopus",
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            scopes=["1", "2"],
            default_host="orgpolicy.googleapis.com",
            ssl_credentials=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )


@pytest.mark.parametrize(
    "transport_class",
    [transports.OrgPolicyGrpcTransport, transports.OrgPolicyGrpcAsyncIOTransport],
)
def test_org_policy_grpc_transport_client_cert_source_for_mtls(transport_class):
    cred = ga_credentials.AnonymousCredentials()

    # Check ssl_channel_credentials is used if provided.
    with mock.patch.object(transport_class, "create_channel") as mock_create_channel:
        mock_ssl_channel_creds = mock.Mock()
        transport_class(
            host="squid.clam.whelk",
            credentials=cred,
            ssl_channel_credentials=mock_ssl_channel_creds,
        )
        mock_create_channel.assert_called_once_with(
            "squid.clam.whelk:443",
            credentials=cred,
            credentials_file=None,
            scopes=None,
            ssl_credentials=mock_ssl_channel_creds,
            quota_project_id=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )

    # Check if ssl_channel_credentials is not provided, then client_cert_source_for_mtls
    # is used.
    with mock.patch.object(transport_class, "create_channel", return_value=mock.Mock()):
        with mock.patch("grpc.ssl_channel_credentials") as mock_ssl_cred:
            transport_class(
                credentials=cred,
                client_cert_source_for_mtls=client_cert_source_callback,
            )
            expected_cert, expected_key = client_cert_source_callback()
            mock_ssl_cred.assert_called_once_with(
                certificate_chain=expected_cert, private_key=expected_key
            )


def test_org_policy_http_transport_client_cert_source_for_mtls():
    cred = ga_credentials.AnonymousCredentials()
    with mock.patch(
        "google.auth.transport.requests.AuthorizedSession.configure_mtls_channel"
    ) as mock_configure_mtls_channel:
        transports.OrgPolicyRestTransport(
            credentials=cred, client_cert_source_for_mtls=client_cert_source_callback
        )
        mock_configure_mtls_channel.assert_called_once_with(client_cert_source_callback)


@pytest.mark.parametrize(
    "transport_name",
    [
        "grpc",
        "grpc_asyncio",
        "rest",
    ],
)
def test_org_policy_host_no_port(transport_name):
    client = OrgPolicyClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="orgpolicy.googleapis.com"
        ),
        transport=transport_name,
    )
    assert client.transport._host == (
        "orgpolicy.googleapis.com:443"
        if transport_name in ["grpc", "grpc_asyncio"]
        else "https://orgpolicy.googleapis.com"
    )


@pytest.mark.parametrize(
    "transport_name",
    [
        "grpc",
        "grpc_asyncio",
        "rest",
    ],
)
def test_org_policy_host_with_port(transport_name):
    client = OrgPolicyClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="orgpolicy.googleapis.com:8000"
        ),
        transport=transport_name,
    )
    assert client.transport._host == (
        "orgpolicy.googleapis.com:8000"
        if transport_name in ["grpc", "grpc_asyncio"]
        else "https://orgpolicy.googleapis.com:8000"
    )


@pytest.mark.parametrize(
    "transport_name",
    [
        "rest",
    ],
)
def test_org_policy_client_transport_session_collision(transport_name):
    creds1 = ga_credentials.AnonymousCredentials()
    creds2 = ga_credentials.AnonymousCredentials()
    client1 = OrgPolicyClient(
        credentials=creds1,
        transport=transport_name,
    )
    client2 = OrgPolicyClient(
        credentials=creds2,
        transport=transport_name,
    )
    session1 = client1.transport.list_constraints._session
    session2 = client2.transport.list_constraints._session
    assert session1 != session2
    session1 = client1.transport.list_policies._session
    session2 = client2.transport.list_policies._session
    assert session1 != session2
    session1 = client1.transport.get_policy._session
    session2 = client2.transport.get_policy._session
    assert session1 != session2
    session1 = client1.transport.get_effective_policy._session
    session2 = client2.transport.get_effective_policy._session
    assert session1 != session2
    session1 = client1.transport.create_policy._session
    session2 = client2.transport.create_policy._session
    assert session1 != session2
    session1 = client1.transport.update_policy._session
    session2 = client2.transport.update_policy._session
    assert session1 != session2
    session1 = client1.transport.delete_policy._session
    session2 = client2.transport.delete_policy._session
    assert session1 != session2
    session1 = client1.transport.create_custom_constraint._session
    session2 = client2.transport.create_custom_constraint._session
    assert session1 != session2
    session1 = client1.transport.update_custom_constraint._session
    session2 = client2.transport.update_custom_constraint._session
    assert session1 != session2
    session1 = client1.transport.get_custom_constraint._session
    session2 = client2.transport.get_custom_constraint._session
    assert session1 != session2
    session1 = client1.transport.list_custom_constraints._session
    session2 = client2.transport.list_custom_constraints._session
    assert session1 != session2
    session1 = client1.transport.delete_custom_constraint._session
    session2 = client2.transport.delete_custom_constraint._session
    assert session1 != session2


def test_org_policy_grpc_transport_channel():
    channel = grpc.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.OrgPolicyGrpcTransport(
        host="squid.clam.whelk",
        channel=channel,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert transport._ssl_channel_credentials == None


def test_org_policy_grpc_asyncio_transport_channel():
    channel = aio.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.OrgPolicyGrpcAsyncIOTransport(
        host="squid.clam.whelk",
        channel=channel,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert transport._ssl_channel_credentials == None


# Remove this test when deprecated arguments (api_mtls_endpoint, client_cert_source) are
# removed from grpc/grpc_asyncio transport constructor.
@pytest.mark.parametrize(
    "transport_class",
    [transports.OrgPolicyGrpcTransport, transports.OrgPolicyGrpcAsyncIOTransport],
)
def test_org_policy_transport_channel_mtls_with_client_cert_source(transport_class):
    with mock.patch(
        "grpc.ssl_channel_credentials", autospec=True
    ) as grpc_ssl_channel_cred:
        with mock.patch.object(
            transport_class, "create_channel"
        ) as grpc_create_channel:
            mock_ssl_cred = mock.Mock()
            grpc_ssl_channel_cred.return_value = mock_ssl_cred

            mock_grpc_channel = mock.Mock()
            grpc_create_channel.return_value = mock_grpc_channel

            cred = ga_credentials.AnonymousCredentials()
            with pytest.warns(DeprecationWarning):
                with mock.patch.object(google.auth, "default") as adc:
                    adc.return_value = (cred, None)
                    transport = transport_class(
                        host="squid.clam.whelk",
                        api_mtls_endpoint="mtls.squid.clam.whelk",
                        client_cert_source=client_cert_source_callback,
                    )
                    adc.assert_called_once()

            grpc_ssl_channel_cred.assert_called_once_with(
                certificate_chain=b"cert bytes", private_key=b"key bytes"
            )
            grpc_create_channel.assert_called_once_with(
                "mtls.squid.clam.whelk:443",
                credentials=cred,
                credentials_file=None,
                scopes=None,
                ssl_credentials=mock_ssl_cred,
                quota_project_id=None,
                options=[
                    ("grpc.max_send_message_length", -1),
                    ("grpc.max_receive_message_length", -1),
                ],
            )
            assert transport.grpc_channel == mock_grpc_channel
            assert transport._ssl_channel_credentials == mock_ssl_cred


# Remove this test when deprecated arguments (api_mtls_endpoint, client_cert_source) are
# removed from grpc/grpc_asyncio transport constructor.
@pytest.mark.parametrize(
    "transport_class",
    [transports.OrgPolicyGrpcTransport, transports.OrgPolicyGrpcAsyncIOTransport],
)
def test_org_policy_transport_channel_mtls_with_adc(transport_class):
    mock_ssl_cred = mock.Mock()
    with mock.patch.multiple(
        "google.auth.transport.grpc.SslCredentials",
        __init__=mock.Mock(return_value=None),
        ssl_credentials=mock.PropertyMock(return_value=mock_ssl_cred),
    ):
        with mock.patch.object(
            transport_class, "create_channel"
        ) as grpc_create_channel:
            mock_grpc_channel = mock.Mock()
            grpc_create_channel.return_value = mock_grpc_channel
            mock_cred = mock.Mock()

            with pytest.warns(DeprecationWarning):
                transport = transport_class(
                    host="squid.clam.whelk",
                    credentials=mock_cred,
                    api_mtls_endpoint="mtls.squid.clam.whelk",
                    client_cert_source=None,
                )

            grpc_create_channel.assert_called_once_with(
                "mtls.squid.clam.whelk:443",
                credentials=mock_cred,
                credentials_file=None,
                scopes=None,
                ssl_credentials=mock_ssl_cred,
                quota_project_id=None,
                options=[
                    ("grpc.max_send_message_length", -1),
                    ("grpc.max_receive_message_length", -1),
                ],
            )
            assert transport.grpc_channel == mock_grpc_channel


def test_constraint_path():
    project = "squid"
    constraint = "clam"
    expected = "projects/{project}/constraints/{constraint}".format(
        project=project,
        constraint=constraint,
    )
    actual = OrgPolicyClient.constraint_path(project, constraint)
    assert expected == actual


def test_parse_constraint_path():
    expected = {
        "project": "whelk",
        "constraint": "octopus",
    }
    path = OrgPolicyClient.constraint_path(**expected)

    # Check that the path construction is reversible.
    actual = OrgPolicyClient.parse_constraint_path(path)
    assert expected == actual


def test_custom_constraint_path():
    organization = "oyster"
    custom_constraint = "nudibranch"
    expected = (
        "organizations/{organization}/customConstraints/{custom_constraint}".format(
            organization=organization,
            custom_constraint=custom_constraint,
        )
    )
    actual = OrgPolicyClient.custom_constraint_path(organization, custom_constraint)
    assert expected == actual


def test_parse_custom_constraint_path():
    expected = {
        "organization": "cuttlefish",
        "custom_constraint": "mussel",
    }
    path = OrgPolicyClient.custom_constraint_path(**expected)

    # Check that the path construction is reversible.
    actual = OrgPolicyClient.parse_custom_constraint_path(path)
    assert expected == actual


def test_policy_path():
    project = "winkle"
    policy = "nautilus"
    expected = "projects/{project}/policies/{policy}".format(
        project=project,
        policy=policy,
    )
    actual = OrgPolicyClient.policy_path(project, policy)
    assert expected == actual


def test_parse_policy_path():
    expected = {
        "project": "scallop",
        "policy": "abalone",
    }
    path = OrgPolicyClient.policy_path(**expected)

    # Check that the path construction is reversible.
    actual = OrgPolicyClient.parse_policy_path(path)
    assert expected == actual


def test_common_billing_account_path():
    billing_account = "squid"
    expected = "billingAccounts/{billing_account}".format(
        billing_account=billing_account,
    )
    actual = OrgPolicyClient.common_billing_account_path(billing_account)
    assert expected == actual


def test_parse_common_billing_account_path():
    expected = {
        "billing_account": "clam",
    }
    path = OrgPolicyClient.common_billing_account_path(**expected)

    # Check that the path construction is reversible.
    actual = OrgPolicyClient.parse_common_billing_account_path(path)
    assert expected == actual


def test_common_folder_path():
    folder = "whelk"
    expected = "folders/{folder}".format(
        folder=folder,
    )
    actual = OrgPolicyClient.common_folder_path(folder)
    assert expected == actual


def test_parse_common_folder_path():
    expected = {
        "folder": "octopus",
    }
    path = OrgPolicyClient.common_folder_path(**expected)

    # Check that the path construction is reversible.
    actual = OrgPolicyClient.parse_common_folder_path(path)
    assert expected == actual


def test_common_organization_path():
    organization = "oyster"
    expected = "organizations/{organization}".format(
        organization=organization,
    )
    actual = OrgPolicyClient.common_organization_path(organization)
    assert expected == actual


def test_parse_common_organization_path():
    expected = {
        "organization": "nudibranch",
    }
    path = OrgPolicyClient.common_organization_path(**expected)

    # Check that the path construction is reversible.
    actual = OrgPolicyClient.parse_common_organization_path(path)
    assert expected == actual


def test_common_project_path():
    project = "cuttlefish"
    expected = "projects/{project}".format(
        project=project,
    )
    actual = OrgPolicyClient.common_project_path(project)
    assert expected == actual


def test_parse_common_project_path():
    expected = {
        "project": "mussel",
    }
    path = OrgPolicyClient.common_project_path(**expected)

    # Check that the path construction is reversible.
    actual = OrgPolicyClient.parse_common_project_path(path)
    assert expected == actual


def test_common_location_path():
    project = "winkle"
    location = "nautilus"
    expected = "projects/{project}/locations/{location}".format(
        project=project,
        location=location,
    )
    actual = OrgPolicyClient.common_location_path(project, location)
    assert expected == actual


def test_parse_common_location_path():
    expected = {
        "project": "scallop",
        "location": "abalone",
    }
    path = OrgPolicyClient.common_location_path(**expected)

    # Check that the path construction is reversible.
    actual = OrgPolicyClient.parse_common_location_path(path)
    assert expected == actual


def test_client_with_default_client_info():
    client_info = gapic_v1.client_info.ClientInfo()

    with mock.patch.object(
        transports.OrgPolicyTransport, "_prep_wrapped_messages"
    ) as prep:
        client = OrgPolicyClient(
            credentials=ga_credentials.AnonymousCredentials(),
            client_info=client_info,
        )
        prep.assert_called_once_with(client_info)

    with mock.patch.object(
        transports.OrgPolicyTransport, "_prep_wrapped_messages"
    ) as prep:
        transport_class = OrgPolicyClient.get_transport_class()
        transport = transport_class(
            credentials=ga_credentials.AnonymousCredentials(),
            client_info=client_info,
        )
        prep.assert_called_once_with(client_info)


@pytest.mark.asyncio
async def test_transport_close_async():
    client = OrgPolicyAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc_asyncio",
    )
    with mock.patch.object(
        type(getattr(client.transport, "grpc_channel")), "close"
    ) as close:
        async with client:
            close.assert_not_called()
        close.assert_called_once()


def test_transport_close():
    transports = {
        "rest": "_session",
        "grpc": "_grpc_channel",
    }

    for transport, close_name in transports.items():
        client = OrgPolicyClient(
            credentials=ga_credentials.AnonymousCredentials(), transport=transport
        )
        with mock.patch.object(
            type(getattr(client.transport, close_name)), "close"
        ) as close:
            with client:
                close.assert_not_called()
            close.assert_called_once()


def test_client_ctx():
    transports = [
        "rest",
        "grpc",
    ]
    for transport in transports:
        client = OrgPolicyClient(
            credentials=ga_credentials.AnonymousCredentials(), transport=transport
        )
        # Test client calls underlying transport.
        with mock.patch.object(type(client.transport), "close") as close:
            close.assert_not_called()
            with client:
                pass
            close.assert_called()


@pytest.mark.parametrize(
    "client_class,transport_class",
    [
        (OrgPolicyClient, transports.OrgPolicyGrpcTransport),
        (OrgPolicyAsyncClient, transports.OrgPolicyGrpcAsyncIOTransport),
    ],
)
def test_api_key_credentials(client_class, transport_class):
    with mock.patch.object(
        google.auth._default, "get_api_key_credentials", create=True
    ) as get_api_key_credentials:
        mock_cred = mock.Mock()
        get_api_key_credentials.return_value = mock_cred
        options = client_options.ClientOptions()
        options.api_key = "api_key"
        with mock.patch.object(transport_class, "__init__") as patched:
            patched.return_value = None
            client = client_class(client_options=options)
            patched.assert_called_once_with(
                credentials=mock_cred,
                credentials_file=None,
                host=client.DEFAULT_ENDPOINT,
                scopes=None,
                client_cert_source_for_mtls=None,
                quota_project_id=None,
                client_info=transports.base.DEFAULT_CLIENT_INFO,
                always_use_jwt_access=True,
                api_audience=None,
            )
