# template_agent_youtube

> A local agent template that automatically generates YouTube descriptions using GPT

---

## Overview

Write your video content in `input.txt`, and GPT will automatically generate a complete YouTube description saved to the `output/` folder.

This is a practical template for learning how to **embed GPT into a workflow** — not just chatting with it.

```
input.txt  →  [run.py + GPT API]  →  output/youtube_description.txt
```

---

## Project Structure

```
template_agent_youtube/
├── run.py               # Main agent script
├── input.txt            # Video summary/notes input file
├── output/              # Generated description output folder
├── requirements.txt     # Python dependencies
├── .env.example         # Environment variable template (copy to .env)
└── .gitignore
```

---

## Getting Started

### 1. Install Dependencies

```bash
python3 -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Set Up Environment Variables

```bash
cp .env.example .env
```

Open `.env` and enter your API key:

```
OPENAI_API_KEY=sk-proj-your_api_key_here
```

> Get your API key at [OpenAI Platform](https://platform.openai.com/api-keys).

### 3. Write Your Input

Add your video content to `input.txt` in any format — summary, notes, or script.

```
Today's video is about building a local agent from scratch.
Put a file in the input folder and GPT processes it automatically.
...
```

### 4. Run

```bash
python run.py
```

The result will be saved to `output/youtube_description.txt`.

---

## Output Example

```
Today's video covers how to build a local agent from scratch.
...

✅ Who this is for
• Anyone curious about API-based automation
...

#YouTubeAutomation #GPT #LocalAgent ...
```

---

## Security

- Never commit your `.env` file — it is excluded via `.gitignore`.
- If your API key is exposed, revoke and regenerate it immediately at [OpenAI Platform](https://platform.openai.com/api-keys).

---

## Channel

**Crab** — AI you can actually use at work, without the complexity.
Practical tips, concepts, and insights — one problem at a time, every week.

📩 info@creativeflow.co.kr
