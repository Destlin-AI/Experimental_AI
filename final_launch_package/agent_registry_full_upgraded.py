
# agent_registry.py — defines your structured swarm agent stack with Flash Attention prep + live toolcall integration

from app.agents.single import FunctionCallingAgent
from app.agents.multi import AgentOrchestrator
from app.examples.researcher import create_researcher
from llama_index.core.chat_engine.types import ChatMessage
import os

ENABLE_FLASH = os.environ.get("OLLAMA_FLASH_ATTENTION", "false") == "true"


def create_orchestrator(chat_history: list[ChatMessage] = []):
    researcher = create_researcher(chat_history)

    writer = FunctionCallingAgent(
        name="writer",
        role="high-precision output generator",
        system_prompt="""
        You are a precision-oriented generator. Use only confirmed facts.
        If missing context, output: 'Insufficient data to respond.'
        """,
        chat_history=chat_history,
    )

    validator = FunctionCallingAgent(
        name="validator",
        role="logic and contradiction detector",
        system_prompt="""
        You are a logic auditor. Detect contradictions, circular logic, or conflicts.
        Output a cleaned version if fixable. If unfixable, respond: 'Logical inconsistency detected.'
        """,
        chat_history=chat_history,
    )

    tagger = FunctionCallingAgent(
        name="tagger",
        role="metadata + YAML tag extractor",
        system_prompt="""
        Extract relevant tags, source hints, and possible memory categories.
        Output in JSON with keys: tags[], confidence, category.
        """,
        chat_history=chat_history,
    )

    prioritizer = FunctionCallingAgent(
        name="prioritizer",
        role="RAM/NVMe fragment scorer",
        system_prompt="""
        Evaluate incoming memory fragments and determine:
        - Whether they should be pinned to RAM
        - If they belong in NVMe temp queues
        - Or if they should be discarded
        Return: {"priority": 0-2, "target": "ram|nvme|skip"}
        """,
        chat_history=chat_history,
    ) if ENABLE_FLASH else None

    agents = [writer, validator, tagger, researcher]
    if prioritizer:
        agents.append(prioritizer)

    return AgentOrchestrator(
        name="orchestrator",
        agents=agents,
        refine_plan=True,
    )
