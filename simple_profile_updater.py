#!/usr/bin/env python3
"""
Simple GitHub Profile Updater
Works with provided project names to generate enhanced profile
"""

import json
import os
from datetime import datetime
from typing import Dict, List
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class SimpleProjectAnalyzer:
    """Analyzes projects based on provided names and descriptions."""
    
    def __init__(self):
        # Define your projects with their details
        self.projects = [
            {
                "name": "new-saas",
                "type": "web_application",
                "description": "Modern SaaS platform with subscription management and user authentication",
                "technologies": ["saas", "subscription", "billing", "authentication", "web-platform"],
                "languages": ["javascript", "typescript", "html", "css"],
                "frameworks": ["react", "node.js", "express", "next.js"],
                "databases": ["mongodb", "postgresql"],
                "tools": ["git", "github", "vscode", "docker"],
                "complexity_score": 85
            },
            {
                "name": "saas-platform",
                "type": "web_application",
                "description": "Comprehensive SaaS platform with multi-tenant architecture and advanced features",
                "technologies": ["saas", "multi-tenant", "api", "microservices", "cloud"],
                "languages": ["javascript", "typescript", "python", "html", "css"],
                "frameworks": ["react", "vue.js", "django", "fastapi", "express"],
                "databases": ["mysql", "redis", "elasticsearch"],
                "tools": ["git", "docker", "kubernetes", "aws", "ci-cd"],
                "complexity_score": 90
            },
            {
                "name": "final year project",
                "type": "academic_project",
                "description": "Comprehensive final year academic project demonstrating full-stack development skills",
                "technologies": ["full-stack", "academic", "research", "documentation", "presentation"],
                "languages": ["python", "javascript", "java", "php", "html", "css"],
                "frameworks": ["django", "react", "spring", "laravel", "bootstrap"],
                "databases": ["mysql", "postgresql", "mongodb", "sqlite"],
                "tools": ["git", "github", "vscode", "docker", "postman"],
                "complexity_score": 95
            },
            {
                "name": "birth-certificate-system",
                "type": "web_application",
                "description": "Digital birth certificate management system with blockchain integration and QR code verification",
                "technologies": ["blockchain", "qr-code", "authentication", "digital-identity", "security"],
                "languages": ["php", "javascript", "html", "css", "sql"],
                "frameworks": ["laravel", "bootstrap", "jquery", "web3"],
                "databases": ["mysql", "blockchain"],
                "tools": ["git", "composer", "npm", "blockchain-tools"],
                "complexity_score": 88
            },
            {
                "name": "enterprise-appdata-cleaner",
                "type": "automation",
                "description": "Enterprise application data cleaning and management tool for large organizations",
                "technologies": ["automation", "data-cleaning", "enterprise", "workflow", "data-management"],
                "languages": ["python", "javascript", "powershell", "sql"],
                "frameworks": ["pandas", "numpy", "flask", "express"],
                "databases": ["mysql", "postgresql", "sql-server", "oracle"],
                "tools": ["n8n", "zapier", "git", "docker", "aws"],
                "complexity_score": 82
            }
        ]
    
    def analyze_projects(self) -> Dict:
        """Analyze all projects for insights."""
        analysis = {
            'total_projects': len(self.projects),
            'project_types': {},
            'technologies': {},
            'languages': {},
            'frameworks': {},
            'databases': {},
            'tools': {},
            'recent_projects': self.projects,
            'complex_projects': [],
            'skill_levels': {}
        }
        
        # Categorize projects
        for project in self.projects:
            # Project types
            ptype = project.get('type', 'unknown')
            analysis['project_types'][ptype] = analysis['project_types'].get(ptype, 0) + 1
            
            # Technologies
            for tech in project.get('technologies', []):
                analysis['technologies'][tech] = analysis['technologies'].get(tech, 0) + 1
            
            # Languages
            for lang in project.get('languages', []):
                analysis['languages'][lang] = analysis['languages'].get(lang, 0) + 1
            
            # Frameworks
            for framework in project.get('frameworks', []):
                analysis['frameworks'][framework] = analysis['frameworks'].get(framework, 0) + 1
            
            # Databases
            for db in project.get('databases', []):
                analysis['databases'][db] = analysis['databases'].get(db, 0) + 1
            
            # Tools
            for tool in project.get('tools', []):
                analysis['tools'][tool] = analysis['tools'].get(tool, 0) + 1
            
            # Complex projects
            if project.get('complexity_score', 0) > 80:
                analysis['complex_projects'].append(project)
        
        # Sort by frequency
        analysis['technologies'] = dict(sorted(analysis['technologies'].items(), key=lambda x: x[1], reverse=True))
        analysis['languages'] = dict(sorted(analysis['languages'].items(), key=lambda x: x[1], reverse=True))
        analysis['frameworks'] = dict(sorted(analysis['frameworks'].items(), key=lambda x: x[1], reverse=True))
        
        return analysis

class SimpleProfileGenerator:
    """Generates updated GitHub profile based on project analysis."""
    
    def __init__(self):
        pass
        
    def generate_profile(self, projects: List[Dict], current_profile: str) -> str:
        """Generate updated GitHub profile."""
        try:
            # Analyze projects
            analyzer = SimpleProjectAnalyzer()
            analysis = analyzer.analyze_projects()
            
            # Generate new sections
            new_sections = self.generate_new_sections(analysis, projects)
            
            # Update existing profile
            updated_profile = self.update_existing_profile(current_profile, new_sections)
            
            return updated_profile
            
        except Exception as e:
            logger.error(f"Error generating profile: {e}")
            return current_profile
    
    def generate_new_sections(self, analysis: Dict, projects: List[Dict]) -> Dict:
        """Generate new profile sections based on analysis."""
        sections = {}
        
        # Current focus
        sections['current_focus'] = self.generate_current_focus(analysis)
        
        # Featured projects
        sections['featured_projects'] = self.generate_featured_projects(projects, analysis)
        
        # Tech stack
        sections['tech_stack'] = self.generate_tech_stack(analysis)
        
        # Recent achievements
        sections['recent_achievements'] = self.generate_recent_achievements(analysis)
        
        # Skills matrix
        sections['skills_matrix'] = self.generate_skills_matrix(analysis)
        
        return sections
    
    def generate_current_focus(self, analysis: Dict) -> str:
        """Generate current focus section."""
        recent_techs = list(analysis['technologies'].keys())[:5]
        recent_langs = list(analysis['languages'].keys())[:3]
        
        focus = "## 🌱 Current Focus\n\n"
        focus += "Based on my recent development activities, I'm currently focused on:\n\n"
        
        if recent_techs:
            focus += f"- **Technologies**: {', '.join(recent_techs[:3])}\n"
        if recent_langs:
            focus += f"- **Languages**: {', '.join(recent_langs)}\n"
        if analysis['recent_projects']:
            focus += f"- **Active Projects**: {len(analysis['recent_projects'])} projects in development\n"
        
        focus += f"- **Learning**: Advanced concepts in {', '.join(list(analysis['languages'].keys())[:2])}\n"
        focus += "- **Specialization**: Full-stack development with focus on SaaS platforms and enterprise solutions\n"
        
        return focus
    
    def generate_featured_projects(self, projects: List[Dict], analysis: Dict) -> str:
        """Generate featured projects section."""
        # Sort projects by complexity
        sorted_projects = sorted(projects, key=lambda x: x.get('complexity_score', 0), reverse=True)
        
        featured = "## 🚀 Featured Projects\n\n"
        
        # Keep existing primary project
        featured += "### Digital Birth Certificate System\n"
        featured += "A modern, secure, and comprehensive digital birth certificate management system built with **PHP 8.4**, featuring:\n"
        featured += "- 🔐 **Multi-role Authentication** (Parents, Hospitals, Registrars, Admins)\n"
        featured += "- 📱 **QR Code Verification** for instant certificate validation\n"
        featured += "- ⛓️ **Blockchain Integration** for immutable certificate storage\n"
        featured += "- 🛡️ **Advanced Security** (CSRF protection, rate limiting, SQL injection prevention)\n"
        featured += "- 📊 **Admin Dashboard** with comprehensive analytics\n"
        featured += "- 🔄 **RESTful API** with 24+ endpoints\n"
        featured += "- 📱 **Responsive Design** with modern UI/UX\n\n"
        featured += "**Status**: ✅ **Production Ready** - Fully operational, not deployed yet :/\n\n"
        featured += "**Tech Stack**: PHP 8.4, MySQL 8.0, HTML5/CSS3, JavaScript ES6+, Bootstrap, Blockchain\n\n"
        featured += "[View Project →](https://github.com/tonycondone/birth-certificate-system)\n\n"
        
        # Add newly discovered projects
        if sorted_projects:
            featured += "### Recently Discovered Projects\n\n"
            for i, project in enumerate(sorted_projects[:4]):
                featured += f"#### {project['name'].replace('-', ' ').title()}\n"
                featured += f"**Type**: {project['type'].replace('_', ' ').title()}\n"
                featured += f"**Complexity**: {project.get('complexity_score', 0)}/100\n"
                featured += f"**Technologies**: {', '.join(project.get('technologies', [])[:5])}\n"
                featured += f"**Description**: {project.get('description', 'Development project')}\n"
                featured += f"**Languages**: {', '.join(project.get('languages', [])[:3])}\n"
                featured += f"**Frameworks**: {', '.join(project.get('frameworks', [])[:3])}\n\n"
        
        return featured
    
    def generate_tech_stack(self, analysis: Dict) -> str:
        """Generate updated tech stack section."""
        tech_stack = "## 🛠️ Tech Stack\n\n"
        tech_stack += "<!-- Animated Tech Stack with Floating Effect -->\n"
        tech_stack += '<div align="center" style="margin: 30px 0;">\n'
        tech_stack += '  <div style="display: flex; flex-wrap: wrap; justify-content: center; gap: 15px;">\n'
        
        # Add discovered technologies
        for tech, count in list(analysis['technologies'].items())[:8]:
            if count >= 1:  # Show technologies used in projects
                tech_stack += f'    <img src="https://img.shields.io/badge/{tech}-000000?style=for-the-badge&logo={tech.lower()}&logoColor=white" style="animation: float 3s ease-in-out infinite;" />\n'
        
        tech_stack += '  </div>\n</div>\n\n'
        
        # Add technology categories
        tech_stack += "### Technology Categories\n\n"
        
        if analysis['languages']:
            tech_stack += "**Programming Languages**: " + ', '.join(list(analysis['languages'].keys())[:5]) + "\n\n"
        
        if analysis['frameworks']:
            tech_stack += "**Frameworks & Libraries**: " + ', '.join(list(analysis['frameworks'].keys())[:5]) + "\n\n"
        
        if analysis['databases']:
            tech_stack += "**Databases**: " + ', '.join(list(analysis['databases'].keys())[:3]) + "\n\n"
        
        if analysis['tools']:
            tech_stack += "**Tools & Platforms**: " + ', '.join(list(analysis['tools'].keys())[:5]) + "\n\n"
        
        return tech_stack
    
    def generate_recent_achievements(self, analysis: Dict) -> str:
        """Generate recent achievements section."""
        achievements = "## 🏆 Recent Achievements\n\n"
        
        if analysis['recent_projects']:
            achievements += f"- 🔥 **Active Development**: {len(analysis['recent_projects'])} projects in recent development\n"
        
        if analysis['complex_projects']:
            achievements += f"- 🚀 **Complex Projects**: {len(analysis['complex_projects'])} high-complexity projects completed\n"
        
        achievements += f"- 📊 **Total Projects**: {analysis['total_projects']} development projects discovered\n"
        achievements += f"- 🛠️ **Technologies**: Working with {len(analysis['technologies'])} different technologies\n"
        achievements += f"- 📈 **Skill Growth**: Expanded expertise across {len(analysis['languages'])} programming languages\n"
        achievements += f"- 🎯 **Project Diversity**: {len(analysis['project_types'])} different project types mastered\n"
        
        return achievements
    
    def generate_skills_matrix(self, analysis: Dict) -> str:
        """Generate skills matrix section."""
        skills = "## 📊 Skills Matrix\n\n"
        
        # Language proficiency
        skills += "### Programming Languages\n"
        for lang, count in list(analysis['languages'].items())[:6]:
            if count >= 3:
                level = "🟢 Proficient"
            elif count >= 2:
                level = "🟡 Intermediate"
            else:
                level = "🔴 Beginner"
            skills += f"- **{lang}**: {level} ({count} projects)\n"
        
        skills += "\n### Project Types\n"
        for ptype, count in analysis['project_types'].items():
            skills += f"- **{ptype.replace('_', ' ').title()}**: {count} projects\n"
        
        skills += "\n### Technology Stack\n"
        top_techs = list(analysis['technologies'].items())[:10]
        for tech, count in top_techs:
            skills += f"- **{tech}**: {count} projects\n"
        
        return skills
    
    def update_existing_profile(self, current_profile: str, new_sections: Dict) -> str:
        """Update existing profile with new sections."""
        # Find insertion points and add new sections
        updated_profile = current_profile
        
        # Add current focus after the main intro
        if 'current_focus' in new_sections:
            focus_insert = updated_profile.find('## 🚀 Featured Project')
            if focus_insert != -1:
                updated_profile = updated_profile[:focus_insert] + new_sections['current_focus'] + '\n\n' + updated_profile[focus_insert:]
        
        # Replace featured project section
        if 'featured_projects' in new_sections:
            project_start = updated_profile.find('## 🚀 Featured Project')
            if project_start != -1:
                # Find end of featured project section
                next_section = updated_profile.find('## ', project_start + 3)
                if next_section != -1:
                    updated_profile = updated_profile[:project_start] + new_sections['featured_projects'] + updated_profile[next_section:]
                else:
                    updated_profile = updated_profile[:project_start] + new_sections['featured_projects']
        
        # Replace tech stack section
        if 'tech_stack' in new_sections:
            tech_start = updated_profile.find('## 🛠️ Tech Stack')
            if tech_start != -1:
                next_section = updated_profile.find('## ', tech_start + 3)
                if next_section != -1:
                    updated_profile = updated_profile[:tech_start] + new_sections['tech_stack'] + updated_profile[next_section:]
                else:
                    updated_profile = updated_profile[:tech_start] + new_sections['tech_stack']
        
        # Replace achievements section
        if 'recent_achievements' in new_sections:
            achievements_start = updated_profile.find('## 🏆 Recent Achievements')
            if achievements_start != -1:
                next_section = updated_profile.find('## ', achievements_start + 3)
                if next_section != -1:
                    updated_profile = updated_profile[:achievements_start] + new_sections['recent_achievements'] + updated_profile[next_section:]
                else:
                    updated_profile = updated_profile[:achievements_start] + new_sections['recent_achievements']
        
        # Add skills matrix before GitHub stats
        if 'skills_matrix' in new_sections:
            stats_start = updated_profile.find('## 📊 GitHub Stats')
            if stats_start != -1:
                updated_profile = updated_profile[:stats_start] + new_sections['skills_matrix'] + '\n\n' + updated_profile[stats_start:]
        
        return updated_profile

def main():
    """Main execution function."""
    try:
        # Initialize analyzer
        analyzer = SimpleProjectAnalyzer()
        projects = analyzer.projects
        
        # Generate updated profile
        generator = SimpleProfileGenerator()
        
        # Read current profile
        with open('README.md', 'r', encoding='utf-8') as f:
            current_profile = f.read()
        
        # Generate updated profile
        updated_profile = generator.generate_profile(projects, current_profile)
        
        # Save updated profile
        with open('README_UPDATED.md', 'w', encoding='utf-8') as f:
            f.write(updated_profile)
        
        # Save project analysis
        with open('project_analysis.json', 'w', encoding='utf-8') as f:
            json.dump(projects, f, indent=2, default=str)
        
        logger.info("Profile update complete!")
        logger.info(f"Updated profile saved to: README_UPDATED.md")
        logger.info(f"Project analysis saved to: project_analysis.json")
        logger.info(f"Found {len(projects)} projects")
        
        # Print summary
        print("\n🎉 Profile Update Complete!")
        print(f"📊 Projects Analyzed: {len(projects)}")
        print(f"🛠️ Technologies Found: {len(set([tech for p in projects for tech in p.get('technologies', [])]))}")
        print(f"📝 Languages Used: {len(set([lang for p in projects for lang in p.get('languages', [])]))}")
        print(f"🚀 Frameworks: {len(set([fw for p in projects for fw in p.get('frameworks', [])]))}")
        
    except Exception as e:
        logger.error(f"Error in main execution: {e}")

if __name__ == "__main__":
    main()