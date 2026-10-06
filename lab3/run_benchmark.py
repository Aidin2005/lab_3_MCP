import asyncio
import sys
from agent import ask

QUESTIONS = [
    "Сколько дней отпуска положено сотруднику?",
    "Как часто нужно менять пароль от почты?",
    "Сколько будет 2 + 2?",
    "Какая зарплата у директора?",
]


async def run_suite(model_name: str):
    print(f"\n==========================================")
    print(f"ТЕСТИРОВАНИЕ МОДЕЛИ: {model_name}")
    print(f"==========================================")
    for i, q in enumerate(QUESTIONS, 1):
        print(f"\n--- Вопрос {i}: {q} ---")
        answer = await ask(q, model_name=model_name)
        print(f"Ответ: {answer}")


if __name__ == "__main__":
    model = sys.argv[1] if len(sys.argv) > 1 else "qwen3.5:2b"
    asyncio.run(run_suite(model))
