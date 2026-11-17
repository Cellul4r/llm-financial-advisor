# Financial Advisor With LLM
*204203 COMPUTER SCIENCE TECHNOLOGY*

A Streamlit chat app that answers personal-finance questions. A large language model (through [LiteLLM](https://github.com/BerriAI/litellm), Groq `llama-3.3-70b-versatile` by default) calls specialised financial tools such as a tax calculator, loan calculator, and financial health checker.

## Table Of Contents
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Installation and Setup](#installation-and-setup)
- [How to run](#how-to-run)
- [Project Structure](#project-structure)
- [Running Tests](#running-tests)
- [Adding a New Tool](#adding-a-new-tool)
- [Contributing](#contributing)
- [Contributors](#contributors)
- [Slide Presentation](#slide-presentation)
- [Disclaimer](#disclaimer)
- [License](#license)

## Features
- Chat completion and tool calling

### Tool Calling
- Financial Health Checker Tool
- Financial Institution Tool
- Financial Loan Tool
- Investment Saving Tool and Investment Risk Tool
- Tax Calculator Tool
- Currency Converter Tool

## Tech Stack
- Python 3.11
- [Streamlit](https://streamlit.io/): web UI
- [LiteLLM](https://github.com/BerriAI/litellm): LLM provider abstraction and function calling
- [python-dotenv](https://github.com/theskumar/python-dotenv): environment variable loading

## Installation and Setup
1. Clone the repository
   ```sh
   git clone https://github.com/Cellul4r/llm-financial-advisor.git
   cd llm-financial-advisor
   ```
2. Create a virtual environment and install the requirements from **requirements.txt**
   ```sh
   source start.sh
   ```
   On Windows:
   ```sh
   python -m venv .venv
   .venv\Scripts\activate
   pip install -r requirements.txt
   ```
3. Set up environment variables
   ```sh
   cp .env.example .env
   ```
   Then open `.env` and set your `GROQ_API_KEY`. `DEFAULT_MODEL`, `TEMPERATURE`, and `MAX_TOKENS` are optional.
   > Never commit your `.env` file or real API keys.

### Dev Container / Codespaces
The repository includes `.devcontainer/devcontainer.json`. Open it in GitHub Codespaces or VS Code Dev Containers, and the requirements install automatically. The app is served on port `8501`.

## How to run
- Run with Streamlit
  ```sh
  streamlit run main.py
  ```
- Open http://localhost:8501 in your browser.

## Project Structure
```
llm-financial-advisor/
├── main.py                         # Streamlit app entry point; registers all tools
├── tools/                          # Tools the LLM can call
│   ├── tool.py                     # Abstract base class `Tool` and `ToolCall`
│   ├── financial_health_checker_tool.py
│   ├── financial_institution_tool.py
│   ├── financial_loan_tool.py
│   ├── investment_saving_tool.py   # Investment & saving + investment risk
│   ├── tax_calculator_tool.py
│   └── currency_converter_tool.py
├── utils/
│   ├── llm_client.py               # LiteLLM wrapper (chat + tool calling)
│   └── tool_executor.py            # Registers tools and executes tool calls
├── tests/                          # LLM-driven test scripts for each tool
├── resource/img/                   # Images used by the UI
├── .devcontainer/                  # Dev Container / Codespaces config
├── .env.example                    # Template for environment variables
├── start.sh                        # Creates venv and installs dependencies
├── requirements.txt
├── Guide.md                        # Developer guide and git flow
└── slide_presentation.pdf
```

## Running Tests
The tests are scripts that send sample prompts to the LLM and print the results. They are not pytest unit tests. Run them from the repository root with a valid API key in `.env`:
```sh
python -m tests.tax_calculator_test
python -m tests.financial_loan_test
```

## Adding a New Tool
1. Create a new file in `tools/` that subclasses `Tool` from `tools/tool.py`.
2. Implement `get_schemas()` so it returns the function-calling schema(s), and add the tool logic.
3. Register it in `main.py`:
   ```python
   tool_executor.register_tools(YourNewTool())
   ```
4. Add a test script in `tests/`, following the existing ones.

See [Guide.md](Guide.md) for more details.

## Contributing
Contributions are welcome!

### Issues
- Found a bug or have an idea? [Open an issue](https://github.com/Cellul4r/llm-financial-advisor/issues).
- Check existing issues first to avoid duplicates.
- For bugs, include the steps to reproduce, the expected vs. actual behaviour, and screenshots or logs if possible.

### Pull Requests
1. Fork the repository, or create a branch from `main` (`feature/your-feature` or `fix/your-fix`).
2. Keep your changes focused on one feature or fix.
3. Make sure the app still runs (`streamlit run main.py`) and the related tests still pass.
4. Never commit `.env` files or API keys.
5. [Open a pull request](https://github.com/Cellul4r/llm-financial-advisor/pulls) that describes what you changed and how you tested it. Link the related issue (for example, `Closes #12`).

See the git flow in [Guide.md](Guide.md).

## Contributors
 *  [Theerada Siri](https://github.com/Cellul4r) 670510663 - Backend (Tax Calculator Tool)
 * [Krit Thongjib](https://github.com/Not-Tan) 670510689 - Backend (Financial Health Checker Tool)
 * [Pitchayanat Patthamasewee](https://github.com/Fres26) 670510670 - Frontend and Backend (Investment & Saving Tool)
 * [Punchita Sittisarit](https://github.com/q28jes) 670510669 - Backend (Financial Institution and loan Tool)

## Slide Presentation
  - [Canva Link](https://www.canva.com/design/DAG1k1nzBWI/GiDsgFCWvvSzcmjPGEyEQg/edit?utm_content=DAG1k1nzBWI&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton)
  - [PDF version](slide_presentation.pdf)

## Disclaimer
This is an educational project. The responses it generates are not professional financial, investment, or tax advice. Always check important decisions with a qualified professional.

## License
This project is licensed under the [MIT License](LICENSE).
