import asyncio
from azure.eventhub.aio import EventHubProducerClient
from azure.eventhub import EventData
import yfinance as yf

from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential
from datetime import datetime


async def run(stocksCodesList):
    print('Start Batch for stocks: \n',stocksCodesList)
    # Create a producer client to send messages to the event hub.
    # Get connection string from vault

    credential = DefaultAzureCredential()
    keyVaultName = "eventhub-connection-str"
    secretName = "sendToEventHubTopic"
    KVUri = "https://" + keyVaultName + ".vault.azure.net"

    client = SecretClient(vault_url=KVUri, credential=credential)
    conn_str_value = client.get_secret(secretName).value

    # sendToEventHubTopic
    producer = EventHubProducerClient.from_connection_string(conn_str_value)
    
    async with producer:
        # Create a batch.
        event_data_batch =  await producer.create_batch()
        for stockCode in stocksCodesList:
            #Get stock info
            stockInfo = yf.Ticker(stockCode).info
            print(stockInfo)
            # Add events to the batch.
            event_data_batch.add(EventData(stockInfo))

        # Send the batch of events to the event hub.
        await producer.send_batch(event_data_batch)
        printSentMessage()


def printSentMessage():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print('Batch sent - Current Time =', current_time)

loop = asyncio.get_event_loop()
loop.run_until_complete(run(["MSFT"]))
loop.close()



# sched = BackgroundScheduler()
# # seconds can be replaced with minutes, hours, or days
# sched.add_job(run, 'interval', seconds=10)
# print("going to start scheduled task")
# sched.start()

# toShutDown = os.getenv("SHUT_DOWN_PRODUCER")

# if toShutDown == 'true':
#     sched.shutdown()

# run(["msft"])