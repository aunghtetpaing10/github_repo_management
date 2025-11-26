# GitHub Repository Management - AI Agent System

An intelligent multi-agent system powered by [crewAI](https://crewai.com) that automatically creates and configures GitHub repositories from Product Requirements Documents (PRDs).

## What It Does

Give the system a PRD (Product Requirements Document), and it will automatically:
- ✅ Parse and analyze the PRD to extract project details, features, and tech stack
- ✅ Create a new GitHub repository with the project name and description
- ✅ Generate a comprehensive README with all project information
- ✅ **🆕 Scaffold complete project structure** with folders and base files
- ✅ **🆕 Set up framework-specific boilerplate** (FastAPI, React, Node.js)
- ✅ **🆕 Create development branches** and Git configuration
- ✅ Create labeled issues for each feature identified in the PRD
- ✅ Set up project labels for issue categorization
- ✅ Provide a complete development backlog ready for your team

## Architecture

The system uses four specialized AI agents:

1. **PRD Analyst Agent** - Extracts structured information from PRD documents
2. **Repository Creator Agent** - Sets up GitHub repositories with proper configuration
3. **Project Scaffolder Agent** - 🆕 Creates folder structures and base files based on tech stack
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
1. Parse the sample e-commerce PRD included in `main.py`
2. Create a GitHub repository named "e-commerce-platform" 
3. Generate a comprehensive README
4. **🆕 Scaffold complete project structure** based on tech stack
5. Create issues for all features
6. Output a summary report to `project_setup_report.md`

## 🆕 New: Project Scaffolding

The system now automatically creates complete project structures! Based on the tech stack in your PRD:

**For Python/FastAPI projects:**
- Creates `app/`, `tests/`, `docs/` folders
- Adds `main.py`, `config.py`, test files
- Generates `requirements.txt`, `.env.example`, `.gitignore`

**For React projects:**
- Creates `src/components/`, `src/pages/`, `public/` folders
- Adds `App.js`, `index.js`, styling files
- Generates `package.json`, `.gitignore`

**For Node.js/Express projects:**
- Creates `src/routes/`, `src/controllers/`, `tests/` folders
- Adds `index.js`, middleware files
- Generates `package.json`, `.env.example`, `.gitignore`

See [SCAFFOLDING_GUIDE.md](SCAFFOLDING_GUIDE.md) for detailed documentation.

## Using Your Own PRD

Edit `src/github_repo_management/main.py` and replace the `sample_prd` variable with your PRD content:

```python
sample_prd = """
# Your Project Name

## Description
Your project description here

## Tech Stack
- Technology 1
- Technology 2

## Features
- Feature 1 description
- Feature 2 description
- Feature 3 description
"""
```

## PRD Format Guidelines

Your PRD should include:
- **Project Name**: As a heading or "Project: Name"
- **Description**: Project overview and goals
- **Tech Stack**: List of technologies to be used
- **Features**: List of features and functionality

The parser is flexible and can handle various markdown formats.

## Example Output

When you run the system with a PRD, you'll see:

```
✓ PRD Analysis Complete
  - Project: E-Commerce Platform
  - Features Identified: 8
  - Tech Stack: Python, FastAPI, PostgreSQL, React, Redux, Stripe API

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
│   │   ├── agents.yaml          # Agent definitions
│   │   └── tasks.yaml           # Task definitions
│   ├── tools/
│   │   ├── github_tools.py      # GitHub API integration
│   │   ├── prd_parser.py        # PRD parsing logic
│   │   ├── git_tools.py         # 🆕 Git operations (files, branches)
│   │   ├── scaffolding_tools.py # 🆕 Project scaffolding
│   │   └── project_templates.py # 🆕 Framework templates
│   ├── crew.py                  # Crew orchestration
│   └── main.py                  # Entry point
├── examples/
│   └── scaffold_example.py      # 🆕 Usage examples
├── .env.example                 # Environment variables template
├── README.md                    # This file
└── SCAFFOLDING_GUIDE.md         # 🆕 Detailed scaffolding docs
```

## Customization

- **Modify agents**: Edit `src/github_repo_management/config/agents.yaml`
- **Modify tasks**: Edit `src/github_repo_management/config/tasks.yaml`
- **Add new tools**: Create tools in `src/github_repo_management/tools/`
- **Add project templates**: 🆕 Create templates in `src/github_repo_management/tools/project_templates.py`
- **Change workflow**: Update `src/github_repo_management/crew.py`

## Support

For support, questions, or feedback regarding the GithubRepoManagement Crew or crewAI.
- Visit our [documentation](https://docs.crewai.com)
- Reach out to us through our [GitHub repository](https://github.com/joaomdmoura/crewai)
- [Join our Discord](https://discord.com/invite/X4JWnZnxPb)
- [Chat with our docs](https://chatg.pt/DWjSBZn)

Let's create wonders together with the power and simplicity of crewAI.
