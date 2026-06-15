#!/usr/bin/env python3
"""
LLM Council — MetaGPT-inspired multi-role orchestration.

Roles execute sequentially; each sees the full message history from prior roles,
enabling genuine context accumulation across the council.

Architecture (MetaGPT patterns, no MetaGPT dependency):
  Message  — typed data container (role, content, action, timestamp)
  Action   — unit of work with a system prompt; transforms context → response
  Role     — agent that owns an Action and an LLM backend
  Council  — orchestrator: runs roles in order, maintains shared message memory

Role assignments:
  ProductManager → ChatGPT  → AnalyzeRequirements
  Architect      → Gemini   → DesignSolution (sees PM analysis as context)

Output JSON:
{
  "prompt": "...",
  "council": {
    "product_manager": { "role", "action", "llm", "model", "source", "response" },
    "architect":        { "role", "action", "llm", "model", "source", "response" }
  },
  "messages": [
    { "role": "User",           "content": "...", "action": "UserInput",           "timestamp": "..." },
    { "role": "ProductManager", "content": "...", "action": "AnalyzeRequirements", "timestamp": "..." },
    { "role": "Architect",      "content": "...", "action": "DesignSolution",      "timestamp": "..." }
  ]
}
"""

import os
import sys
import json
import shutil
import subprocess
from datetime import datetime, timezone
from typing import Optional, Tuple

import requests


# ─── MetaGPT-inspired abstractions ────────────────────────────────────────────


class Message:
    """Typed data container passed between roles (analogous to MetaGPT's Message)."""

    def __init__(self, role: str, content: str, action: str):
        self.role = role
        self.content = content
        self.action = action
        self.timestamp = datetime.now(timezone.utc).isoformat()

    def to_dict(self) -> dict:
        return {
            "role": self.role,
            "content": self.content,
            "action": self.action,
            "timestamp": self.timestamp,
        }


class Action:
    """Base class for role work units (analogous to MetaGPT's Action)."""
    name: str = ""
    system_prompt: str = ""

    def build_context(self, memory: list) -> str:
        """Build the input context string from accumulated message history."""
        raise NotImplementedError


class AnalyzeRequirements(Action):
    """ProductManager action: parse the request and produce a structured requirements analysis."""
    name = "AnalyzeRequirements"
    system_prompt = (
        "You are a Product Manager in a multi-AI council. "
        "Your role is to analyze the user's question and produce a structured requirements analysis.\n\n"
        "Identify: the core problem or goal, key requirements and constraints, "
        "success criteria, and any ambiguities that need addressing.\n\n"
        "Be concise and structured. Your analysis will be passed to the Technical Architect as context."
    )

    def build_context(self, memory: list) -> str:
        for msg in memory:
            if msg.action == "UserInput":
                return msg.content
        return ""


class DesignSolution(Action):
    """Architect action: design a solution with full visibility into the PM's requirements analysis."""
    name = "DesignSolution"
    system_prompt = (
        "You are a Technical Architect in a multi-AI council. "
        "You receive the user's original question together with the Product Manager's requirements analysis.\n\n"
        "Design a concrete solution: propose a specific technical approach, "
        "evaluate key trade-offs (complexity, performance, maintainability, cost), "
        "identify risks and dependencies, and recommend concrete tools, patterns, or frameworks.\n\n"
        "Build on the Product Manager's analysis — address the requirements they identified "
        "and fill any gaps they noted. Be specific and actionable."
    )

    def build_context(self, memory: list) -> str:
        user_content = ""
        pm_content = ""
        for msg in memory:
            if msg.action == "UserInput":
                user_content = msg.content
            elif msg.action == "AnalyzeRequirements":
                pm_content = msg.content

        if pm_content:
            return (
                f"=== User Question ===\n{user_content}\n\n"
                f"=== Product Manager's Requirements Analysis ===\n{pm_content}"
            )
        return user_content


# ─── Helpers ──────────────────────────────────────────────────────────────────


def load_env_file(env_path: str = ".env") -> dict:
    """Load environment variables from a .env file."""
    env_vars = {}
    if not os.path.exists(env_path):
        return env_vars
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, value = line.split("=", 1)
                env_vars[key.strip()] = value.strip().strip('"').strip("'")
    return env_vars


def is_cli_available(name: str) -> bool:
    return shutil.which(name) is not None


def call_codex_cli(context: str, system_prompt: str, timeout: int = 60) -> Tuple[bool, str]:
    """Query via codex CLI, injecting system prompt into the message."""
    full_prompt = f"{system_prompt}\n\n{context}"
    try:
        result = subprocess.run(
            ["codex", "-p", full_prompt],
            capture_output=True, text=True, timeout=timeout,
        )
        if result.returncode == 0:
            return True, result.stdout.strip()
        return False, f"codex error: {result.stderr.strip()}"
    except subprocess.TimeoutExpired:
        return False, "codex timed out"
    except Exception as e:
        return False, f"codex exception: {e}"


def call_gemini_cli(context: str, system_prompt: str, timeout: int = 60) -> Tuple[bool, str]:
    """Query via gemini CLI, injecting system prompt into the message."""
    full_prompt = f"{system_prompt}\n\n{context}"
    try:
        result = subprocess.run(
            ["gemini", "-p", full_prompt],
            capture_output=True, text=True, timeout=timeout,
        )
        if result.returncode == 0:
            return True, result.stdout.strip()
        return False, f"gemini-cli error: {result.stderr.strip()}"
    except subprocess.TimeoutExpired:
        return False, "gemini-cli timed out"
    except Exception as e:
        return False, f"gemini-cli exception: {e}"


def call_openai_api(context: str, system_prompt: str, api_key: str, model: str) -> str:
    """Query OpenAI API with role-specific system prompt."""
    try:
        resp = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": model,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": context},
                ],
                "max_tokens": 2000,
                "temperature": 0.7,
            },
            timeout=30,
        )
        resp.raise_for_status()
        return resp.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Error querying OpenAI ({model}): {e}"


def call_gemini_api(context: str, system_prompt: str, api_key: str, model: str) -> str:
    """Query Gemini API with role-specific system instruction."""
    try:
        url = (
            f"https://generativelanguage.googleapis.com/v1beta/models/"
            f"{model}:generateContent?key={api_key}"
        )
        resp = requests.post(
            url,
            headers={"Content-Type": "application/json"},
            json={
                "systemInstruction": {"parts": [{"text": system_prompt}]},
                "contents": [{"parts": [{"text": context}]}],
                "generationConfig": {"temperature": 0.7, "maxOutputTokens": 2000},
            },
            timeout=30,
        )
        resp.raise_for_status()
        data = resp.json()
        return data["candidates"][0]["content"]["parts"][0]["text"]
    except Exception as e:
        return f"Error querying Gemini ({model}): {e}"


# ─── Role classes ──────────────────────────────────────────────────────────────


class Role:
    """Base class for council members (analogous to MetaGPT's Role)."""
    name: str = ""

    def run(self, memory: list) -> Tuple[Message, dict]:
        """Execute this role against accumulated message history. Returns (Message, metadata)."""
        raise NotImplementedError


class ProductManager(Role):
    """Analyzes requirements. Backed by ChatGPT."""
    name = "ProductManager"

    def __init__(self, api_key: Optional[str], model: str):
        self.api_key = api_key
        self.model = model
        self.action = AnalyzeRequirements()

    def run(self, memory: list) -> Tuple[Message, dict]:
        context = self.action.build_context(memory)

        response: Optional[str] = None
        source: Optional[str] = None

        if is_cli_available("codex"):
            ok, resp = call_codex_cli(context, self.action.system_prompt)
            if ok:
                response, source = resp, "codex-cli"

        if response is None:
            if self.api_key:
                response = call_openai_api(context, self.action.system_prompt, self.api_key, self.model)
                source = f"api ({self.model})"
            else:
                response = "Error: codex CLI not available and OPENAI_API_KEY not set"
                source = "none"

        msg = Message(role=self.name, content=response, action=self.action.name)
        meta = {
            "role": self.name,
            "action": self.action.name,
            "llm": "chatgpt",
            "model": self.model,
            "source": source,
            "response": response,
        }
        return msg, meta


class Architect(Role):
    """Designs solutions with full message context. Backed by Gemini."""
    name = "Architect"

    def __init__(self, api_key: Optional[str], model: str):
        self.api_key = api_key
        self.model = model
        self.action = DesignSolution()

    def run(self, memory: list) -> Tuple[Message, dict]:
        context = self.action.build_context(memory)

        response: Optional[str] = None
        source: Optional[str] = None

        if is_cli_available("gemini"):
            ok, resp = call_gemini_cli(context, self.action.system_prompt)
            if ok:
                response, source = resp, "gemini-cli"

        if response is None:
            if self.api_key:
                response = call_gemini_api(context, self.action.system_prompt, self.api_key, self.model)
                source = f"api ({self.model})"
            else:
                response = "Error: gemini CLI not available and GEMINI_API_KEY not set"
                source = "none"

        msg = Message(role=self.name, content=response, action=self.action.name)
        meta = {
            "role": self.name,
            "action": self.action.name,
            "llm": "gemini",
            "model": self.model,
            "source": source,
            "response": response,
        }
        return msg, meta


# ─── Council (Team orchestrator) ──────────────────────────────────────────────


class Council:
    """
    Orchestrates role execution and message passing (analogous to MetaGPT's Team).

    Roles execute sequentially. Each role receives the full accumulated message
    history so downstream roles can build on upstream outputs.
    """

    def __init__(self):
        self.memory: list = []
        self.roles: list = []

    def hire(self, roles: list):
        self.roles = roles

    def run(self, prompt: str) -> dict:
        """Seed memory with user input, then run each role in order."""
        self.memory = [Message(role="User", content=prompt, action="UserInput")]

        council_outputs = {}
        for role in self.roles:
            msg, meta = role.run(self.memory)
            self.memory.append(msg)
            role_key = role.name.lower()
            council_outputs[role_key] = meta

        return {
            "prompt": prompt,
            "council": council_outputs,
            "messages": [m.to_dict() for m in self.memory],
        }


# ─── Entry point ──────────────────────────────────────────────────────────────


def main():
    if len(sys.argv) < 2:
        print(json.dumps({
            "error": "Usage: query_llms.py <prompt>",
            "council": None,
            "messages": [],
        }))
        sys.exit(1)

    prompt = " ".join(sys.argv[1:])

    env = load_env_file()
    openai_key = env.get("OPENAI_API_KEY") or os.environ.get("OPENAI_API_KEY")
    gemini_key = env.get("GEMINI_API_KEY") or os.environ.get("GEMINI_API_KEY")
    openai_model = env.get("OPENAI_MODEL") or os.environ.get("OPENAI_MODEL") or "gpt-5-nano"
    gemini_model = env.get("GEMINI_MODEL") or os.environ.get("GEMINI_MODEL") or "gemini-3-flash-preview"

    council = Council()
    council.hire([
        ProductManager(api_key=openai_key, model=openai_model),
        Architect(api_key=gemini_key, model=gemini_model),
    ])

    result = council.run(prompt)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
