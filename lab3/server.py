from pathlib import Path
from mcp.server.mcpserver import MCPServer

DOCS = Path(__file__).parent / "docs"  # папка с документами
mcp = MCPServer("file-search")  # создаём MCP-сервер


@mcp.tool()  # эта функция станет инструментом для модели
def search_files(query: str) -> list[dict]:
    """Ищет слово или фразу во всех документах компании (папка docs).
    Используй, когда вопрос касается правил, сроков или контактов компании."""
    hits = []
    q_lower = query.lower().strip()
    words = [w for w in q_lower.split() if len(w) > 2]
    for f in DOCS.glob("*.txt"):
        for line in f.read_text(encoding="utf-8").splitlines():
            l_lower = line.lower()
            if q_lower in l_lower or (words and any(w in l_lower for w in words)):
                hits.append({"file": f.name, "text": line})
    return hits


@mcp.tool()
def read_document(name: str) -> str:
    """Читает документ компании целиком из папки docs.
    Не разрешает выходить за пределы папки docs.
    Параметр name: имя файла, например 'hr_vacation.txt'."""
    file_path = (DOCS / name).resolve()
    docs_dir = DOCS.resolve()
    if not file_path.is_relative_to(docs_dir):
        return f"Ошибка: доступ запрещён. Нельзя читать файлы вне папки docs ('{name}')."
    if not file_path.is_file():
        return f"Ошибка: файл '{name}' не найден в docs."
    return file_path.read_text(encoding="utf-8")


if __name__ == "__main__":
    mcp.run()
