# Tensor.trade Python SDK

The Tensor.trade Python SDK is a Python-based toolkit designed for developers who need to interface with the
Tensor.trade API. This SDK simplifies the process of accessing trading and financial data through GraphQL queries. It is
tailored for those who require reliable and straightforward tools to retrieve market data, manage trading operations, or
interact with the rich datasets provided by Tensor.trade.

The SDK leverages [ariadne-codegen](https://github.com/mirumee/ariadne-codegen) to generate the clients used within the
SDK. This approach ensures that the SDK
remains up-to-date with the latest GraphQL schema changes and provides a robust foundation for interacting with the
Tensor.trade API.

## Installation
```bash
pip install tensortradesdk
```

## Examples

### Collection Data

Get data based on GraphQL queries that can be found
in [Tensor.trade API docs](https://tensor-hq.notion.site/PUBLIC-Tensor-Trade-API-Docs-alpha-b18e1a196187473bac9b5d6de5b47032#23a79268ff6e46bcb2d7d176eb2066da)
and are also available
in [Tensor.trade Apollo Studio Explorer](https://studio.apollographql.com/public/Tensor-Trade-API/variant/current/explorer?collectionId=39d0b9d4-91d5-4e2e-a153-62adcde8db45&focusCollectionId=39d0b9d4-91d5-4e2e-a153-62adcde8db45).

#### Mint

```python
import os

from tensortradesdk.clients.collection_data_client import CollectionDataClient

collection_data_client = CollectionDataClient(api_key=os.environ["TENSOR_API_KEY"])
mint = collection_data_client.mint(mint="5gzsZDwaVERyKEpujPYfHkpvc7jMGvixZC5aJqAnEGEP")
print(mint)
# will print out (formatted for better legibility)
# mint=MintMint(
#   slug='05c52d84-2e49-4ed9-a473-b43cab41e777', 
#   tswap_orders=[], 
#   tensor_bids=[
#     MintMintTensorBids(
#       bidder='yfUkk7NmNmimdSdLA4gjnnKd2bYuSbDRYQFLww9bPeq', 
#       expiry=1733821085000, 
#       price='51240000000'
#     )
#   ], 
#   hswap_orders=[], 
#   active_listings=[
#     MintMintActiveListings(
#       mint=MintMintActiveListingsMint(onchain_id='5gzsZDwaVERyKEpujPYfHkpvc7jMGvixZC5aJqAnEGEP'), 
#       tx=MintMintActiveListingsTx(
#         seller_id='9bnVcN1ASN7Y4RLaE6XFmf4kiCYBA5vGMn37fEpVsCmV', 
#         gross_amount='111990000000', 
#         gross_amount_unit='SOL_LAMPORT'
#       )
#     )
#   ]
# )
```

### Transactions

#### TComp listing

```python
import os

from tensortradesdk.clients.transactions_client import TransactionsClient
from tensortradesdk.solana import SolanaClient

transactions_client = TransactionsClient(api_key=os.environ["TENSOR_API_KEY"])
tx_buffer = transactions_client.tcomp_list_tx(
    mint="5gzsZDwaVERyKEpujPYfHkpvc7jMGvixZC5aJqAnEGEP",
    owner="GkDpghsgrsJPcajN7pP9jAtDyfEoK2jxw9CLhZro6i59",
    price="420000000000",
)
print(tx_buffer)
# will print out (formatted for better legibility)
# tcomp_list_tx=TcompListTxTcompListTx(
#   txs=[
#     TcompListTxTcompListTxTxs(
#       last_valid_block_height=218440754, 
#       tx={
#         'type': 'Buffer', 
#         'data': [1, 0, 0, 0, 0, ...]
#       }
#     )
#   ]
# )

solana_client = SolanaClient(
    network="mainnet",
    private_key="<private_key>",
)
solana_client.submit_tensor_transaction(tx_buffer)
```

### GraphQL subscriptions

```python
import os

import asyncio

from tensortradesdk.clients.subscriptions_client_async import SubscriptionsClientAsync

subscriptions_client = SubscriptionsClientAsync(api_key=os.environ["TENSOR_API_KEY"])


async def print_orders():
    async for update in subscriptions_client.tswap_order_update_all():
        print(update)


asyncio.run(print_orders())
# this will stream order updates to console until the process is interrupted (e.g. Ctrl+C)
# tswap_order_update_all=TswapOrderUpdateAllTswapOrderUpdateAll(address='2aGMBEtKpyJeWTiCCSuE5Ktpbx9Q93932eUiaBXbY8H3', pool=TswapOrderUpdateAllTswapOrderUpdateAllPool(address='2aGMBEtKpyJeWTiCCSuE5Ktpbx9Q93932eUiaBXbY8H3', created_unix=1703151492000, curve_type=<CurveType.LINEAR: 'LINEAR'>, delta='10', mm_compound_fees=False, mm_fee_bps=None, nfts_for_sale=[], nfts_held=0, owner_address='K5iuD4h1zv46bsw5KNBMDkYKnnZCGoLq151wdJ7uv9d', pool_type=<PoolType.TOKEN: 'TOKEN'>, sol_balance='238981700', starting_price='9508900000', buy_now_price=None, sell_now_price=None, stats_accumulated_mm_profit='0', stats_taker_buy_count=0, stats_taker_sell_count=0, taker_buy_count=0, taker_sell_count=0, updated_at=1703151495750), slug='f2916c33-8835-49dd-b4b0-e70d7ac7f6cd')
# tswap_order_update_all=TswapOrderUpdateAllTswapOrderUpdateAll(address='5sFGxHB4FPNesDLAFY4qLAYRbPdkwULyrgQLHmzBAbS3', pool=TswapOrderUpdateAllTswapOrderUpdateAllPool(address='5sFGxHB4FPNesDLAFY4qLAYRbPdkwULyrgQLHmzBAbS3', created_unix=1703151498000, curve_type=<CurveType.LINEAR: 'LINEAR'>, delta='10', mm_compound_fees=False, mm_fee_bps=None, nfts_for_sale=[], nfts_held=0, owner_address='K5iuD4h1zv46bsw5KNBMDkYKnnZCGoLq151wdJ7uv9d', pool_type=<PoolType.TOKEN: 'TOKEN'>, sol_balance='238981700', starting_price='43106500000', buy_now_price=None, sell_now_price=None, stats_accumulated_mm_profit='0', stats_taker_buy_count=0, stats_taker_sell_count=0, taker_buy_count=0, taker_sell_count=0, updated_at=1703151501294), slug='claynosaurz')
# tswap_order_update_all=TswapOrderUpdateAllTswapOrderUpdateAll(address='DjP4K4cyt1UHWWc6rMPj59XndrabaGjXmfz1yq4KyofD', pool=TswapOrderUpdateAllTswapOrderUpdateAllPool(address='DjP4K4cyt1UHWWc6rMPj59XndrabaGjXmfz1yq4KyofD', created_unix=1703151488000, curve_type=<CurveType.LINEAR: 'LINEAR'>, delta='10', mm_compound_fees=False, mm_fee_bps=None, nfts_for_sale=[], nfts_held=0, owner_address='K5iuD4h1zv46bsw5KNBMDkYKnnZCGoLq151wdJ7uv9d', pool_type=<PoolType.TOKEN: 'TOKEN'>, sol_balance='238981700', starting_price='924100000', buy_now_price=None, sell_now_price=None, stats_accumulated_mm_profit='0', stats_taker_buy_count=0, stats_taker_sell_count=0, taker_buy_count=0, taker_sell_count=0, updated_at=1703151492272), slug='88f69a79-98ca-4320-a999-04170880f996')
```

## Development

### Update GraphQL schema

Download the schema from:
https://studio.apollographql.com/public/Tensor-Trade-API/variant/current/schema/sdl

> Currently not allowed to introspect schema so unable to automate the following.

To update the schema from Tensor.trade GraphQL API run the following command:

```bash
poetry run update_gql_schema
```

This currenlty errors with:

```json
{
  "errors": [
    {
      "message": "GraphQL introspection is not allowed by Apollo Server, but the query contained __schema or __type. To enable introspection, pass introspection: true to ApolloServer in production",
      "extensions": {
        "code": "GRAPHQL_VALIDATION_FAILED"
      }
    }
  ]
}
```

### Autogenerate clients

To autogenerate clients from GrapgQL queries run the following command:

```bash
poetry run generate_gql_clients
```

