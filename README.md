# Topic Digest Agent 🔬

An autonomous research assistant built with the ReAct framework using `smolagents` and Streamlit. It uses AI to search the web, read pages, extract facts, check credibility, and synthesize findings into a comprehensive digest.

## Architecture & ReAct Framework

The agent follows the **ReAct** (Reason + Act) loop. Given a topic, it thinks about what to do, takes an action (uses a tool), observes the result, and repeats until the final digest is complete.

```
[User Input] --> [Agent]
                   |
           (Thought Process)
             /           \
         [Act] <------ [Observe]
           |               |
    (Tool Invocation) (Tool Output)
           |               |
    [ Web Search, Extraction, Credibility, etc. ]
```

## Tools
- `search_tool`: Searches DuckDuckGo
- `webpage_tool`: Reads raw page content
- `extract_key_facts`: LLM-based fact extraction
- `check_source_credibility`: URL domain rating
- `save_note`: Appends findings to session log
- `generate_citations`: Formats references

## Setup

1. **Clone the repository** (or download the files)
2. **Create a virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
4. **Set up environment variables**:
   Rename `.env.example` to `.env` and add your Groq API key:
   ```
   GROQ_API_KEY=your_key_here
   ```
5. **Run the app**:
   ```bash
   streamlit run app.py
   ```

## Usage
- Open the Streamlit UI (typically `http://localhost:8501`).
- Enter a topic like "Quantum Computing in Healthcare".
- The agent will autonomously stream its thoughts and actions.
- Review the generated **Research Digest**, **Reasoning Trace**, and **Research Log**.

## Project Structure
```
.
├── .env.example
├── .gitignore
├── README.md
├── agent.py
├── app.py
├── docs/
│   └── Topic_Digest_Agent_Documentation.md
├── requirements.txt
└── tools/
    ├── __init__.py
    ├── citations.py
    ├── credibility.py
    ├── extract_facts.py
    ├── notes.py
    └── search_tools.py
```

## Credits / License
Built using HuggingFace's [smolagents](https://github.com/huggingface/smolagents). Free to use under MIT License.
