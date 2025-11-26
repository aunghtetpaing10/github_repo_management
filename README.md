# GitHub Repository Management - AI Agent System

An intelligent multi-agent system powered by [crewAI](https://crewai.com) that automatically creates and configures complete GitHub repositories from simple project ideas. **Just describe what you want to build, and AI does the rest!**

## What It Does

**Simply describe your project idea in plain language**, and the system will automatically:
- ✅ **🆕 Generate a comprehensive PRD** from your simple description
- ✅ Recommend appropriate tech stack based on your requirements
- ✅ Parse and analyze the generated PRD to extract project details
- ✅ Create a new GitHub repository with the project name and description
- ✅ Generate a comprehensive README with all project information
- ✅ Create labeled issues for each feature identified in the PRD
- ✅ Set up project labels for issue categorization
- ✅ Provide a complete development backlog ready for your team

## Architecture

The system uses four specialized AI agents:

1. **PRD Generator Agent** - 🆕 Transforms simple ideas into comprehensive PRDs
2. **PRD Analyst Agent** - Extracts structured information from PRD documents
3. **Repository Creator Agent** - Sets up GitHub repositories with proper configuration
4. **Issue Manager Agent** - Creates and organizes issues from feature requirements

## Prerequisites

- Python >=3.10 <3.14
- OpenAI API Key
- GitHub Personal Access Token

## Installation

1. **Install UV** (Python package manager):
```bash
pip install uv
```

2. **Install dependencies**:
```bash
crewai install
```

3. **Configure environment variables**:
   - Copy `.env.example` to `.env`
   - Add your `OPENAI_API_KEY`
   - Add your `GITHUB_TOKEN` (create one at https://github.com/settings/tokens)
     - Required scope: `repo` (full control of private repositories)

```bash
cp .env.example .env
# Then edit .env with your keys
```

## Quick Start

Run the prototype with the sample PRD:

```bash
crewai run
```

The system will:
1. **🆕 Generate a comprehensive PRD** from your simple project idea
2. Analyze and extract project details, tech stack, and features
3. Create a GitHub repository with appropriate name
4. Generate a comprehensive README
5. Create issues for all features

## Running Individual Agents

You can run specific agents independently instead of the full workflow:
```bash
python test_single_agent.py
```

**Use cases:**
- Test PRD generation without creating GitHub resources
- Test issue creation on an existing repository
- Debug specific agent configurations
- Iterate quickly on prompt improvements

---

## Using Your Own Project Idea

Edit `src/github_repo_management/main.py` and replace the `project_idea` variable with your own description:

```python
project_idea = """
I want to build a task management app where teams can collaborate,
assign tasks, track progress, and get notifications. It should have
user authentication, real-time updates, and a mobile-friendly interface.
"""
```

**That's it!** No need to specify tech stack or write a formal PRD. The AI will:
- Recommend appropriate technologies
- Generate a complete PRD
- Set up your GitHub repository

## Project Idea Guidelines

**Just describe what you want to build!** You can mention:
- **What the project does** - Main purpose and functionality
- **Key features** - What users should be able to do
- **Target users** - Who will use it (optional)
- **Special requirements** - Any specific needs (optional)

The AI will figure out the best tech stack and generate a complete PRD for you.

## Example Output

When you run the system with a simple idea, you'll see:

```
✓ PRD Generated
  - Project: E-Commerce Platform  
  - Tech Stack Recommended: Python, FastAPI, PostgreSQL, React, Redux, Stripe API
  
✓ PRD Analysis Complete
  - Features Identified: 8
  - All requirements structured

✓ Repository Created
  - URL: https://github.com/yourusername/e-commerce-platform
  - README: Generated with full project details
  - Labels: Created (feature, bug, enhancement, documentation)

✓ Issues Created
  - #1 User authentication and profile management
  - #2 Product catalog with search and filtering
  - #3 Shopping cart functionality
  - #4 Secure payment processing with Stripe
  - #5 Order tracking and history
  - #6 Admin dashboard for inventory management
  - #7 Email notifications for orders
  - #8 Product reviews and ratings

✓ Project Setup Complete!
```

## Project Structure

```
github_repo_management/
├── src/github_repo_management/
│   ├── config/
│   │   ├── agents.yaml          # Agent definitions (4 agents)
│   │   └── tasks.yaml           # Task definitions
│   ├── tools/
│   │   ├── github_tools.py      # GitHub API integration
│   │   └── prd_parser.py        # PRD parsing logic
│   ├── crew.py                  # Crew orchestration
│   └── main.py                  # Entry point
├── .env.example                 # Environment variables template
└── README.md                    # This file
```

## Customization

- **Modify agents**: Edit `src/github_repo_management/config/agents.yaml`
- **Modify tasks**: Edit `src/github_repo_management/config/tasks.yaml`
- **Add new tools**: Create tools in `src/github_repo_management/tools/`
- **Change workflow**: Update `src/github_repo_management/crew.py`
