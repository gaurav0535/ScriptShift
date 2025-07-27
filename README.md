# ScriptShift

> 🤖 An intelligent content repurposing system that uses LangGraph to transform your content across platforms with AI-driven conversation flow.

ScriptShift is an AI-powered content repurposing tool built with LangGraph and FastAPI. It helps users transform their existing content into different formats while maintaining the core message and adapting it for different platforms and audiences.

## 🚀 Features

- Content input via URL or raw text
- Interactive conversation flow using LangGraph
- Content analysis and summarization
- Customizable target audience and tone settings
- Multi-platform content adaptation
- OpenAI GPT integration for high-quality content generation

## 🏗️ Architecture

The project uses LangGraph for managing the conversation flow through different nodes:

1. `ask_for_content` - Initial node that prompts for user content
2. `parse_user_content` - Processes the input (URL/raw text)
3. `analyze` - Analyzes and understands the content
4. `clarify` - Gets additional context from the user
5. `polish` - Refines the content
6. `repurpose` - Adapts content for different platforms
7. `finalize` - Generates the final output

## 🔧 Setup

1. Clone the repository
2. Create a virtual environment:
```bash
python -m venv script
source script/bin/activate  # On Windows: script\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file with your OpenAI API key:
```
OPENAI_API_KEY=your_api_key_here
OPENAI_MODEL=gpt-4
```

## 🏃‍♂️ Running the Project

1. Start the application:
```bash
python test_graph.py
```

2. Follow the interactive prompts to:
   - Input your content (URL or raw text)
   - Specify target audience and tone
   - Choose target platforms
   - Review and receive the repurposed content

## 📁 Project Structure

```
ScriptShift/
├── app/
│   ├── api/
│   │   └── routes.py
│   ├── graph/
│   │   ├── nodes/
│   │   │   ├── ask_for_content.py
│   │   │   ├── parse_user_content.py
│   │   │   ├── analyze.py
│   │   │   ├── clarify.py
│   │   │   ├── polish.py
│   │   │   ├── repurpose.py
│   │   │   └── finalize.py
│   │   ├── graph.py
│   │   └── state.py
│   ├── services/
│   │   └── content_scrapper.py
│   └── utils/
│       └── logger.py
└── test_graph.py
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## ⚠️ Note

Make sure to handle your API keys securely and never commit them to version control.
