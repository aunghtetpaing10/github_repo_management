"""
Project templates for different technology stacks.
Templates define folder structures and base files for quick scaffolding.
"""

from typing import Dict, List


class ProjectTemplate:
    """Base class for project templates."""

    def __init__(self, project_name: str):
        self.project_name = project_name

    def get_folders(self) -> List[str]:
        """Returns list of folders to create."""
        raise NotImplementedError

    def get_files(self) -> List[Dict[str, str]]:
        """Returns list of files with path and content."""
        raise NotImplementedError


class PythonFastAPITemplate(ProjectTemplate):
    """Template for Python FastAPI projects."""

    def get_folders(self) -> List[str]:
        return [
            "app",
            "app/api",
            "app/core",
            "app/models",
            "app/services",
            "tests",
            "docs",
        ]

    def get_files(self) -> List[Dict[str, str]]:
        return [
            {"path": "app/__init__.py", "content": ""},
            {
                "path": "app/main.py",
                "content": f'''"""
{self.project_name} - FastAPI Application
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="{self.project_name}",
    description="API for {self.project_name}",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {{"message": "Welcome to {self.project_name}"}}


@app.get("/health")
async def health_check():
    return {{"status": "healthy"}}
''',
            },
            {"path": "app/core/__init__.py", "content": ""},
            {
                "path": "app/core/config.py",
                "content": '''"""
Application configuration.
"""
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""
    
    app_name: str = "FastAPI App"
    debug: bool = False
    api_version: str = "v1"
    
    class Config:
        env_file = ".env"


settings = Settings()
''',
            },
            {"path": "app/api/__init__.py", "content": ""},
            {"path": "app/models/__init__.py", "content": ""},
            {"path": "app/services/__init__.py", "content": ""},
            {"path": "tests/__init__.py", "content": ""},
            {
                "path": "tests/test_main.py",
                "content": '''"""
Tests for main application.
"""
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
''',
            },
            {
                "path": "requirements.txt",
                "content": """fastapi==0.104.1
uvicorn[standard]==0.24.0
pydantic-settings==2.1.0
python-dotenv==1.0.0
pytest==7.4.3
httpx==0.25.2
""",
            },
            {
                "path": ".env.example",
                "content": """# Application Configuration
APP_NAME=FastAPI App
DEBUG=False
API_VERSION=v1
""",
            },
            {
                "path": ".gitignore",
                "content": """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
.venv/
ENV/
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Environment
.env
.env.local

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# Testing
.pytest_cache/
.coverage
htmlcov/

# OS
.DS_Store
Thumbs.db
""",
            },
        ]


class ReactTemplate(ProjectTemplate):
    """Template for React projects."""

    def get_folders(self) -> List[str]:
        return [
            "src",
            "src/components",
            "src/pages",
            "src/hooks",
            "src/utils",
            "src/services",
            "public",
        ]

    def get_files(self) -> List[Dict[str, str]]:
        return [
            {
                "path": "package.json",
                "content": f'''{{
  "name": "{self.project_name.lower().replace(" ", "-")}",
  "version": "0.1.0",
  "private": true,
  "dependencies": {{
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-scripts": "5.0.1"
  }},
  "scripts": {{
    "start": "react-scripts start",
    "build": "react-scripts build",
    "test": "react-scripts test",
    "eject": "react-scripts eject"
  }},
  "eslintConfig": {{
    "extends": [
      "react-app"
    ]
  }},
  "browserslist": {{
    "production": [
      ">0.2%",
      "not dead",
      "not op_mini all"
    ],
    "development": [
      "last 1 chrome version",
      "last 1 firefox version",
      "last 1 safari version"
    ]
  }}
}}
''',
            },
            {
                "path": "src/index.js",
                "content": """import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
""",
            },
            {
                "path": "src/App.js",
                "content": f"""import React from 'react';
import './App.css';

function App() {{
  return (
    <div className="App">
      <header className="App-header">
        <h1>{self.project_name}</h1>
        <p>Welcome to your React application!</p>
      </header>
    </div>
  );
}}

export default App;
""",
            },
            {
                "path": "src/App.css",
                "content": """.App {
  text-align: center;
}

.App-header {
  background-color: #282c34;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  font-size: calc(10px + 2vmin);
  color: white;
}
""",
            },
            {
                "path": "src/index.css",
                "content": """body {
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
    'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue',
    sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

code {
  font-family: source-code-pro, Menlo, Monaco, Consolas, 'Courier New',
    monospace;
}
""",
            },
            {
                "path": "public/index.html",
                "content": f'''<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <meta name="theme-color" content="#000000" />
    <meta name="description" content="{self.project_name}" />
    <title>{self.project_name}</title>
  </head>
  <body>
    <noscript>You need to enable JavaScript to run this app.</noscript>
    <div id="root"></div>
  </body>
</html>
''',
            },
            {
                "path": ".gitignore",
                "content": """# Dependencies
node_modules/
/.pnp
.pnp.js

# Testing
/coverage

# Production
/build

# Misc
.DS_Store
.env.local
.env.development.local
.env.test.local
.env.production.local

npm-debug.log*
yarn-debug.log*
yarn-error.log*
""",
            },
        ]


class NodeExpressTemplate(ProjectTemplate):
    """Template for Node.js Express projects."""

    def get_folders(self) -> List[str]:
        return [
            "src",
            "src/routes",
            "src/controllers",
            "src/models",
            "src/middleware",
            "src/config",
            "tests",
        ]

    def get_files(self) -> List[Dict[str, str]]:
        return [
            {
                "path": "package.json",
                "content": f'''{{
  "name": "{self.project_name.lower().replace(" ", "-")}",
  "version": "1.0.0",
  "description": "{self.project_name}",
  "main": "src/index.js",
  "scripts": {{
    "start": "node src/index.js",
    "dev": "nodemon src/index.js",
    "test": "jest"
  }},
  "dependencies": {{
    "express": "^4.18.2",
    "dotenv": "^16.3.1",
    "cors": "^2.8.5"
  }},
  "devDependencies": {{
    "nodemon": "^3.0.1",
    "jest": "^29.7.0"
  }}
}}
''',
            },
            {
                "path": "src/index.js",
                "content": f"""const express = require('express');
const cors = require('cors');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(cors());
app.use(express.json());
app.use(express.urlencoded({{ extended: true }}));

// Routes
app.get('/', (req, res) => {{
  res.json({{ message: 'Welcome to {self.project_name}' }});
}});

app.get('/health', (req, res) => {{
  res.json({{ status: 'healthy' }});
}});

// Start server
app.listen(PORT, () => {{
  console.log(`Server running on port ${{PORT}}`);
}});

module.exports = app;
""",
            },
            {
                "path": ".env.example",
                "content": """PORT=3000
NODE_ENV=development
""",
            },
            {
                "path": ".gitignore",
                "content": """node_modules/
.env
.env.local
npm-debug.log*
yarn-debug.log*
yarn-error.log*
.DS_Store
""",
            },
        ]


# Template registry
TEMPLATES = {
    "python-fastapi": PythonFastAPITemplate,
    "react": ReactTemplate,
    "node-express": NodeExpressTemplate,
}


def get_template(template_name: str, project_name: str) -> ProjectTemplate:
    """
    Get a project template by name.

    Args:
        template_name: Name of the template (e.g., 'python-fastapi', 'react')
        project_name: Name of the project

    Returns:
        ProjectTemplate instance

    Raises:
        ValueError: If template not found
    """
    template_class = TEMPLATES.get(template_name.lower())
    if not template_class:
        available = ", ".join(TEMPLATES.keys())
        raise ValueError(
            f"Template '{template_name}' not found. Available: {available}"
        )

    return template_class(project_name)


def list_templates() -> List[str]:
    """Returns list of available template names."""
    return list(TEMPLATES.keys())
