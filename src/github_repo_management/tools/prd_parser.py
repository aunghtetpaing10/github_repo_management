from crewai.tools import BaseTool
from typing import Type, Dict, List
from pydantic import BaseModel, Field
import re
import json


class PRDParserInput(BaseModel):
    """Input schema for PRDParserTool."""
    prd_content: str = Field(..., description="The full content of the Product Requirements Document")


class PRDParserTool(BaseTool):
    name: str = "parse_prd_document"
    description: str = (
        "Parses a Product Requirements Document (PRD) and extracts structured information including "
        "project name, description, tech stack, features, and requirements. Returns a JSON structure "
        "with all extracted information."
    )
    args_schema: Type[BaseModel] = PRDParserInput

    def _extract_section(self, content: str, section_name: str) -> str:
        """Extract content from a specific section."""
        patterns = [
            rf"(?:^|\n)#{1,3}\s*{section_name}[:\s]*\n(.*?)(?=\n#{1,3}\s|\Z)",
            rf"(?:^|\n){section_name}[:\s]*\n(.*?)(?=\n[A-Z][a-zA-Z\s]+[:\n]|\Z)",
        ]
        
        for pattern in patterns:
            match = re.search(pattern, content, re.IGNORECASE | re.DOTALL)
            if match:
                return match.group(1).strip()
        return ""

    def _extract_list_items(self, text: str) -> List[str]:
        """Extract list items from text (bullets, numbers, or lines)."""
        items = []
        
        # Try to find bulleted or numbered lists
        lines = text.split('\n')
        for line in lines:
            line = line.strip()
            # Match bullets (-, *, •) or numbers (1., 2., etc.)
            match = re.match(r'^(?:[-*•]|\d+\.)\s+(.+)$', line)
            if match:
                items.append(match.group(1).strip())
            elif line and not line.startswith('#') and len(line) > 3:
                # If not empty and not a header, consider it an item
                items.append(line)
        
        return items

    def _extract_project_name(self, content: str) -> str:
        """Extract project name from PRD."""
        # Look for "Project:", "Project Name:", or first heading
        patterns = [
            r"(?:^|\n)Project(?:\s+Name)?[:\s]+(.+?)(?:\n|$)",
            r"(?:^|\n)#\s+(.+?)(?:\n|$)",
            r"(?:^|\n)Name[:\s]+(.+?)(?:\n|$)"
        ]
        
        for pattern in patterns:
            match = re.search(pattern, content, re.IGNORECASE | re.MULTILINE)
            if match:
                return match.group(1).strip()
        
        return "Untitled Project"

    def _extract_description(self, content: str) -> str:
        """Extract project description."""
        desc = self._extract_section(content, "Description")
        if not desc:
            desc = self._extract_section(content, "Overview")
        if not desc:
            desc = self._extract_section(content, "Summary")
        
        # If still no description, take the first paragraph after project name
        if not desc:
            lines = content.split('\n')
            for i, line in enumerate(lines):
                if line.strip() and not line.startswith('#') and len(line) > 20:
                    desc = line.strip()
                    break
        
        return desc or "No description provided"

    def _extract_tech_stack(self, content: str) -> List[str]:
        """Extract technology stack."""
        tech_text = self._extract_section(content, "Tech(?:nology)?\s+Stack")
        if not tech_text:
            tech_text = self._extract_section(content, "Technologies")
        if not tech_text:
            tech_text = self._extract_section(content, "Stack")
        
        if tech_text:
            items = self._extract_list_items(tech_text)
            if items:
                return items
            # If no list format, try to split by commas
            return [tech.strip() for tech in tech_text.split(',') if tech.strip()]
        
        return []

    def _extract_features(self, content: str) -> List[Dict[str, str]]:
        """Extract features list."""
        features_text = self._extract_section(content, "Features")
        if not features_text:
            features_text = self._extract_section(content, "Functionality")
        if not features_text:
            features_text = self._extract_section(content, "Requirements")
        
        if features_text:
            items = self._extract_list_items(features_text)
            features = []
            for item in items:
                # Try to detect priority
                priority = "Medium"
                if re.search(r'\b(?:must|critical|high|priority)\b', item, re.IGNORECASE):
                    priority = "High"
                elif re.search(r'\b(?:nice|low|optional|should)\b', item, re.IGNORECASE):
                    priority = "Low"
                
                features.append({
                    "title": item,
                    "priority": priority,
                    "description": item
                })
            return features
        
        return []

    def _run(self, prd_content: str) -> str:
        try:
            # Extract all information
            project_name = self._extract_project_name(prd_content)
            description = self._extract_description(prd_content)
            tech_stack = self._extract_tech_stack(prd_content)
            features = self._extract_features(prd_content)
            
            # Create structured output
            result = {
                "project_name": project_name,
                "description": description,
                "tech_stack": tech_stack,
                "features": features,
                "feature_count": len(features)
            }
            
            return json.dumps(result, indent=2)
        except Exception as e:
            return f"Error parsing PRD: {str(e)}"
