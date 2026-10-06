import asyncio
import sys
from mcp import Client, StdioServerParameters

server = StdioServerParameters(command=sys.executable, args=["server.py"])


async def main():
    async with Client(server) as client:
        tools = await client.list_tools()
        print("Инструменты:", [t.name for t in tools.tools])
        
        query = sys.argv[1] if len(sys.argv) > 1 else "отпуск"
        print(f"\n--- Поиск по запросу: '{query}' ---")
        result = await client.call_tool("search_files", {"query": query})
        for block in result.content:
            print(block.text)

        # Тестирование бонусного инструмента read_document
        print("\n--- Проверка бонусного инструмента read_document ---")
        doc_result = await client.call_tool("read_document", {"name": "it_faq.txt"})
        for block in doc_result.content:
            print(f"[Чтение it_faq.txt]:\n{block.text}")

        # Проверка безопасности (защита от path traversal)
        security_test = await client.call_tool("read_document", {"name": "../server.py"})
        for block in security_test.content:
            print(f"[Попытка несанкционированного доступа '../server.py']:\n{block.text}")


if __name__ == "__main__":
    asyncio.run(main())
