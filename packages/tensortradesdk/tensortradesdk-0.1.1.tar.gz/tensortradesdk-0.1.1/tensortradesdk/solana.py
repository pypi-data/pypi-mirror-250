from typing import Literal

from solana.rpc.api import Client
from solana.transaction import Transaction
from solders.keypair import Keypair
from solders.message import to_bytes_versioned, MessageV0
from solders.rpc.responses import SendTransactionResp
from solders.transaction import VersionedTransaction

from tensortradesdk.clients.base_model import BaseModel

Network = Literal["devnet", "mainnet"]


class SolanaClient:
    def __init__(self, network: Network, private_key: str):
        self.client = create_client(network)
        self.keypair = create_keypair(private_key)

    def submit_tensor_transaction(
        self, payload: BaseModel
    ) -> list[SendTransactionResp]:
        data = payload.model_dump()
        if len(data) != 1:
            raise RuntimeError("Invalid payload")
        root_key = next(iter(data.keys()))
        try:
            txs_buffer = data[root_key]["txs"]
            txs = []
            for tx_buffer in txs_buffer:
                if versioned_tx_buffer := tx_buffer.get("tx_v_0"):
                    tx = create_versioned_transaction(
                        self.client, self.keypair, versioned_tx_buffer.get("data")
                    )
                elif legacy_tx_buffer := tx_buffer.get("tx"):
                    tx = create_legacy_transaction(
                        self.keypair, legacy_tx_buffer.get("data")
                    )
                else:
                    raise KeyError("Missing tx and txV0 keys")
                txs.append(send_transaction(self.client, tx, self.keypair))
            return txs

        except KeyError:
            raise RuntimeError("Invalid payload")


def create_client(network: Network) -> Client:
    url = f"https://api.{network}.solana.com"
    if network.startswith("http"):
        url = network
    return Client(url)


def create_keypair(private_key: str) -> Keypair:
    return Keypair.from_base58_string(private_key)


def create_legacy_transaction(
    sender_key_pair: Keypair, transaction_buffer: list[int]
) -> Transaction:
    transaction = Transaction.deserialize(bytes(transaction_buffer))
    transaction.sign(sender_key_pair)
    return transaction


def create_versioned_transaction(
    client: Client, sender_key_pair: Keypair, transaction_buffer: list[int]
) -> VersionedTransaction:
    block = client.get_latest_blockhash().value
    transaction = VersionedTransaction.from_bytes(bytes(transaction_buffer))
    new_msg = MessageV0(
        transaction.message.header,
        transaction.message.account_keys,
        block.blockhash,
        transaction.message.instructions,
        [],
    )
    signature = sender_key_pair.sign_message(to_bytes_versioned(new_msg))
    return VersionedTransaction.populate(new_msg, [signature])


def send_transaction(
    client: Client,
    transaction: VersionedTransaction | Transaction,
    sender_key_pair: Keypair | None = None,
) -> SendTransactionResp:
    return client.send_transaction(transaction, sender_key_pair)
