"""
Basic library for interacting with OpenAI chat API
"""

import os
from openai import OpenAI
from rich.console import Console
from dataclasses import dataclass
from typing import Optional

__version__ = "0.0.1"


@dataclass
class ChatEntry:
    text: str

    def as_json(self):
        raise NotImplementedError()

    @property
    def role(self):
        raise NotImplementedError()

    def __str__(self):
        return f"[{self.role}]\n{self.text}"


@dataclass
class AssistantEntry(ChatEntry):
    def as_json(self):
        return {"role": "assistant", "content": self.text}

    @property
    def role(self):
        return "Assistant"


@dataclass
class UserEntry(ChatEntry):
    def as_json(self):
        return {"role": "user", "content": self.text}

    @property
    def role(self):
        return "User"

@dataclass
class SystemEntry(ChatEntry):
    def as_json(self):
        return {"role": "system", "content": self.text}

    @property
    def role(self):
        return "System"


if os.environ.get("OPENAI_API_KEY") is None:
    raise Exception("OPENAI_API_KEY is not set")

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)


def complete(
    prompt: str,
    conversation_history: list[ChatEntry],
    model: str = "gpt-4-1106-preview",
    system_prompt: Optional[str] = None,
    write_output: bool = True,
    console: Optional[Console] = None,
        output_style: str = "deep_sky_blue2",
):
    if console:
        print = console.print

    messages = []
    if system_prompt:
        messages.append(SystemEntry(system_prompt).as_json())

    for entry in conversation_history:
        messages.append(entry.as_json())

    messages.append(UserEntry(prompt).as_json())
    stream = client.chat.completions.create(
        model=model,
        messages=messages,
        stream=True,
    )
    if write_output:
        print()
    out = ""
    for chunk in stream:
        out_chunk = chunk.choices[0].delta.content or ""
        out += out_chunk
        if write_output:
            print(out_chunk, end="", style=output_style)

    if write_output:
        print()
        print()

    return out

