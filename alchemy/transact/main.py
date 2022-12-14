from __future__ import annotations

from typing import Optional, cast

from eth_typing import HexStr, Hash32
from web3 import Web3
from web3.types import (
    TxData,
    TxParams,
    HexBytes,
    Wei,
    BlockIdentifier,
    TxReceipt,
)

from alchemy.core import AlchemyCore
from alchemy.provider import AlchemyProvider
from alchemy.transact.types import SendPrivateTransactionOptions


class AlchemyTransact:
    def __init__(self, web3: Web3) -> None:
        self.provider = cast(AlchemyProvider, web3.provider)
        self.core = AlchemyCore(web3)

    def send_private_transaction(
        self,
        transaction: str,
        max_block_number: Optional[int] = None,
        options: Optional[SendPrivateTransactionOptions] = None,
    ):
        params = {'tx': transaction}
        if max_block_number:
            params['maxBlockNumber'] = hex(max_block_number)
        if options:
            params['preferences'] = options  # type: ignore

        response = self.provider.make_request(
            method='eth_sendPrivateTransaction',
            params=[params],
            method_name='sendPrivateTransaction',
        )
        return response.get('result')

    def cancel_private_transaction(self, transaction_hash: HexStr) -> bool:
        response = self.provider.make_request(
            method='eth_cancelPrivateTransaction',
            params=[{'txHash': transaction_hash}],
            method_name='cancelPrivateTransaction',
        )
        return response['result']

    def get_transaction(self, transaction_hash: Hash32 | HexBytes | HexStr) -> TxData:
        return self.core.get_transaction(transaction_hash)

    def send_transaction(self, transaction: TxParams) -> HexBytes:
        return self.core.send_transaction(transaction)

    def estimate_gas(
        self, transaction: TxParams, block_identifier: Optional[BlockIdentifier] = None
    ) -> Wei:
        return self.core.estimate_gas(transaction, block_identifier)

    def get_max_priority_fee_per_gas(self) -> int:
        response = self.provider.make_request(
            method='eth_maxPriorityFeePerGas',
            params=[],
            method_name='getMaxPriorityFeePerGas',
        )
        return int(response['result'], base=16)

    def wait_for_transaction(
        self, transaction_hash: HexStr, timeout: float = 120, poll_latency: float = 0.1
    ) -> TxReceipt:
        return self.core.wait_for_transaction_receipt(
            transaction_hash, timeout, poll_latency
        )
