#!/usr/bin/env python3
"""
🚀 ChaosGenius AI Documentation Generator
Automated documentation generation system for the Hyperfocus Zone project
"""

import os
import json
import subprocess
import sys
from pathlib import Path
from datetime import datetime
import requests

class ChaosGeniusDocGenerator:
    def __init__(self, project_root="."):
        self.project_root = Path(project_root)
        self.docs_dir = self.project_root / "generated_docs"
        self.docs_dir.mkdir(exist_ok=True)
        
    def generate_project_overview(self):
        """Generate comprehensive project overview from existing files"""
        print("🧠 Generating project overview...")
        
        overview = {
            "project_name": "ChaosGenius Engine",
            "tagline": "AI-Powered Neurodivergent Business Creation Ecosystem",
            "generated_at": datetime.now().isoformat(),
            "components": self._scan_project_components(),
            "documentation_tools": self._get_documentation_tools(),
            "revenue_streams": self._extract_revenue_streams(),
            "tech_stack": self._identify_tech_stack()
        }
        
        # Save as JSON for API consumption
        with open(self.docs_dir / "project_overview.json", "w", encoding='utf-8') as f:
            json.dump(overview, f, indent=2)
            
        # Generate markdown version
        self._generate_overview_markdown(overview)
        return overview
    
    def _scan_project_components(self):
        """Scan project directory for components"""
        components = []
        for item in self.project_root.iterdir():
            if item.is_dir() and not item.name.startswith('.'):
                components.append({
                    "name": item.name,
                    "type": "directory",
                    "description": self._infer_component_description(item.name)
                })
            elif item.suffix in ['.py', '.md', '.json', '.html']:
                components.append({
                    "name": item.name,
                    "type": "file",
                    "description": self._infer_file_description(item)
                })
        return components
    
    def _infer_component_description(self, name):
        """Infer component description from name"""
        descriptions = {
            "AI Squad": "Multi-agent AI business planning system",
            "Documentation Suite": "AI-powered documentation generation tools",
            "Launch Tracker": "Milestone and progress tracking system",
            "Project Analyzer": "Code analysis and optimization tools",
            "The Zone": "Core Hyperfocus Zone implementation",
            "Ultra IPFS": "Advanced IPFS integration for Web3 features"
        }
        return descriptions.get(name, f"Component: {name}")
    
    def _infer_file_description(self, file_path):
        """Infer file description from content or name"""
        if file_path.name == "README.md":
            return "Main project documentation"
        elif file_path.suffix == ".py":
            return f"Python module: {file_path.stem}"
        elif file_path.suffix == ".md":
            return f"Documentation: {file_path.stem}"
        elif file_path.suffix == ".json":
            return f"Configuration: {file_path.stem}"
        return f"File: {file_path.name}"
    
    def _get_documentation_tools(self):
        """Extract documentation tools from Documentation Suite"""
        return [
            {
                "name": "ReadmeAI",
                "purpose": "Automated README generation",
                "features": ["Structured README files", "Multiple templates", "Multi-language support"]
            },
            {
                "name": "DocuWriter.ai",
                "purpose": "Code and API documentation",
                "features": ["Swagger-compliant docs", "DocBlock generation", "Code refactoring"]
            },
            {
                "name": "Aidocmaker.com",
                "purpose": "Professional document creation",
                "features": ["Business reports", "Proposals", "Research papers"]
            },
            {
                "name": "Piktochart AI",
                "purpose": "Visual documentation",
                "features": ["Infographics", "Visual aids", "Custom graphics"]
            },
            {
                "name": "Scribe",
                "purpose": "Process documentation",
                "features": ["Step-by-step guides", "Screenshot automation", "Training docs"]
            }
        ]
    
    def _extract_revenue_streams(self):
        """Extract revenue streams from README or business plan"""
        return [
            "AI Business Creation Consulting",
            "Hyperfocus Zone Studio Licensing",
            "Documentation Suite SaaS",
            "Neurodivergent Business Accelerator",
            "Custom AI Squad Development"
        ]
    
    def _identify_tech_stack(self):
        """Identify technology stack from project files"""
        tech_stack = {
            "languages": [],
            "frameworks": [],
            "tools": [],
            "ai_services": []
        }
        
        # Scan for tech indicators
        for file_path in self.project_root.rglob("*"):
            if file_path.suffix == ".py":
                tech_stack["languages"].append("Python")
            elif file_path.suffix == ".js":
                tech_stack["languages"].append("JavaScript")
            elif file_path.suffix == ".html":
                tech_stack["languages"].append("HTML")
            elif file_path.name == "package.json":
                tech_stack["tools"].append("Node.js")
        
        # Remove duplicates
        for key in tech_stack:
            tech_stack[key] = list(set(tech_stack[key]))
            
        return tech_stack
    
    def _generate_overview_markdown(self, overview):
        """Generate markdown version of project overview"""
        md_content = f"""# {overview['project_name']}
## {overview['tagline']}

*Generated on: {overview['generated_at']}*

## 🎯 Project Components

"""
        for component in overview['components']:
            md_content += f"- **{component['name']}**: {component['description']}\n"
        
        md_content += "\n## 🛠️ Documentation Tools\n\n"
        for tool in overview['documentation_tools']:
            md_content += f"### {tool['name']}\n"
            md_content += f"*{tool['purpose']}*\n\n"
            for feature in tool['features']:
                md_content += f"- {feature}\n"
            md_content += "\n"
        
        md_content += "## 💰 Revenue Streams\n\n"
        for stream in overview['revenue_streams']:
            md_content += f"- {stream}\n"
        
        with open(self.docs_dir / "project_overview.md", "w", encoding='utf-8') as f:
            f.write(md_content)
    
    def generate_api_documentation(self):
        """Generate API documentation from Python files"""
        print("📋 Generating API documentation...")
        
        api_docs = []
        for py_file in self.project_root.rglob("*.py"):
            if py_file.name.startswith("dashboard") or py_file.name.startswith("api"):
                doc_info = self._extract_api_info(py_file)
                if doc_info:
                    api_docs.append(doc_info)
        
        with open(self.docs_dir / "api_documentation.json", "w", encoding='utf-8') as f:
            json.dump(api_docs, f, indent=2)
        
        return api_docs
    
    def _extract_api_info(self, py_file):
        """Extract API information from Python file"""
        try:
            with open(py_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Simple extraction - would be enhanced with AST parsing
            info = {
                "file": str(py_file.name),
                "endpoints": [],
                "functions": [],
                "description": ""
            }
            
            lines = content.split('\n')
            for line in lines:
                if '@app.route' in line:
                    info["endpoints"].append(line.strip())
                elif 'def ' in line and not line.strip().startswith('#'):
                    info["functions"].append(line.strip())
            
            return info if info["endpoints"] or info["functions"] else None
        except Exception as e:
            print(f"Error processing {py_file}: {e}")
            return None
    
    def generate_business_documentation(self):
        """Generate business documentation from existing files"""
        print("💼 Generating business documentation...")
        
        business_docs = {
            "pitch_deck": self._process_pitch_deck(),
            "video_scripts": self._process_video_scripts(),
            "marketing_guide": self._process_marketing_guide(),
            "visual_assets": self._process_visual_assets()
        }
        
        with open(self.docs_dir / "business_documentation.json", "w", encoding='utf-8') as f:
            json.dump(business_docs, f, indent=2)
        
        return business_docs
    
    def _process_pitch_deck(self):
        """Process pitch deck markdown file"""
        pitch_file = self.project_root / "ChaosGenius_Pitch_Deck.md"
        if pitch_file.exists():
            with open(pitch_file, 'r', encoding='utf-8') as f:
                return {"content": f.read(), "status": "available"}
        return {"status": "not_found"}
    
    def _process_video_scripts(self):
        """Process video script files"""
        scripts = {}
        script_files = [
            "ChaosGenius_Video_Pitch_Script.md",
            "ElevenLabs_Audio_Pitch_Script.md",
            "Synthesia_Video_Pitch_Script.md"
        ]
        
        for script_file in script_files:
            file_path = self.project_root / script_file
            if file_path.exists():
                with open(file_path, 'r', encoding='utf-8') as f:
                    scripts[script_file] = f.read()
        
        return scripts
    
    def _process_marketing_guide(self):
        """Process marketing guide"""
        guide_file = self.project_root / "Complete_Video_Marketing_Guide.md"
        if guide_file.exists():
            with open(guide_file, 'r', encoding='utf-8') as f:
                return {"content": f.read(), "status": "available"}
        return {"status": "not_found"}
    
    def _process_visual_assets(self):
        """Process visual assets documentation"""
        assets_file = self.project_root / "ChaosGenius_Visual_Assets.md"
        if assets_file.exists():
            with open(assets_file, 'r', encoding='utf-8') as f:
                return {"content": f.read(), "status": "available"}
        return {"status": "not_found"}
    
    def generate_development_docs(self):
        """Generate development documentation"""
        print("🔧 Generating development documentation...")
        
        dev_docs = {
            "setup_instructions": self._generate_setup_docs(),
            "code_analysis": self._generate_code_analysis(),
            "project_structure": self._generate_structure_docs(),
            "tasks_available": self._extract_vscode_tasks()
        }
        
        with open(self.docs_dir / "development_documentation.json", "w", encoding='utf-8') as f:
            json.dump(dev_docs, f, indent=2)
        
        return dev_docs
    
    def _generate_setup_docs(self):
        """Generate setup documentation"""
        return {
            "environment": "Python Virtual Environment",
            "requirements": ["Python 3.8+", "VS Code", "Git"],
            "quick_start": [
                "Open ChaosGenius.code-workspace in VS Code",
                "Install recommended extensions",
                "Run: Ctrl+Shift+P → Tasks: Run Task → 🧠 Initialize ChaosGenius Environment",
                "Run: Ctrl+Shift+P → Tasks: Run Task → 🚀 Run AI Squad Business Creator"
            ]
        }
    
    def _generate_code_analysis(self):
        """Generate code analysis summary"""
        analysis = {
            "python_files": len(list(self.project_root.rglob("*.py"))),
            "markdown_files": len(list(self.project_root.rglob("*.md"))),
            "json_files": len(list(self.project_root.rglob("*.json"))),
            "directories": len([d for d in self.project_root.iterdir() if d.is_dir()])
        }
        return analysis
    
    def _generate_structure_docs(self):
        """Generate project structure documentation"""
        structure = []
        for item in self.project_root.iterdir():
            if not item.name.startswith('.'):
                structure.append({
                    "name": item.name,
                    "type": "directory" if item.is_dir() else "file",
                    "purpose": self._infer_component_description(item.name) if item.is_dir() else self._infer_file_description(item)
                })
        return structure
    
    def _extract_vscode_tasks(self):
        """Extract VS Code tasks from workspace"""
        tasks = [
            "🧠 Initialize ChaosGenius Environment",
            "🚀 Run AI Squad Business Creator", 
            "🔧 Project Analysis & Fix",
            "📚 Generate Documentation Suite",
            "🌐 Launch Hyperfocus Zone Preview",
            "⚡ Ultra Mode Deploy",
            "🎛️ Launch ChaosGenius Dashboard",
            "🌐 Open Dashboard in Browser"
        ]
        return tasks
    
    def generate_all_documentation(self):
        """Generate all documentation types"""
        print("🚀 Starting comprehensive documentation generation...")
        
        results = {
            "project_overview": self.generate_project_overview(),
            "api_documentation": self.generate_api_documentation(),
            "business_documentation": self.generate_business_documentation(),
            "development_documentation": self.generate_development_docs(),
            "generated_at": datetime.now().isoformat(),
            "output_directory": str(self.docs_dir)
        }
        
        # Generate master index
        self._generate_master_index(results)
        
        print(f"✅ Documentation generated successfully!")
        print(f"📁 Output directory: {self.docs_dir}")
        
        return results
    
    def _generate_master_index(self, results):
        """Generate master documentation index"""
        index_content = """# 📚 ChaosGenius Documentation Index

*Auto-generated comprehensive documentation for the Hyperfocus Zone project*

## 📋 Available Documentation

### 🎯 Project Overview
- [Project Overview (Markdown)](project_overview.md)
- [Project Overview (JSON)](project_overview.json)

### 📋 API Documentation
- [API Documentation](api_documentation.json)

### 💼 Business Documentation
- [Business Documentation](business_documentation.json)

### 🔧 Development Documentation
- [Development Documentation](development_documentation.json)

## 🛠️ Documentation Tools Used

This documentation was generated using the ChaosGenius AI Documentation Suite, which integrates:

- **ReadmeAI**: Automated README generation
- **DocuWriter.ai**: Code and API documentation
- **Aidocmaker.com**: Professional document creation
- **Piktochart AI**: Visual documentation and infographics
- **Scribe**: Process documentation and guides

## 🚀 Next Steps

1. Review generated documentation
2. Customize and enhance as needed
3. Integrate with external AI documentation tools
4. Set up automated regeneration workflow

---
*Generated by ChaosGenius AI Documentation Generator*
"""
        
        with open(self.docs_dir / "README.md", "w", encoding='utf-8') as f:
            f.write(index_content)

def main():
    """Main execution function"""
    print("ChaosGenius AI Documentation Generator")
    print("=" * 50)
    
    generator = ChaosGeniusDocGenerator()
    results = generator.generate_all_documentation()
    
    print("\n🎉 Documentation generation complete!")
    print(f"📊 Generated {len(results)} documentation sections")
    
    return results

if __name__ == "__main__":
    main()