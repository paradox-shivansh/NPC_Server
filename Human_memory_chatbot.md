# 🧠 Human-Inspired Memory Chatbot

This project is a chatbot designed with multiple types of memory to simulate a more human-like conversational system.

The chatbot does not treat every message the same. Instead, it decides:

* What the user wants
* What information should be remembered
* Which memory should be retrieved
* What the chatbot can learn from the interaction
* Whether its behavior should gradually evolve

---

# 🏗️ Overall System Flow

```text
USER MESSAGE
      │
      ▼
┌───────────────────┐
│   MEMORY ROUTER   │
└─────────┬─────────┘
          │
          ▼
   INTENT DETECTION
          │
          ▼
┌──────────────────────────┐
│ Which memory is needed?  │
│ Which memory to write?   │
└────────────┬─────────────┘
             │
             ▼
      MEMORY RETRIEVAL
             │
     ┌───────┼────────┐
     ▼       ▼        ▼
 ENTITY   EPISODIC  SUMMARY
 MEMORY   MEMORY    MEMORY
     │       │        │
     └───────┼────────┘
             │
             ▼
      CONTEXT BUILDER
             │
             ▼
        🤖 CHATBOT LLM
             │
             ▼
       GENERATE RESPONSE
             │
             ▼
      SELF REFLECTION
             │
             ▼
       MEMORY UPDATE
             │
             ▼
            END
```

---

# 1️⃣ User Sends a Message

Example:

```text
"My name is Shivansh and I love building AI applications."
```

The message enters the chatbot system.

---

# 2️⃣ Memory Router

The **Memory Router** is the brain that decides what should happen with the message.

It analyzes:

* User intent
* Importance of the information
* Which memories should be retrieved
* Which memories should be updated

Example decision:

```json
{
    "intent": "personal_information",
    "retrieve_memories": [
        "entity",
        "summary"
    ],
    "write_memories": [
        "entity"
    ],
    "importance": 0.8
}
```

---

# 3️⃣ Memory Retrieval

Based on the router's decision, the system retrieves relevant memories.

There are several memory systems.

---

## 👤 Entity Memory

Stores information about people and entities.

Example:

```text
User:
- Name: Shivansh
- Interested in AI
- Interested in RAG
- Prefers beginner-friendly explanations
```

This helps the chatbot remember important long-term information.

---

## 📖 Episodic Memory

Stores important experiences and events.

Example:

```text
"Shivansh started building a human-inspired memory chatbot."
```

Episodic memory answers:

> What happened in the past?

---

## 📝 Summary Memory

Stores a compressed summary of the conversation.

Instead of sending the entire conversation to the LLM:

```text
1000 Messages ❌
```

The system uses:

```text
Conversation Summary
+
Recent Messages
```

This saves tokens and keeps important context.

---

## 🤔 Reflection Memory

Stores lessons learned by the chatbot.

Example:

```text
Lesson:
"Explain technical concepts step-by-step for this user."
```

Reflection memory helps improve future responses.

---

## 🤖 Character Memory

Stores the chatbot's personality traits.

Example:

```json
{
    "humor": 0.5,
    "empathy": 0.7,
    "curiosity": 0.8,
    "formality": 0.5
}
```

The character can slowly evolve based on repeated interactions.

---

# 4️⃣ Context Builder

All relevant memories are combined into a context.

```text
ENTITY MEMORY
        +
EPISODIC MEMORY
        +
SUMMARY MEMORY
        +
REFLECTION MEMORY
        +
CHARACTER MEMORY
        ↓
   CONTEXT BUILDER
```

The context is then sent to the LLM.

---

# 5️⃣ LLM Generates a Response

The LLM receives:

```text
System Instructions
+
Character Personality
+
Relevant Memories
+
Conversation Summary
+
Current User Message
```

Then it generates the final response.

---

# 6️⃣ Self Reflection

After generating a response, the chatbot analyzes the interaction.

It asks itself:

```text
Did I understand the user?

Did I answer correctly?

Did I learn something important?

Did the user reveal a preference?

Was there an important event?

Should my behavior change?
```

Example reflection:

```text
User prefers simple explanations.

Lesson:
Use beginner-friendly language for technical topics.
```

---

# 7️⃣ Memory Update

The system updates the appropriate memory.

Example:

```text
USER:
"I prefer simple explanations."

        ↓

MEMORY ROUTER

        ↓

ENTITY MEMORY

        ↓

STORE:

"User prefers simple explanations."
```

---

# 🔄 Complete Example

## User Message

```text
"I started learning LangGraph today."
```

### Step 1: Memory Router

Detects:

```text
Intent: Personal Information / Event
Importance: High
```

### Step 2: Retrieve Memory

Retrieves:

```text
Entity Memory
Summary Memory
```

### Step 3: LLM Responds

```text
"That's great! LangGraph is especially useful for building
stateful AI agents and memory systems."
```

### Step 4: Self Reflection

The system identifies:

```text
New information about the user:
User is learning LangGraph.
```

### Step 5: Memory Update

Stores:

```text
ENTITY MEMORY:
"User is learning LangGraph."

EPISODIC MEMORY:
"User started learning LangGraph."
```

---

# 🧠 Memory Router Logic

The Memory Router follows this general logic:

```text
                USER MESSAGE
                     │
                     ▼
              INTENT ANALYSIS
                     │
         ┌───────────┼───────────┐
         ▼           ▼           ▼
    Personal       Event       Question
         │           │           │
         ▼           ▼           ▼
      Entity      Episodic    Retrieve Only
      Memory       Memory
```

Not every message should be stored.

Example:

```text
"What is Python?"
```

Usually:

```text
Retrieve Memory: Yes
Write Memory: No
```

But:

```text
"My favorite language is Python."
```

Becomes:

```text
Retrieve Memory: Optional
Write Memory: Entity Memory
```

---

# 🔄 LangGraph Flow

The chatbot workflow is managed by LangGraph.

```text
START
  │
  ▼
ROUTER
  │
  ▼
RETRIEVE MEMORY
  │
  ▼
GENERATE RESPONSE
  │
  ▼
SELF REFLECTION
  │
  ▼
UPDATE MEMORY
  │
  ▼
END
```

Each step is a **LangGraph Node**.

---

# 🎯 Main Goal

The goal is to create a chatbot that behaves more intelligently over time.

```text
INTERACTION
      ↓
MEMORY
      ↓
REFLECTION
      ↓
LEARNING
      ↓
BETTER FUTURE RESPONSE
```

The system should not simply remember everything.

Instead, it should:

* Remember important information
* Forget irrelevant information
* Retrieve relevant experiences
* Learn from interactions
* Maintain a consistent personality
* Slowly evolve based on repeated experiences

---

# 🚀 Future Improvements

Future versions can add:

```text
PostgreSQL
      +
pgvector
      +
Semantic Search
      +
Memory Importance Scoring
      +
Memory Decay
      +
Pattern Detection
      +
Long-term Character Development
```

---

# 🧠 Final Mental Model

Think of the system like this:

```text
MEMORY ROUTER = Brain's decision system

ENTITY MEMORY = Who people are

EPISODIC MEMORY = What happened

SUMMARY MEMORY = What is currently happening

REFLECTION MEMORY = What I learned

CHARACTER MEMORY = Who the chatbot is
```

Together, these components create a **Human-Inspired Cognitive Memory Architecture for Conversational AI**.
