import cognee
import asyncio


async def main():
    # Add sample content
    text = "Natural language processing (NLP) is a subfield of computer science."
    await cognee.add(text)

    # Process with LLMs to build the knowledge graph
    await cognee.cognify()

    # Search the knowledge graph
    results = await cognee.search(
        query_text="Tell me about NLP"
    )

    for result in results:
        print(result)


if __name__ == '__main__':
    asyncio.run(main())
