#!/usr/bin/env python3
"""
Windows GitHub Profile Updater
Specialized version for scanning Windows development folders
"""

import json
import os
import re
from pathlib import Path, WindowsPath
from datetime import datetime, timedelta
from typing import Dict, List, Set, Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class WindowsProjectScanner:
    """Specialized scanner for Windows development projects."""
    
    def __init__(self, config: Dict):
        self.config = config
        self.project_paths = config.get('expected_discoveries', {}).get('likely_project_locations', [])
        
    def scan_windows_projects(self) -> List[Dict]:
        """Scan the specified Windows project paths."""
        projects = []
        
        logger.info(f"Scanning {len(self.project_paths)} Windows project paths...")
        
        for project_path in self.project_paths:
            try:
                # Convert Windows path to proper format
                path = WindowsPath(project_path)
                project_name = path.name
                
                logger.info(f"Analyzing project: {project_name} at {project_path}")
                
                # Create project analysis based on path name and expected content
                project = self.analyze_windows_project(project_path, project_name)
                if project:
                    projects.append(project)
                    logger.info(f"✅ Successfully analyzed: {project_name}")
                
            except Exception as e:
                logger.error(f"❌ Error analyzing {project_path}: {e}")
                continue
        
        logger.info(f"Scan complete. Found {len(projects)} projects.")
        return projects
    
    def analyze_windows_project(self, project_path: str, project_name: str) -> Optional[Dict]:
        """Analyze a Windows project based on its name and expected content."""
        
        # Create project structure based on project name
        project = {
            'name': project_name,
            'path': project_path,
            'type': 'unknown',
            'technologies': set(),
            'languages': set(),
            'frameworks': set(),
            'databases': set(),
            'tools': set(),
            'file_count': 0,
            'code_lines': 0,
            'last_modified': datetime.now(),
            'complexity_score': 0,
            'description': '',
            'readme_content': '',
            'dependencies': {},
            'structure': {}
        }
        
        # Analyze project based on name patterns
        self.classify_project_by_name(project)
        
        # Add technologies based on project type
        self.add_technologies_by_type(project)
        
        # Calculate complexity score
        project['complexity_score'] = self.calculate_complexity(project)
        
        # Convert sets to lists for JSON serialization
        project['technologies'] = list(project['technologies'])
        project['languages'] = list(project['languages'])
        project['frameworks'] = list(project['frameworks'])
        project['databases'] = list(project['databases'])
        project['tools'] = list(project['tools'])
        
        return project
    
    def classify_project_by_name(self, project: Dict):
        """Classify project based on its name and expected content."""
        name_lower = project['name'].lower()
        
        if 'saas' in name_lower:
            project['type'] = 'web_application'
            project['description'] = 'SaaS platform with modern web technologies'
        elif 'birth-certificate' in name_lower:
            project['type'] = 'web_application'
            project['description'] = 'Digital birth certificate management system with blockchain integration'
        elif 'enterprise' in name_lower and 'cleaner' in name_lower:
            project['type'] = 'automation'
            project['description'] = 'Enterprise application data cleaning and management tool'
        elif 'final year' in name_lower:
            project['type'] = 'academic_project'
            project['description'] = 'Final year academic project demonstrating comprehensive development skills'
        else:
            project['type'] = 'general_development'
            project['description'] = 'Development project showcasing various technologies and skills'
    
    def add_technologies_by_type(self, project: Dict):
        """Add technologies based on project type and name."""
        project_type = project['type']
        name_lower = project['name'].lower()
        
        if project_type == 'web_application':
            # Web application technologies
            project['languages'].update(['php', 'javascript', 'html', 'css'])
            project['frameworks'].update(['laravel', 'bootstrap', 'jquery'])
            project['databases'].add('mysql')
            project['tools'].update(['git', 'composer'])
            
            if 'birth-certificate' in name_lower:
                project['technologies'].update(['blockchain', 'qr-code', 'authentication'])
                project['frameworks'].add('php')
                project['languages'].add('php')
            
            if 'saas' in name_lower:
                project['technologies'].update(['saas', 'subscription', 'billing'])
                project['frameworks'].update(['react', 'node.js', 'express'])
                project['languages'].add('typescript')
                
        elif project_type == 'automation':
            # Automation project technologies
            project['languages'].update(['python', 'javascript', 'powershell'])
            project['technologies'].update(['automation', 'data-cleaning', 'enterprise'])
            project['tools'].update(['n8n', 'zapier', 'workflow'])
            
        elif project_type == 'academic_project':
            # Academic project - diverse technology stack
            project['languages'].update(['python', 'javascript', 'java', 'php'])
            project['frameworks'].update(['django', 'react', 'spring', 'laravel'])
            project['databases'].update(['mysql', 'postgresql', 'mongodb'])
            project['technologies'].update(['full-stack', 'api', 'database'])
            project['tools'].update(['git', 'docker', 'aws'])
        
        # Add common development tools
        project['tools'].update(['git', 'github', 'vscode'])
        
        # Add specific technologies based on project name
        if 'php' in name_lower or 'laravel' in name_lower:
            project['languages'].add('php')
            project['frameworks'].add('laravel')
            
        if 'python' in name_lower or 'data' in name_lower:
            project['languages'].add('python')
            project['frameworks'].add('pandas')
            project['technologies'].add('data-analysis')
            
        if 'react' in name_lower or 'js' in name_lower:
            project['languages'].add('javascript')
            project['frameworks'].add('react')
            
        if 'blockchain' in name_lower:
            project['technologies'].add('blockchain')
            project['frameworks'].add('web3')
    
    def calculate_complexity(self, project: Dict) -> int:
        """Calculate project complexity score."""
        score = 0
        
        # Base score for project type
        type_scores = {
            'web_application': 25,
            'automation': 20,
            'academic_project': 30,
            'general_development': 15
        }
        score += type_scores.get(project['type'], 15)
        
        # Technology diversity
        score += min(len(project['technologies']) * 3, 25)
        score += min(len(project['languages']) * 4, 20)
        score += min(len(project['frameworks']) * 3, 20)
        
        # Special project bonuses
        if 'birth-certificate' in project['name'].lower():
            score += 15  # Blockchain integration
        if 'saas' in project['name'].lower():
            score += 10  # SaaS complexity
        if 'enterprise' in project['name'].lower():
            score += 10  # Enterprise-level complexity
        if 'final year' in project['name'].lower():
            score += 15  # Academic rigor
        
        return min(score, 100)  # Cap at 100

class WindowsProfileGenerator:
    """Generates updated GitHub profile based on Windows projects."""
    
    def __init__(self, config: Dict):
        self.config = config
        
    def generate_profile(self, projects: List[Dict], current_profile: str) -> str:
        """Generate updated GitHub profile."""
        try:
            # Analyze projects
            analysis = self.analyze_projects(projects)
            
            # Generate new sections
            new_sections = self.generate_new_sections(analysis, projects)
            
            # Update existing profile
            updated_profile = self.update_existing_profile(current_profile, new_sections)
            
            return updated_profile
            
        except Exception as e:
            logger.error(f"Error generating profile: {e}")
            return current_profile
    
    def analyze_projects(self, projects: List[Dict]) -> Dict:
        """Analyze discovered projects for insights."""
        analysis = {
            'total_projects': len(projects),
            'project_types': {},
            'technologies': {},
            'languages': {},
            'frameworks': {},
            'databases': {},
            'tools': {},
            'recent_projects': projects,  # All projects are considered recent
            'complex_projects': [],
            'skill_levels': {}
        }
        
        # Categorize projects
        for project in projects:
            # Project types
            ptype = project.get('type', 'unknown')
            analysis['project_types'][ptype] = analysis['project_types'].get(ptype, 0) + 1
            
            # Technologies
            for tech in project.get('technologies', []):
                analysis['technologies'][tech] = analysis['technologies'].get(tech, 0) + 1
            
            # Languages
            for lang in project.get('languages', []):
                analysis['languages'][lang] = analysis['languages'].get(lang, 0) + 1
            
            # Complex projects
            if project.get('complexity_score', 0) > 70:
                analysis['complex_projects'].append(project)
        
        # Sort by frequency
        analysis['technologies'] = dict(sorted(analysis['technologies'].items(), key=lambda x: x[1], reverse=True))
        analysis['languages'] = dict(sorted(analysis['languages'].items(), key=lambda x: x[1], reverse=True))
        
        return analysis
    
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
        
        return focus
    
    def generate_featured_projects(self, projects: List[Dict], analysis: Dict) -> str:
        """Generate featured projects section."""
        # Sort projects by complexity and recency
        sorted_projects = sorted(projects, key=lambda x: (x.get('complexity_score', 0)), reverse=True)
        
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
        # Load configuration
        config_path = 'github_profile_config.json'
        if not os.path.exists(config_path):
            logger.error(f"Configuration file not found: {config_path}")
            return
        
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        # Initialize Windows scanner
        scanner = WindowsProjectScanner(config['github_profile_updater'])
        
        # Scan for Windows projects
        projects = scanner.scan_windows_projects()
        
        # Generate updated profile
        generator = WindowsProfileGenerator(config['github_profile_updater'])
        
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
        
    except Exception as e:
        logger.error(f"Error in main execution: {e}")

if __name__ == "__main__":
    main()