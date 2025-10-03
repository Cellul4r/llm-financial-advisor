# Project Guide: llm-financial-advisor

## Repository Structure

- `main.py`: Main entry point for the application.
- `README.md`: Project overview and basic instructions.
- `requirements.txt`: Python dependencies for the project.
- `tools/`: Contains modular tools for financial analysis:
  - `financial_health_checker_tool.py`: Checks financial health.
  - `financial_institution_tool.py`: Interacts with financial institutions.
  - `investment_saving_tool.py`: Handles investment and saving logic.
  - `tool.py`: Base or shared tool logic.
- `utils/`: Utility functions and helpers:
  - `llm_client.py`: Handles LLM (Large Language Model) interactions.
- `tests/`: Contains test cases for the project.

## Setup Instructions

1. **Install dependencies:**
   ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    pip install litellm python-dotenv
   pip install -r requirements.txt
   ```
## Git Flow & Commands

- **Branching:**
  - Work on feature branches (e.g., `feature/tool-update`) and merge into `main` via pull requests.
- **Basic commands:**
  ```bash
  git checkout -b feature/your-feature   # Create and switch to a new branch
  git add .                             # Stage changes
  git commit -m "Describe your changes" # Commit changes
  git push origin feature/your-feature  # Push branch to remote
  git pull origin main                  # Pull latest changes from main
  git merge feature/your-feature        # Merge your branch into main
  ```
- **Pull Requests:**
  - Open a PR for code review before merging to `main`.

## Tool Calling

- Tools in the `tools/` directory are modular and can be called from `main.py` or other modules.
- When adding new tools:
  - Place them in the `tools/` directory.
  - Follow the structure and naming conventions of existing tools.
  - Update imports in `main.py` or relevant files.
- Document tool usage and expected inputs/outputs in code comments.

---
For any questions, refer to the `README.md` or contact the project maintainer.
