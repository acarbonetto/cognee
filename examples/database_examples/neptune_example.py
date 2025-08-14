import base64
import json
import os
import pathlib
import asyncio
import cognee
from cognee.modules.search.types import SearchType
from dotenv import load_dotenv

load_dotenv()

async def main():
    """
    Example script demonstrating how to use Cognee with Amazon Neptune Analytics

    This example:
    1. Configures Cognee to use Neptune Analytics as graph database
    2. Sets up data directories
    3. Adds sample data to Cognee
    4. Processes/cognifies the data
    5. Performs different types of searches
    """

    # Set up Amazon credentials in .env file and get the values from environment variables
    graph_host = os.getenv("GRAPH_HOST", "")
    graph_endpoint_url = f"neptune-db://{graph_host}"

    # Configure Neptune Analytics as the graph & vector database provider
    cognee.config.set_graph_db_config(
        {
            "graph_database_provider": "neptune",  # Specify Neptune Analytics as provider
            "graph_database_url": graph_endpoint_url,  # Neptune Analytics endpoint with the format neptune-graph://<GRAPH_ID>
        }
    )

    # Set up data directories for storing documents and system files
    # You should adjust these paths to your needs
    current_dir = pathlib.Path(__file__).parent
    data_directory_path = str(current_dir / "data_storage")
    cognee.config.data_root_directory(data_directory_path)

    cognee_directory_path = str(current_dir / "cognee_system")
    cognee.config.system_root_directory(cognee_directory_path)

    # Clean any existing data (optional)
    await cognee.prune.prune_data()
    await cognee.prune.prune_system(metadata=True)

    # Create a dataset
    dataset_name = "neptune_example"

    # Add sample text to the dataset
    sample_text_1 ="""
    Amazon Neptune is a fast, reliable, fully managed graph database service that makes it easy to 
    build and run applications that work with highly connected datasets. The core of Neptune is a purpose-built, 
    high-performance graph database engine. This engine is optimized for storing billions of relationships and querying 
    the graph with milliseconds latency. Neptune supports the popular property-graph query languages Apache TinkerPop 
    Gremlin and Neo4j's openCypher, and the W3C's RDF query language, SPARQL. This enables you to build queries that 
    efficiently navigate highly connected datasets. Neptune powers graph use cases such as recommendation engines, 
    fraud detection, knowledge graphs, drug discovery, and network security.
    """

    sample_text_2 = """
    The Neptune database is highly available, with read replicas, point-in-time recovery, continuous
    backup to Amazon S3, and replication across Availability Zones. Neptune provides data security features, with 
    support for encryption at rest and in transit. Neptune is fully managed, so you no longer need to worry about 
    database management tasks like hardware provisioning, software patching, setup, configuration, or backups.
    """

    sample_text_3 = """
    Neptune Analytics is an analytics database engine that complements Neptune database and that can quickly analyze 
    large amounts of graph data in memory to get insights and find trends. Neptune Analytics is a solution for quickly 
    analyzing existing graph databases or graph datasets stored in a data lake. It uses popular graph analytic a
    lgorithms and low-latency analytic queries.
    """

    # Add the sample text to the dataset
    await cognee.add([sample_text_1, sample_text_2, sample_text_3], dataset_name)

    # Process the added document to extract knowledge
    await cognee.cognify([dataset_name])

    # Now let's perform some searches
    # 1. Search for insights related to "Neptune Analytics"
    insights_results = await cognee.search(
        query_type=SearchType.INSIGHTS, query_text="Neptune Analytics"
    )
    print("\n========Insights about Neptune Analytics========:")
    for result in insights_results:
        print(f"- {result}")

    # 2. Search for text chunks related to "graph database"
    chunks_results = await cognee.search(
        query_type=SearchType.CHUNKS, query_text="graph database", datasets=[dataset_name]
    )
    print("\n========Chunks about graph database========:")
    for result in chunks_results:
        print(f"- {result}")

    # 3. Get graph completion related to databases
    graph_completion_results = await cognee.search(
        query_type=SearchType.GRAPH_COMPLETION, query_text="database"
    )
    print("\n========Graph completion for databases========:")
    for result in graph_completion_results:
        print(f"- {result}")

    # Clean up (optional)
    await cognee.prune.prune_data()
    await cognee.prune.prune_system(metadata=True)


if __name__ == "__main__":
    asyncio.run(main())
