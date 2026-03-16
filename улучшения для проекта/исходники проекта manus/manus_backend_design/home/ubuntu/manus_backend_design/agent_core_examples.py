import json
import os
from typing import Dict, Any, List, Callable

# --- 1. Имитация LLM (Large Language Model) ---
# В реальной системе здесь будет вызов API к OpenAI, Gemini или другой LLM.
# Для примера, LLM будет "решать", какой инструмент вызвать или какой текст сгенерировать.

def mock_llm_call(prompt: str, available_tools: List[Dict]) -> Dict[str, Any]:
    """Имитирует вызов LLM и возвращает либо текстовый ответ, либо вызов инструмента.

    В реальной LLM, она бы анализировала `prompt` и `available_tools`
    и генерировала структурированный JSON для вызова инструмента или текстовый ответ.
    """
    print(f"\n--- LLM Input Prompt ---\n{prompt}\n")

    # Простая логика имитации: если в промпте есть ключевые слова, "вызываем" инструмент
    if "create file" in prompt.lower():
        return {
            "tool_call": {
                "name": "file",
                "args": {
                    "action": "write",
                    "path": "/home/ubuntu/test_file.txt",
                    "text": "Hello from Manus mock LLM!"
                }
            }
        }
    elif "list files" in prompt.lower():
        return {
            "tool_call": {
                "name": "shell",
                "args": {
                    "action": "exec",
                    "session": "mock_session",
                    "command": "ls -l /home/ubuntu"
                }
            }
        }
    elif "current date" in prompt.lower():
        return {
            "text_response": "Текущая дата: 16 марта 2026 года. (Имитация LLM)"
        }
    else:
        return {
            "text_response": f"Я получил ваш запрос: \"{prompt}\". (Имитация LLM)"
        }

# --- 2. Менеджер Инструментов (Tool Manager) ---
# Регистрирует инструменты и предоставляет механизм для их вызова.

class ToolManager:
    def __init__(self):
        self.tools: Dict[str, Callable] = {}
        self.tool_schemas: List[Dict] = [] # Для передачи LLM описаний инструментов

    def register_tool(self, name: str, func: Callable, schema: Dict):
        """Регистрирует инструмент и его схему."""
        self.tools[name] = func
        self.tool_schemas.append(schema)
        print(f"Инструмент '{name}' зарегистрирован.")

    def call_tool(self, tool_name: str, **kwargs) -> Any:
        """Вызывает зарегистрированный инструмент."""
        if tool_name not in self.tools:
            raise ValueError(f"Инструмент '{tool_name}' не зарегистрирован.")
        print(f"\nВызов инструмента: {tool_name} с аргументами: {kwargs}")
        try:
            # В реальной системе здесь будет более сложная обработка, возможно, через RPC/IPC
            # для взаимодействия с изолированной средой.
            result = self.tools[tool_name](**kwargs)
            print(f"Результат инструмента '{tool_name}': {result}")
            return result
        except Exception as e:
            print(f"Ошибка при вызове инструмента '{tool_name}': {e}")
            return {"error": str(e)}

# --- 3. Имитация Инструментов (Mock Tools) ---
# Эти функции имитируют реальные инструменты (shell, file и т.д.)

def mock_shell_exec(session: str, command: str) -> Dict[str, str]:
    """Имитирует выполнение команды в оболочке."""
    print(f"[MOCK SHELL] Сессия: {session}, Команда: {command}")
    if command == "ls -l /home/ubuntu":
        return {"output": "-rw-r--r-- 1 ubuntu ubuntu 1234 Mar 16 10:00 test_file.txt\n"}
    return {"output": f"Mock output for: {command}"}

def mock_file_write(path: str, text: str) -> Dict[str, str]:
    """Имитирует запись в файл."""
    print(f"[MOCK FILE] Запись в файл: {path}, Содержимое: '{text[:20]}...' ")
    # В реальной системе здесь будет запись в файл в песочнице
    return {"status": f"Файл {path} успешно записан."}

# --- 4. Модуль Памяти (Memory Module) ---
# Хранит контекст диалога и результаты действий.

class MemoryModule:
    def __init__(self):
        self.history: List[Dict[str, Any]] = []
        self.system_prompt_parts: List[str] = []

    def add_system_prompt_part(self, part: str):
        self.system_prompt_parts.append(part)

    def add_to_history(self, entry: Dict[str, Any]):
        self.history.append(entry)

    def get_full_context(self, tool_schemas: List[Dict]) -> str:
        """Формирует полный промпт для LLM, включая системные инструкции и историю."""
        context_parts = []

        # Системный промпт
        context_parts.append("\n".join(self.system_prompt_parts))

        # Описание доступных инструментов (для Tool Calling)
        context_parts.append("\nAvailable Tools:\n")
        for schema in tool_schemas:
            context_parts.append(json.dumps(schema, indent=2))

        # История диалога
        context_parts.append("\n--- Conversation History ---\n")
        for entry in self.history:
            if "user_message" in entry:
                context_parts.append(f"User: {entry['user_message']}")
            if "agent_response" in entry:
                context_parts.append(f"Agent: {entry['agent_response']}")
            if "tool_call" in entry:
                context_parts.append(f"Agent calls tool: {entry['tool_call']['name']} with {entry['tool_call']['args']}")
            if "tool_result" in entry:
                context_parts.append(f"Tool Result: {entry['tool_result']}")

        return "\n".join(context_parts)

# --- 5. Оркестратор Агента (Agent Orchestrator) ---
# Основной цикл управления агентом.

class AgentOrchestrator:
    def __init__(self, llm_caller: Callable, tool_manager: ToolManager, memory: MemoryModule):
        self.llm_caller = llm_caller
        self.tool_manager = tool_manager
        self.memory = memory
        self.current_phase_id = 1
        self.goal = ""
        self.phases: List[Dict] = []

    def update_plan(self, goal: str, phases: List[Dict], current_phase_id: int):
        self.goal = goal
        self.phases = phases
        self.current_phase_id = current_phase_id
        self.memory.add_to_history({"agent_response": f"План обновлен. Цель: {self.goal}. Текущая фаза: {self.phases[self.current_phase_id-1]['title']}"})
        print(f"[ORCHESTRATOR] План обновлен. Цель: {self.goal}. Текущая фаза: {self.phases[self.current_phase_id-1]['title']}")

    def advance_phase(self, next_phase_id: int):
        if next_phase_id != self.current_phase_id + 1:
            raise ValueError("Можно переходить только к следующей фазе.")
        self.current_phase_id = next_phase_id
        self.memory.add_to_history({"agent_response": f"Переход к фазе: {self.phases[self.current_phase_id-1]['title']}"})
        print(f"[ORCHESTRATOR] Переход к фазе: {self.phases[self.current_phase_id-1]['title']}")

    def run_agent_loop(self, user_input: str):
        self.memory.add_to_history({"user_message": user_input})
        print(f"\n[ORCHESTRATOR] Получен запрос пользователя: {user_input}")

        while True:
            full_prompt = self.memory.get_full_context(self.tool_manager.tool_schemas)
            llm_response = self.llm_caller(full_prompt, self.tool_manager.tool_schemas)

            if "tool_call" in llm_response:
                tool_call = llm_response["tool_call"]
                tool_name = tool_call["name"]
                tool_args = tool_call["args"]
                self.memory.add_to_history({"tool_call": tool_call})

                tool_result = self.tool_manager.call_tool(tool_name, **tool_args)
                self.memory.add_to_history({"tool_result": tool_result})

                # Если инструмент `plan` был вызван, обновить внутреннее состояние оркестратора
                if tool_name == "plan":
                    if tool_args["action"] == "update":
                        self.update_plan(tool_args["goal"], tool_args["phases"], tool_args["current_phase_id"])
                    elif tool_args["action"] == "advance":
                        self.advance_phase(tool_args["next_phase_id"])

                # Продолжаем цикл, чтобы LLM могла обработать результат инструмента
                continue
            elif "text_response" in llm_response:
                agent_response = llm_response["text_response"]
                self.memory.add_to_history({"agent_response": agent_response})
                print(f"\n[ORCHESTRATOR] Ответ агента: {agent_response}")
                break # Задача завершена или требуется новый ввод от пользователя
            else:
                print("[ORCHESTRATOR] Неожиданный ответ от LLM.")
                break

# --- Инициализация и запуск примера ---
if __name__ == "__main__":
    # Инициализация компонентов
    tool_manager = ToolManager()
    memory = MemoryModule()

    # Добавление системных инструкций в память
    memory.add_system_prompt_part("You are an autonomous AI agent. Your goal is to assist the user by using the available tools.")
    memory.add_system_prompt_part("Always use the `plan` tool to manage your task workflow.")

    # Регистрация имитированных инструментов
    tool_manager.register_tool(
        name="shell",
        func=mock_shell_exec,
        schema={
            "name": "shell",
            "description": "Execute shell commands in the sandbox.",
            "parameters": {
                "type": "object",
                "properties": {
                    "session": {"type": "string"},
                    "command": {"type": "string"}
                },
                "required": ["session", "command"]
            }
        }
    )
    tool_manager.register_tool(
        name="file",
        func=mock_file_write,
        schema={
            "name": "file",
            "description": "Write content to a file.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string"},
                    "text": {"type": "string"}
                },
                "required": ["path", "text"]
            }
        }
    )
    # Имитация инструмента `plan` для демонстрации обновления плана
    tool_manager.register_tool(
        name="plan",
        func=lambda action, current_phase_id, goal=None, next_phase_id=None, phases=None: {"status": "Plan updated/advanced"},
        schema={
            "name": "plan",
            "description": "Create, update, and advance the structured task plan.",
            "parameters": {
                "type": "object",
                "properties": {
                    "action": {"type": "string", "enum": ["update", "advance"]},
                    "current_phase_id": {"type": "integer"},
                    "goal": {"type": "string"},
                    "next_phase_id": {"type": "integer"},
                    "phases": {"type": "array", "items": {"type": "object", "properties": {"id": {"type": "integer"}, "title": {"type": "string"}, "capabilities": {"type": "object"}}}}
                },
                "required": ["action", "current_phase_id"]
            }
        }
    )

    orchestrator = AgentOrchestrator(mock_llm_call, tool_manager, memory)

    # --- Пример взаимодействия ---
    print("\n--- Запуск сценария 1: Создание файла ---")
    orchestrator.run_agent_loop("Please create a file named test_file.txt with 'Hello from Manus mock LLM!' content.")

    print("\n--- Запуск сценария 2: Просмотр файлов ---")
    orchestrator.run_agent_loop("Now, list all files in /home/ubuntu.")

    print("\n--- Запуск сценария 3: Простой вопрос ---")
    orchestrator.run_agent_loop("What is the current date?")

    print("\n--- Запуск сценария 4: Обновление плана (имитация) ---")
    orchestrator.run_agent_loop(
        "Update the plan: Goal is to 'Demonstrate agent capabilities', phases are 'Initialize', 'Execute', 'Report'. Current phase is 1."
    )

    print("\n--- Запуск сценария 5: Продвижение плана (имитация) ---")
    orchestrator.run_agent_loop("Advance the plan to the next phase.")

    print("\n--- Полная история взаимодействия ---")
    for entry in memory.history:
        print(entry)

