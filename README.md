# ⚡ NODE ENGINE v2: Premium Agentic Chatbot Ecosystem

An extraordinary, high-end AI application powered by **LangGraph**, **Groq**, and **Tavily**. This platform delivers a state-of-the-art conversational experience with built-in specialized "Protocols" for web research and real-time AI news processing.

---

## ✨ Extraordinary SaaS Features
- **💎 Glassmorphic UI**: A luxury visual experience featuring glass-blur bubbles, depth-inducing shadows, and stone-sleek gradients.
- **◈ Avatar System**: Distinct "Diamond Badge" avatars for both User and AI agents, providing a professional and clear conversational flow.
- **📦 Multi-Protocol Agents**:
  - **Basic Chatbot**: High-speed, intuitive conversational intelligence.
  - **Chatbot With Web Search**: Live search-and-synthesize engine for real-time data retrieval.
  - **AI News Dispatch**: An automated data pipeline that fetches global tech headlines and provides summarized IST-based reports.
- **⚡ Token Streaming**: Real-time token-by-token "typing" effect with an animated cursor, delivering a true ChatGPT-like high-end feel.
- **🧠 Advanced Persistence**: Intelligent session management that preserves conversational memory and historical protocols across reruns.

---

## 🛠️ Technology Stack
- **Framework**: [LangGraph](https://github.com/langchain-ai/langgraph) (Agentic logic & state management)
- **Interface**: [Streamlit](https://streamlit.io/) (Custom SaaS-style UI)
- **Intelligence**: [LangChain Groq](https://github.com/langchain-ai/langchain-groq) (Llama-3-70b / MIxtral-8x7b)
- **Data Engine**: [Tavily AI](https://tavily.com/) (Search Optimized for LLMs)
- **Styling**: Vanilla CSS with **Inter** typography scale.

---

## ⚙️ Setup & Installation

### 1. Prerequisites
- Python 3.10 or higher
- Git

### 2. Clone the Repository
```powershell
git clone https://github.com/bhargavibattula/Agentic_ChatBot.git
cd Agentic_ChatBot
```

### 3. Install Dependencies
```powershell
pip install -r requirements.txt
```

### 4. Configure API Keys
You will need your own API keys to run the platform. These are entered securely within the sidebar once the app is running:
- **Groq API Key**: [Get it here](https://console.groq.com/keys)
- **Tavily API Key**: [Get it here](https://tavily.com/)

---

## 🚀 Launching the Engine

Run the following command in your terminal to start the Node Engine:

```powershell
streamlit run app.py
```

### Usage Steps:
1. **Choose Protocol**: Select from Basic Chatbot, Web Search, or AI News in the sidebar.
2. **Authorize**: Paste your Groq and/or Tavily keys into the secure input fields.
3. **Configure Model**: Select your preferred LLM model (e.g., Llama-3-70b).
4. **Deploy**: Start chatting or launch the news pipeline.

---

## 🏗️ Project Architecture
The codebase is modularized for maximum performance and future-proofing:
```text
src/
├── langgraphagenticai/
│   ├── graph/         # State graphs and routing logic
│   ├── nodes/         # Business logic for fetch, summarize, and tools
│   ├── state/         # Pydantic/TypedDict state definitions
│   ├── LLMS/          # Provider configurations (Groq)
│   └── ui/            # CSS, configuration, and Streamlit components
app.py                # Entry point
```

---

## 📜 Deployment Protocols
- **Daily/Weekly News**: Generates summarized markdown reports in `src/AINews/` and streams them live to the interface.
- **Web Search**: Automatically decides when to use the internet to augment its knowledge using Tavily.

---

