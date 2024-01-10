# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
#
#   Copyright 2023 Valory AG
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
# ------------------------------------------------------------------------------

"""Utility functions."""
from json import JSONDecodeError
from typing import Dict, List

from aea.configurations.base import PackageConfiguration
from aea.configurations.data_types import PackageId, PublicId
from aea.crypto.base import LedgerApi
from requests import get as r_get
from requests.exceptions import ConnectionError as RequestConnectionError

from autonomy.chain.base import registry_contracts
from autonomy.chain.constants import SERVICE_MANAGER_TOKEN_COMPATIBLE_CHAINS
from autonomy.chain.exceptions import DependencyError, FailedToRetrieveComponentMetadata
from autonomy.chain.metadata import IPFS_URI_PREFIX
from autonomy.configurations.base import Service


def get_ipfs_hash_from_uri(uri: str) -> str:
    """Split IPFS hash from the ipfs uri"""

    return uri.replace(IPFS_URI_PREFIX, "")


def resolve_component_id(
    ledger_api: LedgerApi,
    contract_address: str,
    token_id: int,
    is_agent: bool = False,
    is_service: bool = False,
) -> Dict:
    """Resolve component ID to metadata json"""

    try:
        if is_service:
            token_uri_callable = registry_contracts.service_registry.get_token_uri
        elif is_agent:
            token_uri_callable = registry_contracts.agent_registry.get_token_uri
        else:
            token_uri_callable = registry_contracts.component_registry.get_token_uri

        metadata_uri = token_uri_callable(
            ledger_api=ledger_api,
            contract_address=contract_address,
            token_id=token_id,
        )
    except RequestConnectionError as e:
        raise FailedToRetrieveComponentMetadata("Error connecting to the RPC") from e

    try:
        return r_get(url=metadata_uri).json()
    except RequestConnectionError as e:
        raise FailedToRetrieveComponentMetadata(
            "Error connecting to the IPFS gateway"
        ) from e
    except JSONDecodeError as e:
        raise FailedToRetrieveComponentMetadata(
            f"Error decoding json data; make sure metadata file for the component exist on the IPFS registry; Dependency ID: {token_id}"
        ) from e


def parse_public_id_from_metadata(id_string: str) -> PublicId:
    """Parse public ID from on-chain metadata."""

    if ":" in id_string:
        id_string, _ = id_string.split(":")

    try:
        # author/package_name
        return PublicId.from_str(id_string).to_any()
    except ValueError as e:
        id_parts = id_string.split("/")

        if len(id_parts) == 3:
            # component_type/author/name
            _, author, name = id_parts
            return PublicId(author=author, name=name).to_any()

        if len(id_parts) == 4:
            # component_type/author/name/version
            return PackageId.from_uri_path(id_string).public_id.to_any()

        raise DependencyError(f"Invalid package name found `{id_string}`") from e


def verify_component_dependencies(
    ledger_api: LedgerApi,
    contract_address: str,
    dependencies: List[int],
    package_configuration: PackageConfiguration,
    skip_hash_check: bool = False,
) -> None:
    """Verify package dependencies using on-chain metadata."""

    public_id_to_hash: Dict[PublicId, List[str]] = {}

    for dependency in package_configuration.package_dependencies:
        public_id = dependency.public_id.to_any()
        if public_id not in public_id_to_hash:
            public_id_to_hash[public_id] = []
        public_id_to_hash[dependency.public_id.to_any()].append(dependency.package_hash)

    for dependency_id in dependencies:
        component_metadata = resolve_component_id(
            contract_address=contract_address,
            ledger_api=ledger_api,
            token_id=dependency_id,
        )
        component_public_id = parse_public_id_from_metadata(component_metadata["name"])
        if component_public_id not in public_id_to_hash:
            raise DependencyError(
                f"On chain dependency with id {dependency_id} and public ID {component_public_id} not found in the local package configuration"
            )

        if skip_hash_check and len(public_id_to_hash[component_public_id]) > 0:
            public_id_to_hash[component_public_id].pop()
        else:
            on_chain_hash = get_ipfs_hash_from_uri(uri=component_metadata["code_uri"])
            if on_chain_hash not in public_id_to_hash[component_public_id]:
                raise DependencyError(
                    f"Package hash does not match for the on chain package and the local package; Dependency={dependency_id}"
                )
            public_id_to_hash[component_public_id] = [
                _hash
                for _hash in public_id_to_hash[component_public_id]
                if _hash != on_chain_hash
            ]

        if len(public_id_to_hash[component_public_id]) == 0:
            del public_id_to_hash[component_public_id]

    if len(public_id_to_hash):
        missing_deps = list(map(str, public_id_to_hash.keys()))
        raise DependencyError(
            f"Please provide on chain ID as dependency for following packages; {missing_deps}"
        )


def verify_service_dependencies(
    ledger_api: LedgerApi,
    contract_address: str,
    agent_id: int,
    service_configuration: Service,
    skip_hash_check: bool = False,
) -> None:
    """Verify package dependencies using on-chain metadata."""

    agent = service_configuration.agent
    component_metadata = resolve_component_id(
        contract_address=contract_address,
        ledger_api=ledger_api,
        token_id=agent_id,
        is_agent=True,
    )
    component_public_id = parse_public_id_from_metadata(component_metadata["name"])
    if component_public_id != agent.to_any():
        raise DependencyError(
            "On chain ID of the agent does not match with the one in the service configuration"
        )

    if skip_hash_check:
        return

    if agent.hash != get_ipfs_hash_from_uri(uri=component_metadata["code_uri"]):
        raise DependencyError(
            f"Package hash does not match for the on chain package and the local package; Dependency={agent}"
        )


def is_service_manager_token_compatible_chain(ledger_api: LedgerApi) -> bool:
    """Verify package dependencies using on-chain metadata."""
    return ledger_api.api.eth.chain_id in SERVICE_MANAGER_TOKEN_COMPATIBLE_CHAINS
