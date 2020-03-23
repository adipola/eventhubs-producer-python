import asyncio,os
from azure.eventhub.aio import EventHubProducerClient
from azure.eventhub import EventData
import yfinance as yf

from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential


async def run():
    # Create a producer client to send messages to the event hub.
    # Specify a connection string to your event hubs namespace and
 	# the event hub name.
    # get connection key from vault

    # credential = DefaultAzureCredential()

    keyVaultName = "eventhub-connection-str"
    seceretName = "sendToEventHubTopic"
    KVUri = "https://" + keyVaultName + ".vault.azure.net"

    client = SecretClient(vault_url=KVUri, credential=credential)
    conn_str = client.get_secret(seceretName)

    msft = yf.Ticker("MSFT")
    vxus = yf.Ticker("VXUS")

    # sendToEventHubTopic
    producer = EventHubProducerClient.from_connection_string(conn_str)
    
    async with producer:
        # Create a batch.
        event_data_batch = await producer.create_batch()

        # Add events to the batch.
        event_data_batch.add(EventData(msft.info))
        event_data_batch.add(EventData(vxus.info))

        # Send the batch of events to the event hub.
        await producer.send_batch(event_data_batch)
        print("batch sent")

loop = asyncio.get_event_loop()
loop.run_until_complete(run())


