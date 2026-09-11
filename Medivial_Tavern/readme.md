# 🏰 Medieval Tavern NPC Simulation

A multi-agent autonomous NPC simulation built using:

- LangChain
- LangGraph
- Groq
- ChromaDB
- SQLite

## Characters

### Eva
A kind and friendly waitress who enjoys talking and making people happy.

### Freddy
The frustrated owner and chef whose tavern is losing money.

### John
A regular customer who likes Eva and enjoys flirting with her.

---

## How It Works

Every NPC has:

- Entity Memory
- Episodic Memory
- Summary Memory
- Reflection Memory
- Character Memory
- Relationship Memory

Each NPC stores its memory separately.

Example:

data/eva/memory.db

data/freddy/memory.db

data/john/memory.db

---

## Daily Simulation

Each simulated day lasts 5 minutes.

The God Agent creates:

- Weather
- Tavern conditions
- Daily events
- Mood changes

NPCs then decide what they want to do.

They can:

- Talk
- Wait
- Interrupt
- Leave

Conversations are monitored by a Reviewer Agent to reduce repetition.

---

## Installation

Install dependencies:

uv add langchain langchain-core langchain-groq langgraph chromadb pydantic python-dotenv

Add your Groq API key to `.env`:

GROQ_API_KEY=your_key_here

Run:

uv run python main.py



# Medieval Tavern NPC Simulation

An autonomous medieval tavern simulation where NPCs make decisions, interact with each other, remember past events, react to the world, and speak using character-specific voices.

The system is designed so that NPC behaviour is not hard-coded. Each NPC uses an LLM to decide what to do based on its personality, mood, role, memories, world state, and current interactions.

---

## System Overview

```text
                    ┌─────────────────┐
                    │   Day Manager   │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │   World / God   │
                    │   Creates Day   │
                    └────────┬────────┘
                             │
                             ▼
              ┌────────────────────────────┐
              │       NPC Decision         │
              │ talk / work / wander /     │
              │ rest / join / interrupt    │
              └────────────┬───────────────┘
                           │
                           ▼
              ┌────────────────────────────┐
              │     Conversation Manager   │
              │                            │
              │  2-way / 3-way / group     │
              │  conversations             │
              │  interruptions             │
              └────────────┬───────────────┘
                           │
              ┌────────────┴─────────────┐
              ▼                          ▼
       ┌──────────────┐          ┌──────────────┐
       │ NPC Memory   │          │  Reviewer    │
       │ System       │          │    Agent     │
       └──────┬───────┘          └──────────────┘
              │
              ▼
       Persistent Memory
       for each NPC

                           │
                           ▼
                    ┌──────────────┐
                    │  TTS Manager │
                    └──────┬───────┘
                           ▼
                         Voice