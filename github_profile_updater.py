#!/usr/bin/env python3
"""
GitHub Profile Updater
Scans specified user path for development projects and generates comprehensive GitHub profile update
while ignoring Windows system files and folders.
"""

import os
import json
import re
import hashlib
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Set, Optional, Tuple
import mimetypes
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ProjectScanner:
    """Scans file system for development projects and analyzes their structure."""
    
    def __init__(self, config: Dict):
        self.config = config
        self.exclusion_rules = config.get('windows_exclusion_rules', {})
        self.discovery_patterns = config.get('development_discovery_patterns', {})
        self.analysis_framework = config.get('analysis_framework', {})
        
        # Initialize exclusion patterns
        self.system_folders = set(self.exclusion_rules.get('system_folders', []))
        self.system_files = set(self.exclusion_rules.get('system_files', []))
        self.temporary_patterns = self.exclusion_rules.get('temporary_patterns', [])
        self.windows_apps_folders = set(self.exclusion_rules.get('windows_apps_folders', []))
        
        # Project indicators
        self.project_indicators = self.discovery_patterns.get('project_indicators', {})
        self.code_extensions = set(self.discovery_patterns.get('code_file_extensions', []))
        self.ignore_folders = set(self.discovery_patterns.get('ignore_folders', []))
        
        # Compile regex patterns
        self.temp_patterns = [re.compile(pattern.replace('*', '.*')) for pattern in self.temporary_patterns]
        
    def should_exclude_path(self, path: Path) -> bool:
        """Check if a path should be excluded based on Windows exclusion rules."""
        path_str = str(path)
        
        # Check system folders
        for folder in self.system_folders:
            if folder.lower() in path_str.lower():
                return True
                
        # Check Windows apps folders
        for folder in self.windows_apps_folders:
            if folder.lower() in path_str.lower():
                return True
                
        # Check temporary patterns
        for pattern in self.temp_patterns:
            if pattern.search(path.name):
                return True
                
        # Check ignore folders
        for folder in self.ignore_folders:
            if folder.lower() in path_str.lower():
                return True
                
        return False
    
    def is_project_root(self, path: Path) -> bool:
        """Check if a directory is a project root based on indicators."""
        if not path.is_dir():
            return False
            
        # Check for root files
        for file_name in self.project_indicators.get('root_files', []):
            if (path / file_name).exists():
                return True
                
        # Check for config files
        for file_name in self.project_indicators.get('config_files', []):
            if (path / file_name).exists():
                return True
                
        # Check for documentation files
        for file_name in self.project_indicators.get('documentation_files', []):
            if (path / file_name).exists():
                return True
                
        return False
    
    def scan_projects(self, base_path: str, max_depth: int = 5) -> List[Dict]:
        """Recursively scan for development projects."""
        projects = []
        base_path = Path(base_path)
        
        if not base_path.exists():
            logger.error(f"Base path does not exist: {base_path}")
            return projects
            
        logger.info(f"Starting scan from: {base_path}")
        
        for root, dirs, files in os.walk(base_path, topdown=True):
            root_path = Path(root)
            current_depth = len(root_path.parts) - len(base_path.parts)
            
            # Limit depth
            if current_depth > max_depth:
                dirs.clear()
                continue
                
            # Filter out excluded directories
            dirs[:] = [d for d in dirs if not self.should_exclude_path(root_path / d)]
            
            # Check if current directory is a project root
            if self.is_project_root(root_path):
                project = self.analyze_project(root_path)
                if project:
                    projects.append(project)
                    logger.info(f"Found project: {project['name']} at {root_path}")
                    
        logger.info(f"Scan complete. Found {len(projects)} projects.")
        return projects
    
    def analyze_project(self, project_path: Path) -> Optional[Dict]:
        """Analyze a single project directory."""
        try:
            project = {
                'name': project_path.name,
                'path': str(project_path),
                'type': 'unknown',
                'technologies': set(),
                'languages': set(),
                'frameworks': set(),
                'databases': set(),
                'tools': set(),
                'file_count': 0,
                'code_lines': 0,
                'last_modified': None,
                'complexity_score': 0,
                'description': '',
                'readme_content': '',
                'dependencies': {},
                'structure': {}
            }
            
            # Analyze project structure
            self.analyze_project_structure(project_path, project)
            
            # Classify project type
            project['type'] = self.classify_project(project)
            
            # Extract technologies
            self.extract_technologies(project_path, project)
            
            # Calculate complexity score
            project['complexity_score'] = self.calculate_complexity(project)
            
            # Convert sets to lists for JSON serialization
            project['technologies'] = list(project['technologies'])
            project['languages'] = list(project['languages'])
            project['frameworks'] = list(project['frameworks'])
            project['databases'] = list(project['databases'])
            project['tools'] = list(project['tools'])
            
            return project
            
        except Exception as e:
            logger.error(f"Error analyzing project {project_path}: {e}")
            return None
    
    def analyze_project_structure(self, project_path: Path, project: Dict):
        """Analyze the structure of a project directory."""
        try:
            for item in project_path.rglob('*'):
                if item.is_file() and not self.should_exclude_path(item):
                    # Skip large files
                    if item.stat().st_size > 10 * 1024 * 1024:  # 10MB
                        continue
                        
                    project['file_count'] += 1
                    
                    # Track last modification
                    mtime = datetime.fromtimestamp(item.stat().st_mtime)
                    if not project['last_modified'] or mtime > project['last_modified']:
                        project['last_modified'] = mtime
                    
                    # Count code lines
                    if item.suffix.lower() in self.code_extensions:
                        try:
                            with open(item, 'r', encoding='utf-8', errors='ignore') as f:
                                lines = f.readlines()
                                project['code_lines'] += len(lines)
                        except:
                            pass
                    
                    # Check for README
                    if item.name.lower() in ['readme.md', 'readme.txt']:
                        try:
                            with open(item, 'r', encoding='utf-8', errors='ignore') as f:
                                project['readme_content'] = f.read()[:1000]  # First 1000 chars
                        except:
                            pass
                            
        except Exception as e:
            logger.error(f"Error analyzing project structure: {e}")
    
    def classify_project(self, project: Dict) -> str:
        """Classify project based on indicators and content."""
        indicators = self.analysis_framework.get('project_classification', {})
        
        # Web applications
        web_indicators = indicators.get('web_applications', {}).get('indicators', [])
        if any(indicator in project['technologies'] for indicator in web_indicators):
            return 'web_application'
            
        # Data science
        data_indicators = indicators.get('data_science', {}).get('indicators', [])
        if any(indicator in project['technologies'] for indicator in data_indicators):
            return 'data_science'
            
        # Blockchain
        blockchain_indicators = indicators.get('blockchain', {}).get('indicators', [])
        if any(indicator in project['technologies'] for indicator in blockchain_indicators):
            return 'blockchain'
            
        # Automation
        automation_indicators = indicators.get('automation', {}).get('indicators', [])
        if any(indicator in project['technologies'] for indicator in automation_indicators):
            return 'automation'
            
        # API development
        api_indicators = indicators.get('api_development', {}).get('indicators', [])
        if any(indicator in project['technologies'] for indicator in api_indicators):
            return 'api_development'
            
        # Mobile development
        mobile_indicators = indicators.get('mobile_development', {}).get('indicators', [])
        if any(indicator in project['technologies'] for indicator in mobile_indicators):
            return 'mobile_development'
            
        return 'general_development'
    
    def extract_technologies(self, project_path: Path, project: Dict):
        """Extract technologies from project files."""
        try:
            # Check package files
            package_files = {
                'package.json': self.parse_package_json,
                'composer.json': self.parse_composer_json,
                'requirements.txt': self.parse_requirements_txt,
                'Pipfile': self.parse_pipfile,
                'pom.xml': self.parse_pom_xml,
                'build.gradle': self.parse_gradle_file,
                'Cargo.toml': self.parse_cargo_toml,
                'go.mod': self.parse_go_mod
            }
            
            for file_name, parser_func in package_files.items():
                file_path = project_path / file_name
                if file_path.exists():
                    try:
                        dependencies = parser_func(file_path)
                        project['dependencies'][file_name] = dependencies
                        project['technologies'].update(dependencies)
                    except Exception as e:
                        logger.debug(f"Error parsing {file_name}: {e}")
            
            # Check for framework indicators in file content
            self.scan_file_content_for_technologies(project_path, project)
            
        except Exception as e:
            logger.error(f"Error extracting technologies: {e}")
    
    def parse_package_json(self, file_path: Path) -> Set[str]:
        """Parse package.json for dependencies."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                deps = set()
                deps.update(data.get('dependencies', {}).keys())
                deps.update(data.get('devDependencies', {}).keys())
                return deps
        except:
            return set()
    
    def parse_composer_json(self, file_path: Path) -> Set[str]:
        """Parse composer.json for dependencies."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                deps = set()
                deps.update(data.get('require', {}).keys())
                deps.update(data.get('require-dev', {}).keys())
                return deps
        except:
            return set()
    
    def parse_requirements_txt(self, file_path: Path) -> Set[str]:
        """Parse requirements.txt for Python packages."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                deps = set()
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        package = line.split('==')[0].split('>=')[0].split('<=')[0]
                        deps.add(package)
                return deps
        except:
            return set()
    
    def parse_pipfile(self, file_path: Path) -> Set[str]:
        """Parse Pipfile for Python packages."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                deps = set()
                # Simple regex-based parsing
                import re
                packages = re.findall(r'\[packages\]\s*\n(.*?)(?=\n\[|$)', content, re.DOTALL)
                for package in packages:
                    lines = package.strip().split('\n')
                    for line in lines:
                        if '=' in line:
                            pkg = line.split('=')[0].strip()
                            deps.add(pkg)
                return deps
        except:
            return set()
    
    def parse_pom_xml(self, file_path: Path) -> Set[str]:
        """Parse pom.xml for Java dependencies."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                deps = set()
                # Simple regex-based parsing
                import re
                dependencies = re.findall(r'<artifactId>(.*?)</artifactId>', content)
                deps.update(dependencies)
                return deps
        except:
            return set()
    
    def parse_gradle_file(self, file_path: Path) -> Set[str]:
        """Parse build.gradle for dependencies."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                deps = set()
                # Simple regex-based parsing
                import re
                dependencies = re.findall(r'implementation\s+[\'"]([^\'"]+)[\'"]', content)
                deps.update(dependencies)
                return deps
        except:
            return set()
    
    def parse_cargo_toml(self, file_path: Path) -> Set[str]:
        """Parse Cargo.toml for Rust dependencies."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                deps = set()
                # Simple regex-based parsing
                import re
                dependencies = re.findall(r'\[dependencies\]\s*\n(.*?)(?=\n\[|$)', content, re.DOTALL)
                for dep in dependencies:
                    lines = dep.strip().split('\n')
                    for line in lines:
                        if '=' in line:
                            pkg = line.split('=')[0].strip()
                            deps.add(pkg)
                return deps
        except:
            return set()
    
    def parse_go_mod(self, file_path: Path) -> Set[str]:
        """Parse go.mod for Go dependencies."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                deps = set()
                for line in f:
                    line = line.strip()
                    if line.startswith('require'):
                        parts = line.split()
                        if len(parts) >= 2:
                            deps.add(parts[1])
                return deps
        except:
            return set()
    
    def scan_file_content_for_technologies(self, project_path: Path, project: Dict):
        """Scan file content for technology indicators."""
        try:
            # Common technology patterns
            tech_patterns = {
                'python': [r'import\s+(\w+)', r'from\s+(\w+)'],
                'javascript': [r'import\s+[\'"]([^\'"]+)[\'"]', r'require\s*\(\s*[\'"]([^\'"]+)[\'"]'],
                'php': [r'use\s+([^;]+)', r'include\s+[\'"]([^\'"]+)[\'"]'],
                'database': [r'mysql', r'postgresql', r'mongodb', r'sqlite', r'redis'],
                'cloud': [r'aws', r'azure', r'gcp', r'heroku', r'vercel', r'netlify'],
                'api': [r'rest', r'graphql', r'soap', r'grpc']
            }
            
            for file_path in project_path.rglob('*'):
                if file_path.is_file() and file_path.suffix.lower() in self.code_extensions:
                    try:
                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                            content = f.read()
                            
                            for tech_type, patterns in tech_patterns.items():
                                for pattern in patterns:
                                    matches = re.findall(pattern, content, re.IGNORECASE)
                                    for match in matches:
                                        if tech_type == 'python':
                                            project['languages'].add('python')
                                            project['technologies'].add(match)
                                        elif tech_type == 'javascript':
                                            project['languages'].add('javascript')
                                            project['technologies'].add(match)
                                        elif tech_type == 'php':
                                            project['languages'].add('php')
                                            project['technologies'].add(match)
                                        elif tech_type == 'database':
                                            project['databases'].add(match)
                                        elif tech_type == 'cloud':
                                            project['tools'].add(match)
                                        elif tech_type == 'api':
                                            project['tools'].add(match)
                                            
                    except:
                        continue
                        
        except Exception as e:
            logger.error(f"Error scanning file content: {e}")
    
    def calculate_complexity(self, project: Dict) -> int:
        """Calculate project complexity score."""
        score = 0
        
        # File count contribution
        score += min(project['file_count'] // 10, 20)
        
        # Code lines contribution
        score += min(project['code_lines'] // 100, 30)
        
        # Technology diversity
        score += min(len(project['technologies']) * 2, 20)
        
        # Project type complexity
        type_scores = {
            'web_application': 15,
            'data_science': 12,
            'blockchain': 20,
            'automation': 8,
            'api_development': 10,
            'mobile_development': 15,
            'general_development': 5
        }
        score += type_scores.get(project['type'], 5)
        
        return min(score, 100)  # Cap at 100

class ProfileGenerator:
    """Generates updated GitHub profile based on discovered projects."""
    
    def __init__(self, config: Dict):
        self.config = config
        self.profile_template = config.get('profile_generation', {}).get('current_profile_template', {})
        
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
            'recent_projects': [],
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
            
            # Recent projects (last 6 months)
            if project.get('last_modified'):
                six_months_ago = datetime.now() - timedelta(days=180)
                if project['last_modified'] > six_months_ago:
                    analysis['recent_projects'].append(project)
            
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
        sorted_projects = sorted(projects, key=lambda x: (x.get('complexity_score', 0), x.get('last_modified', datetime.min)), reverse=True)
        
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
            for i, project in enumerate(sorted_projects[:3]):
                featured += f"#### {project['name']}\n"
                featured += f"**Type**: {project['type'].replace('_', ' ').title()}\n"
                featured += f"**Complexity**: {project.get('complexity_score', 0)}/100\n"
                featured += f"**Technologies**: {', '.join(project.get('technologies', [])[:5])}\n"
                if project.get('readme_content'):
                    featured += f"**Description**: {project['readme_content'][:200]}...\n"
                featured += f"**Last Modified**: {project.get('last_modified', 'Unknown')}\n\n"
        
        return featured
    
    def generate_tech_stack(self, analysis: Dict) -> str:
        """Generate updated tech stack section."""
        tech_stack = "## 🛠️ Tech Stack\n\n"
        tech_stack += "<!-- Animated Tech Stack with Floating Effect -->\n"
        tech_stack += '<div align="center" style="margin: 30px 0;">\n'
        tech_stack += '  <div style="display: flex; flex-wrap: wrap; justify-content: center; gap: 15px;">\n'
        
        # Add discovered technologies
        for tech, count in list(analysis['technologies'].items())[:8]:
            if count >= 2:  # Only show technologies used in multiple projects
                tech_stack += f'    <img src="https://img.shields.io/badge/{tech}-000000?style=for-the-badge&logo={tech.lower()}&logoColor=white" style="animation: float 3s ease-in-out infinite;" />\n'
        
        tech_stack += '  </div>\n</div>\n\n'
        
        # Add technology categories
        tech_stack += "### Technology Categories\n\n"
        
        if analysis['languages']:
            tech_stack += "**Programming Languages**: " + ', '.join(list(analysis['languages'].keys())[:5]) + "\n\n"
        
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
            if count >= 5:
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
        
        # Initialize scanner
        scanner = ProjectScanner(config)
        
        # Scan for projects
        scan_config = config.get('scan_configuration', {})
        projects = scanner.scan_projects(
            scan_config.get('base_path', '/workspace'),
            scan_config.get('max_depth', 5)
        )
        
        # Generate updated profile
        generator = ProfileGenerator(config)
        
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