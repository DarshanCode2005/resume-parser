import re
import json
from pathlib import Path
from typing import Dict, List, Optional
import spacy
from pdfminer.high_level import extract_text
from docx import Document
import pandas as pd

class ResumeParser:
    def __init__(self):
        # Load SpaCy model for NER
        self.nlp = spacy.load("en_core_web_sm")
        
        # Common section headers in resumes
        self.sections = {
            'education': ['education', 'academic background', 'qualifications'],
            'experience': ['experience', 'work experience', 'employment history', 'work history'],
            'skills': ['skills', 'technical skills', 'competencies', 'expertise'],
            'projects': ['projects', 'personal projects', 'academic projects'],
            'certifications': ['certifications', 'certificates', 'professional certifications']
        }
        
        # Regex patterns for common data
        self.patterns = {
            'email': r'[\w\.-]+@[\w\.-]+\.\w+',
            'phone': r'(\+\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}',
            'linkedin': r'linkedin\.com/in/[\w\-]+/?',
            'github': r'github\.com/[\w\-]+/?'
        }

    def extract_text_from_file(self, file_path: str) -> str:
        """Extract text from different file formats."""
        file_path = Path(file_path)
        
        if file_path.suffix.lower() == '.pdf':
            return extract_text(file_path)
        elif file_path.suffix.lower() in ['.docx', '.doc']:
            doc = Document(file_path)
            return '\n'.join([paragraph.text for paragraph in doc.paragraphs])
        elif file_path.suffix.lower() in ['.txt']:
            return file_path.read_text()
        else:
            raise ValueError(f"Unsupported file format: {file_path.suffix}")

    def find_contact_info(self, text: str) -> Dict[str, str]:
        """Extract contact information using regex patterns."""
        contact_info = {}
        
        for info_type, pattern in self.patterns.items():
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                contact_info[info_type] = match.group()
                
        # Extract name using SpaCy NER
        doc = self.nlp(text[:1000])
        for ent in doc.ents:
            if ent.label_ == "PERSON":
                contact_info['name'] = ent.text
                break
                
        return contact_info

    def extract_sections(self, text: str) -> Dict[str, str]:
        """Extract different sections from the resume."""
        sections_found = {}
        lines = text.split('\n')
        current_section = None
        section_content = []
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Check if line is a section header
            line_lower = line.lower()
            found_section = None
            
            for section_name, headers in self.sections.items():
                if any(header in line_lower for header in headers):
                    found_section = section_name
                    break
            
            if found_section:
                if current_section:
                    sections_found[current_section] = '\n'.join(section_content)
                current_section = found_section
                section_content = []
            elif current_section:
                section_content.append(line)
        
        # Add the last section
        if current_section and section_content:
            sections_found[current_section] = '\n'.join(section_content)
            
        return sections_found

    def extract_skills(self, text: str) -> List[str]:
        """Extract skills from text using NLP and custom rules."""
        # Common technical skills keywords
        tech_skills = set(['python', 'java', 'javascript', 'html', 'css', 'sql', 'react', 
                          'node.js', 'aws', 'docker', 'kubernetes', 'machine learning'])
        
        skills = set()
        words = text.lower().split()
        
        for word in words:
            if word in tech_skills:
                skills.add(word)

        doc = self.nlp(text)
        for ent in doc.ents:
            if ent.label_ in ["ORG", "PRODUCT"]:
                skills.add(ent.text.lower())
                
        return list(skills)

    def parse_resume(self, file_path: str) -> Dict:
        """Main method to parse resume and return structured data."""
        text = self.extract_text_from_file(file_path)
        contact_info = self.find_contact_info(text)
        sections = self.extract_sections(text)
        skills = self.extract_skills(text)
        parsed_data = {
            'contact_information': contact_info,
            'sections': sections,
            'skills': skills
        }
        
        return parsed_data

    def save_to_json(self, parsed_data: Dict, output_path: str):
        """Save parsed resume data to JSON file."""
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(parsed_data, f, indent=2)

    def save_to_structured_format(self, parsed_data: Dict, output_path: str, format: str = 'json'):
        """Save parsed data in different formats."""
        if format.lower() == 'json':
            self.save_to_json(parsed_data, output_path)
        elif format.lower() == 'csv':
            # Convert to DataFrame and save as CSV
            df = pd.DataFrame([parsed_data])
            df.to_csv(output_path, index=False)
        else:
            raise ValueError(f"Unsupported output format: {format}")

def main():
    parser = ResumeParser()
    
    # Parse a single resume
    # Hello please write the path to your resume
    resume_path = "./data-scientist-1559725114.pdf"
    parsed_data = parser.parse_resume(resume_path)
    parser.save_to_structured_format(parsed_data, "output.json", "json")
    parser.save_to_structured_format(parsed_data, "output.csv", "csv")
    
    # Batch processing example
    def process_directory(directory_path: str, output_directory: str):
        directory = Path(directory_path)
        output_dir = Path(output_directory)
        output_dir.mkdir(exist_ok=True)
        
        for resume_file in directory.glob("*"):
            if resume_file.suffix.lower() in ['.pdf', '.docx', '.doc', '.txt']:
                try:
                    parsed_data = parser.parse_resume(str(resume_file))
                    output_path = output_dir / f"{resume_file.stem}_parsed.json"
                    parser.save_to_structured_format(parsed_data, str(output_path))
                    print(f"Successfully parsed: {resume_file.name}")
                except Exception as e:
                    print(f"Error processing {resume_file.name}: {str(e)}")

if __name__ == "__main__":
    main()