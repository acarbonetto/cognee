
import pytest

import cognee
from cognee.infrastructure.databases.vector import get_vector_engine
from cognee.infrastructure.databases.vector.neptune_analytics.NeptuneAnalyticsAdapter import NeptuneAnalyticsAdapter, \
    IndexSchema
from cognee.shared.logging_utils import get_logger
import os

logger = get_logger()

async def main():
    cognee.config.set_vector_db_provider("neptune")

    # When URL is absent
    cognee.config.set_vector_db_url(None)
    with pytest.raises(OSError):
        get_vector_engine()

    # Assert invalid graph ID.
    cognee.config.set_vector_db_url("invalid_url")
    with pytest.raises(ValueError):
        get_vector_engine()

    # Return a valid engine object with valid URL.
    graph_id = os.getenv('GRAPH_ID', "")
    cognee.config.set_vector_db_url(f"neptune-graph://{graph_id}")
    engine = get_vector_engine()
    assert isinstance(engine, NeptuneAnalyticsAdapter)

    TEST_COLLECTION_NAME = "test"
    # Data point - 1
    TEST_UUID = "78a28770-2cd5-41f8-9b65-065a34f16aff"
    TEST_TEXT = "Hello world"
    datapoint = IndexSchema(id=TEST_UUID, text=TEST_TEXT)
    # Data point - 2
    TEST_UUID_2 = "aaaa8770-1234-41f8-9b65-065a34f16aff"
    TEST_TEXT_2 = "Cognee"
    datapoint_2 = IndexSchema(id=TEST_UUID_2, text=TEST_TEXT_2)

    # Prun all vector_db entries
    await engine.prune()

    # Always return true
    has_collection = await engine.has_collection(TEST_COLLECTION_NAME)
    assert has_collection
    # No-op
    await engine.create_collection(TEST_COLLECTION_NAME, IndexSchema)

    # Save data-points
    await engine.create_data_points(TEST_COLLECTION_NAME, [datapoint, datapoint_2])

    # # Retrieve data-points
    result = await engine.retrieve(TEST_COLLECTION_NAME, [TEST_UUID, TEST_UUID_2])
    assert str(result[0].id) == TEST_UUID
    assert result[0].payload['text'] == TEST_TEXT

    assert str(result[1].id) == TEST_UUID_2
    assert result[1].payload['text'] == TEST_TEXT_2

    # Delete datapoint from vector store
    await engine.delete_data_points(TEST_COLLECTION_NAME, [TEST_UUID, TEST_UUID_2])

    # Retrieve should return an empty list.
    result_deleted = await engine.retrieve(TEST_COLLECTION_NAME, [TEST_UUID])
    assert result_deleted == []

if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
