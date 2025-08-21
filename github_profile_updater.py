#!/usr/bin/env python3
"""
GitHub Profile Updater
A comprehensive system that automatically scans your development workspace for projects
and generates an updated GitHub profile while preserving your existing aesthetic and animations.
"""

import os
import json
import logging
import re
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Set, Tuple, Optional
import mimetypes

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('github_profile_updater.log'),
        logging.StreamHandler()
    ]
)

class ProjectScanner:
    """Recursively scans file system for development projects"""
    
    def __init__(self, config: Dict):
        self.config = config
        self.scan_config = config.get('scan_configuration', {})
        self.exclusions = config.get('exclusions', {})
        self.project_indicators = config.get('project_indicators', {})
        self.discovered_projects = []
        self.technologies = set()
        
    def is_excluded_path(self, path: str) -> bool:
        """Check if a path should be excluded from scanning"""
        path_lower = path.lower()
        
        # Windows system exclusions
        windows_exclusions = [
            'appdata', 'desktop', 'downloads', 'documents', 'pictures',
            'music', 'videos', 'onedrive', 'program files', 'programdata',
            'windows', 'system32', 'syswow64', 'temp', 'tmp', 'recycler',
            'recovery', 'boot', 'efi', 'msocache', 'perflogs', 'prefetch'
        ]
        
        for exclusion in windows_exclusions:
            if exclusion in path_lower:
                return True
                
        # Custom exclusions
        for pattern in self.exclusions.get('patterns', []):
            if re.search(pattern, path, re.IGNORECASE):
                return True
                
        return False
    
    def is_project_root(self, directory: Path) -> bool:
        """Determine if a directory is a project root"""
        indicators = self.project_indicators.get('root_files', [])
        config_files = self.project_indicators.get('config_files', [])
        doc_files = self.project_indicators.get('documentation_files', [])
        
        # Check for root files
        for indicator in indicators:
            if (directory / indicator).exists():
                return True
                
        # Check for config files
        for config_file in config_files:
            if (directory / config_file).exists():
                return True
                
        # Check for documentation
        for doc_file in doc_files:
            if (directory / doc_file).exists():
                return True
                
        # Check for code files
        code_extensions = ['.py', '.js', '.php', '.java', '.html', '.css', '.ts', '.jsx', '.tsx']
        for ext in code_extensions:
            if list(directory.glob(f'*{ext}')):
                return True
                
        return False
    
    def extract_technologies(self, file_path: Path) -> Set[str]:
        """Extract technologies from a file"""
        techs = set()
        
        try:
            # Skip large files
            if file_path.stat().st_size > 10 * 1024 * 1024:  # 10MB
                return techs
                
            # Skip binary files
            mime_type, _ = mimetypes.guess_type(str(file_path))
            if mime_type and not mime_type.startswith('text/'):
                return techs
                
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                
            # Package manager files
            if file_path.name == 'package.json':
                try:
                    data = json.loads(content)
                    if 'dependencies' in data:
                        techs.update(data['dependencies'].keys())
                    if 'devDependencies' in data:
                        techs.update(data['devDependencies'].keys())
                except:
                    pass
                    
            elif file_path.name == 'requirements.txt':
                for line in content.split('\n'):
                    line = line.strip()
                    if line and not line.startswith('#'):
                        techs.add(line.split('==')[0].split('>=')[0].split('<=')[0])
                        
            elif file_path.name == 'composer.json':
                try:
                    data = json.loads(content)
                    if 'require' in data:
                        techs.update(data['require'].keys())
                except:
                    pass
                    
            elif file_path.name == 'pom.xml':
                # Basic XML parsing for Maven dependencies
                deps = re.findall(r'<artifactId>([^<]+)</artifactId>', content)
                techs.update(deps)
                
            elif file_path.name == 'Cargo.toml':
                # Basic TOML parsing for Rust dependencies
                deps = re.findall(r'^(\w+)\s*=', content, re.MULTILINE)
                techs.update(deps)
                
            elif file_path.name == 'go.mod':
                # Go module dependencies
                deps = re.findall(r'^(\w+)\s+v[0-9.]+', content, re.MULTILINE)
                techs.update(deps)
                
            # Import statements
            import_patterns = [
                r'^import\s+["\']([^"\']+)["\']',  # Python/JS imports
                r'^from\s+([^\s]+)',  # Python from imports
                r'^require\s+["\']([^"\']+)["\']',  # Node.js require
                r'^use\s+([^;]+);',  # PHP use statements
                r'^import\s+([^;]+);',  # Java imports
            ]
            
            for pattern in import_patterns:
                matches = re.findall(pattern, content, re.MULTILINE)
                # Clean up matches to avoid parsing artifacts
                for match in matches:
                    if match and len(match) < 50:  # Reasonable length for tech names
                        clean_match = match.split('\n')[0].split(' ')[0].strip()
                        if clean_match and not clean_match.startswith('import'):
                            techs.add(clean_match)
                
            # Framework detection
            framework_patterns = {
                'React': [r'react', r'jsx', r'tsx'],
                'Vue': [r'vue', r'vite'],
                'Angular': [r'angular', r'ng-'],
                'Django': [r'django', r'djangorestframework'],
                'Flask': [r'flask'],
                'Laravel': [r'laravel'],
                'Symfony': [r'symfony'],
                'Spring': [r'spring', r'@spring'],
                'Express': [r'express', r'@express'],
                'Next.js': [r'next', r'@next'],
                'Nuxt': [r'nuxt', r'@nuxt'],
                'Tailwind': [r'tailwind'],
                'Bootstrap': [r'bootstrap'],
                'TypeScript': [r'typescript', r'tsconfig'],
                'Webpack': [r'webpack'],
                'Vite': [r'vite'],
                'Docker': [r'docker', r'dockerfile'],
                'Kubernetes': [r'kubernetes', r'k8s'],
            }
            
            for framework, patterns in framework_patterns.items():
                for pattern in patterns:
                    if re.search(pattern, content, re.IGNORECASE):
                        techs.add(framework)
                        
        except Exception as e:
            logging.debug(f"Error extracting technologies from {file_path}: {e}")
            
        return techs
    
    def analyze_project(self, project_path: Path) -> Dict:
        """Analyze a single project"""
        try:
            project_info = {
                'name': project_path.name,
                'path': str(project_path),
                'type': 'Unknown',
                'technologies': set(),
                'file_count': 0,
                'code_lines': 0,
                'complexity_score': 0,
                'last_modified': None,
                'has_readme': False,
                'description': '',
                'readme_content': ''
            }
            
            # Count files and extract technologies
            for file_path in project_path.rglob('*'):
                if file_path.is_file():
                    project_info['file_count'] += 1
                    
                    # Update last modified
                    mtime = file_path.stat().st_mtime
                    if not project_info['last_modified'] or mtime > project_info['last_modified']:
                        project_info['last_modified'] = mtime
                    
                    # Extract technologies
                    techs = self.extract_technologies(file_path)
                    project_info['technologies'].update(techs)
                    
                    # Count code lines
                    if file_path.suffix in ['.py', '.js', '.php', '.java', '.html', '.css', '.ts', '.jsx', '.tsx']:
                        try:
                            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                                project_info['code_lines'] += len(f.readlines())
                        except:
                            pass
                    
                    # Check for README
                    if file_path.name.lower() in ['readme.md', 'readme.txt', 'readme']:
                        project_info['has_readme'] = True
                        try:
                            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                                project_info['readme_content'] = f.read()
                                # Extract description from first paragraph
                                lines = project_info['readme_content'].split('\n')
                                for line in lines:
                                    if line.strip() and not line.startswith('#'):
                                        project_info['description'] = line.strip()
                                        break
                        except:
                            pass
            
            # Calculate complexity score
            project_info['complexity_score'] = (
                project_info['file_count'] * 0.3 +
                project_info['code_lines'] * 0.01 +
                len(project_info['technologies']) * 2
            )
            
            # Determine project type
            project_info['type'] = self.classify_project_type(project_info)
            
            # Convert sets to lists for JSON serialization
            project_info['technologies'] = list(project_info['technologies'])
            
            return project_info
            
        except Exception as e:
            logging.error(f"Error analyzing project {project_path}: {e}")
            return None
    
    def classify_project_type(self, project_info: Dict) -> str:
        """Classify project type based on technologies and structure"""
        techs = set(tech.lower() for tech in project_info['technologies'])
        
        if any(tech in techs for tech in ['react', 'vue', 'angular', 'next.js', 'nuxt']):
            return 'Frontend Web'
        elif any(tech in techs for tech in ['django', 'flask', 'laravel', 'symfony', 'express']):
            return 'Backend Web'
        elif any(tech in techs for tech in ['html', 'css', 'bootstrap', 'tailwind']):
            return 'Static Web'
        elif any(tech in techs for tech in ['pandas', 'numpy', 'scikit-learn', 'tensorflow', 'pytorch']):
            return 'Data Science'
        elif any(tech in techs for tech in ['docker', 'kubernetes', 'terraform']):
            return 'DevOps'
        elif any(tech in techs for tech in ['ethereum', 'solidity', 'web3']):
            return 'Blockchain'
        elif any(tech in techs for tech in ['android', 'ios', 'react-native', 'flutter']):
            return 'Mobile'
        elif any(tech in techs for tech in ['unity', 'unreal', 'godot']):
            return 'Game Development'
        else:
            return 'General Development'
    
    def scan_workspace(self) -> List[Dict]:
        """Scan the entire workspace for projects"""
        base_path = Path(self.scan_config.get('base_path', '.'))
        max_depth = self.scan_config.get('max_depth', 5)
        
        logging.info(f"Starting workspace scan at: {base_path}")
        logging.info(f"Maximum scan depth: {max_depth}")
        
        # Use a set to track processed paths and avoid duplicates
        processed_paths = set()
        
        for depth in range(max_depth + 1):
            logging.info(f"Scanning depth {depth}...")
            
            for item in base_path.iterdir():
                if item.is_dir() and not self.is_excluded_path(str(item)):
                    # Check if we've already processed this path
                    if str(item) in processed_paths:
                        continue
                        
                    if self.is_project_root(item):
                        logging.info(f"Found project: {item.name}")
                        project_info = self.analyze_project(item)
                        if project_info:
                            # Check for duplicates by name and path
                            is_duplicate = any(
                                p['name'] == project_info['name'] and 
                                p['path'] == project_info['path'] 
                                for p in self.discovered_projects
                            )
                            
                            if not is_duplicate:
                                self.discovered_projects.append(project_info)
                                self.technologies.update(project_info['technologies'])
                                processed_paths.add(str(item))
                    
                    # Recursively scan subdirectories
                    if depth < max_depth:
                        self._scan_directory(item, depth + 1, max_depth, processed_paths)
        
        logging.info(f"Scan complete. Found {len(self.discovered_projects)} projects")
        logging.info(f"Discovered {len(self.technologies)} unique technologies")
        
        return self.discovered_projects
    
    def _scan_directory(self, directory: Path, current_depth: int, max_depth: int, processed_paths: set):
        """Recursively scan a directory"""
        try:
            for item in directory.iterdir():
                if item.is_dir() and not self.is_excluded_path(str(item)):
                    # Check if we've already processed this path
                    if str(item) in processed_paths:
                        continue
                        
                    if self.is_project_root(item):
                        logging.info(f"Found project at depth {current_depth}: {item.name}")
                        project_info = self.analyze_project(item)
                        if project_info:
                            # Check for duplicates by name and path
                            is_duplicate = any(
                                p['name'] == project_info['name'] and 
                                p['path'] == project_info['path'] 
                                for p in self.discovered_projects
                            )
                            
                            if not is_duplicate:
                                self.discovered_projects.append(project_info)
                                self.technologies.update(project_info['technologies'])
                                processed_paths.add(str(item))
                    
                    if current_depth < max_depth:
                        self._scan_directory(item, current_depth + 1, max_depth, processed_paths)
        except PermissionError:
            logging.debug(f"Permission denied accessing {directory}")
        except Exception as e:
            logging.debug(f"Error scanning {directory}: {e}")

class ProfileGenerator:
    """Generates updated GitHub profile content"""
    
    def __init__(self, config: Dict, projects: List[Dict], technologies: Set[str]):
        self.config = config
        self.projects = projects
        self.technologies = technologies
        self.profile_template = config.get('profile_generation', {}).get('current_profile_template', {})
        
    def generate_updated_profile(self) -> str:
        """Generate the complete updated profile"""
        # Read current profile
        current_profile = self._read_current_profile()
        
        # Generate new sections
        current_focus = self._generate_current_focus()
        featured_projects = self._generate_featured_projects()
        tech_stack = self._generate_tech_stack()
        recent_achievements = self._generate_recent_achievements()
        skills_matrix = self._generate_skills_matrix()
        
        # Update the profile
        updated_profile = self._update_profile_sections(
            current_profile,
            current_focus,
            featured_projects,
            tech_stack,
            recent_achievements,
            skills_matrix
        )
        
        return updated_profile
    
    def _read_current_profile(self) -> str:
        """Read the current README.md file"""
        try:
            with open('README.md', 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            logging.warning("README.md not found, using template")
            return self._get_default_template()
    
    def _get_default_template(self) -> str:
        """Get default profile template"""
        return """# 🚀 GitHub Profile

## 🌱 Current Focus
*Your current focus will be generated here*

## 🚀 Featured Projects
*Your projects will be discovered and listed here*

## 🛠️ Tech Stack
*Your technology stack will be analyzed here*

## 📊 Skills Matrix
*Your skills will be assessed here*

## 🏆 Recent Achievements
*Your achievements will be listed here*
"""
    
    def _generate_current_focus(self) -> str:
        """Generate current focus section"""
        if not self.projects:
            return "🌱 **Currently exploring new technologies and building innovative solutions**"
        
        # Get recent technologies
        recent_techs = []
        for project in sorted(self.projects, key=lambda x: x.get('last_modified', 0), reverse=True)[:5]:
            recent_techs.extend(project.get('technologies', [])[:3])
        
        unique_techs = list(set(recent_techs))[:8]
        
        focus_text = "🌱 **Currently focused on:**\n"
        for tech in unique_techs:
            focus_text += f"- **{tech}** - Building and exploring new capabilities\n"
        
        return focus_text
    
    def _generate_featured_projects(self) -> str:
        """Generate featured projects section"""
        if not self.projects:
            return "🚀 **Projects coming soon!**"
        
        # Sort projects by complexity and recency
        sorted_projects = sorted(
            self.projects,
            key=lambda x: (x.get('complexity_score', 0), x.get('last_modified', 0)),
            reverse=True
        )
        
        featured_text = "## 🚀 Featured Projects\n\n"
        
        for i, project in enumerate(sorted_projects[:6]):
            featured_text += f"### {i+1}. {project['name']}\n"
            featured_text += f"**Type**: {project['type']}\n"
            featured_text += f"**Complexity**: {'🟢 High' if project['complexity_score'] > 50 else '🟡 Medium' if project['complexity_score'] > 20 else '🔴 Basic'}\n"
            
            if project['description']:
                featured_text += f"**Description**: {project['description']}\n"
            
            if project['technologies']:
                tech_badges = []
                for tech in project['technologies'][:5]:
                    tech_badges.append(f"`{tech}`")
                featured_text += f"**Tech Stack**: {' '.join(tech_badges)}\n"
            
            featured_text += f"**Files**: {project['file_count']} | **Code Lines**: {project['code_lines']:,}\n\n"
        
        return featured_text
    
    def _generate_tech_stack(self) -> str:
        """Generate enhanced tech stack section"""
        if not self.technologies:
            return "🛠️ **Tech stack analysis in progress...**"
        
        # Categorize technologies
        categories = {
            'Programming Languages': ['python', 'javascript', 'php', 'java', 'typescript', 'go', 'rust'],
            'Frontend': ['react', 'vue', 'angular', 'html', 'css', 'bootstrap', 'tailwind'],
            'Backend': ['django', 'flask', 'laravel', 'symfony', 'express', 'spring'],
            'Databases': ['mysql', 'postgresql', 'mongodb', 'redis', 'sqlite'],
            'DevOps': ['docker', 'kubernetes', 'terraform', 'jenkins', 'github-actions'],
            'Data Science': ['pandas', 'numpy', 'scikit-learn', 'tensorflow', 'pytorch'],
            'Blockchain': ['ethereum', 'solidity', 'web3', 'hyperledger'],
            'Tools': ['git', 'vscode', 'postman', 'figma', 'adobe']
        }
        
        tech_stack_text = "## 🛠️ Enhanced Tech Stack\n\n"
        
        for category, tech_list in categories.items():
            matching_techs = [tech for tech in self.technologies if tech.lower() in [t.lower() for t in tech_list]]
            if matching_techs:
                tech_stack_text += f"### {category}\n"
                for tech in matching_techs[:6]:
                    tech_stack_text += f"![{tech}](https://img.shields.io/badge/{tech}-000000?style=for-the-badge&logo={tech.lower()}&logoColor=white) "
                tech_stack_text += "\n\n"
        
        return tech_stack_text
    
    def _generate_recent_achievements(self) -> str:
        """Generate recent achievements section"""
        if not self.projects:
            return "🏆 **Building achievements...**"
        
        achievements = []
        
        # Count projects by type
        project_types = {}
        for project in self.projects:
            ptype = project['type']
            project_types[ptype] = project_types.get(ptype, 0) + 1
        
        for ptype, count in project_types.items():
            achievements.append(f"✅ **{count} {ptype} projects** completed")
        
        # Technology milestones
        tech_count = len(self.technologies)
        if tech_count >= 20:
            achievements.append("🚀 **20+ technologies** mastered")
        elif tech_count >= 10:
            achievements.append("🎯 **10+ technologies** proficient")
        elif tech_count >= 5:
            achievements.append("📚 **5+ technologies** learned")
        
        # Code metrics
        total_lines = sum(p.get('code_lines', 0) for p in self.projects)
        if total_lines >= 10000:
            achievements.append("💻 **10,000+ lines of code** written")
        elif total_lines >= 5000:
            achievements.append("💻 **5,000+ lines of code** written")
        
        achievements_text = "## 🏆 Recent Achievements\n\n"
        for achievement in achievements:
            achievements_text += f"- {achievement}\n"
        
        return achievements_text
    
    def _generate_skills_matrix(self) -> str:
        """Generate skills matrix section"""
        if not self.projects:
            return "📊 **Skills assessment in progress...**"
        
        # Calculate skill levels
        skill_levels = {}
        for project in self.projects:
            for tech in project.get('technologies', []):
                if tech not in skill_levels:
                    skill_levels[tech] = {'projects': 0, 'files': 0, 'lines': 0}
                
                skill_levels[tech]['projects'] += 1
                skill_levels[tech]['files'] += project.get('file_count', 0)
                skill_levels[tech]['lines'] += project.get('code_lines', 0)
        
        # Determine proficiency levels
        proficiency_levels = {}
        for tech, metrics in skill_levels.items():
            if metrics['projects'] >= 5 or metrics['files'] >= 100:
                proficiency_levels[tech] = '🟢 Proficient'
            elif metrics['projects'] >= 2 or metrics['files'] >= 20:
                proficiency_levels[tech] = '🟡 Intermediate'
            else:
                proficiency_levels[tech] = '🔴 Beginner'
        
        # Sort by proficiency
        sorted_skills = sorted(
            proficiency_levels.items(),
            key=lambda x: ('🟢' in x[1], '🟡' in x[1], x[0])
        )
        
        skills_text = "## 📊 Skills Matrix\n\n"
        skills_text += "Skills are assessed based on project evidence and usage frequency.\n\n"
        
        for tech, level in sorted_skills[:15]:  # Top 15 skills
            skills_text += f"- {level} **{tech}**\n"
        
        return skills_text
    
    def _update_profile_sections(self, current_profile: str, *new_sections: str) -> str:
        """Update the profile with new sections"""
        # Find the position to insert new content (after the header)
        lines = current_profile.split('\n')
        
        # Look for the first major section (usually after social links and current work)
        insert_position = 0
        for i, line in enumerate(lines):
            if line.startswith('## ') and 'Featured Project' in line:
                insert_position = i
                break
            elif line.startswith('## ') and 'Tech Stack' in line:
                insert_position = i
                break
            elif line.startswith('## ') and 'GitHub Stats' in line:
                insert_position = i
                break
        
        if insert_position == 0:
            # If no major sections found, insert after the current work section
            for i, line in enumerate(lines):
                if line.startswith('- ⚡ Fun fact'):
                    insert_position = i + 2  # Insert after the fun fact line
                    break
            
            if insert_position == 0:
                # Fallback: insert after the first few lines
                insert_position = min(25, len(lines))
        
        # Insert new sections
        new_content = '\n\n'.join(new_sections)
        lines.insert(insert_position, '\n' + new_content)
        
        return '\n'.join(lines)

def main():
    """Main execution function"""
    try:
        # Load configuration
        config_path = 'github_profile_config.json'
        if not os.path.exists(config_path):
            logging.error(f"Configuration file {config_path} not found!")
            return
        
        with open(config_path, 'r') as f:
            config = json.load(f)
        
        logging.info("🚀 Starting GitHub Profile Updater")
        
        # Initialize scanner
        scanner = ProjectScanner(config)
        
        # Scan workspace
        projects = scanner.scan_workspace()
        
        if not projects:
            logging.warning("No projects found. Check your configuration and workspace path.")
            return
        
        # Generate updated profile
        generator = ProfileGenerator(config, projects, scanner.technologies)
        updated_profile = generator.generate_updated_profile()
        
        # Save updated profile
        with open('README_UPDATED.md', 'w', encoding='utf-8') as f:
            f.write(updated_profile)
        
        # Save project analysis
        analysis_data = {
            'scan_timestamp': datetime.now().isoformat(),
            'total_projects': len(projects),
            'total_technologies': len(scanner.technologies),
            'projects': projects,
            'technologies': list(scanner.technologies)
        }
        
        with open('project_analysis.json', 'w', encoding='utf-8') as f:
            json.dump(analysis_data, f, indent=2, default=str)
        
        logging.info("✅ Profile update complete!")
        logging.info(f"📁 Updated profile saved to: README_UPDATED.md")
        logging.info(f"📊 Project analysis saved to: project_analysis.json")
        logging.info(f"🔍 Discovered {len(projects)} projects with {len(scanner.technologies)} technologies")
        
        # Print summary
        print("\n" + "="*60)
        print("🎉 GITHUB PROFILE UPDATE COMPLETE!")
        print("="*60)
        print(f"📁 Projects Found: {len(projects)}")
        print(f"🛠️ Technologies: {len(scanner.technologies)}")
        print(f"📝 Updated Profile: README_UPDATED.md")
        print(f"📊 Analysis Data: project_analysis.json")
        print("="*60)
        print("\nNext steps:")
        print("1. Review README_UPDATED.md")
        print("2. Copy content to your README.md")
        print("3. Commit and push to GitHub")
        print("4. Run again weekly for updates!")
        
    except Exception as e:
        logging.error(f"Fatal error: {e}")
        raise

if __name__ == "__main__":
    main()