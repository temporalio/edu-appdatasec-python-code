import asyncio
import dataclasses

import temporalio.converter
from temporalio.client import Client

from codec import CompressionCodec
from worker import GreetingWorkflow


async def main():
    # Connect client
    client = await Client.connect(
        "localhost:7233",
        data_converter=dataclasses.replace(
            temporalio.converter.default(), payload_codec=CompressionCodec(),
            failure_converter_class=temporalio.converter.DefaultFailureConverterWithEncodedAttributes,
        ),
    )

    # Run workflow
    result = await client.execute_workflow(
        GreetingWorkflow.run,
        "Temporal",
        id=f"compression-workflow-id",
        task_queue="compression-task-queue",
    )

if __name__ == "__main__":
    asyncio.run(main())
