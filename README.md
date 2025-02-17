# Automated Resume Parser 📄➡️📊

A Python-based tool for extracting structured data from resumes in PDF, DOCX, and TXT formats using NLP and pattern matching.

## Features ✨
- **Multi-format Support**: Process PDF, DOCX, and TXT files
- **Core Information Extraction**:
  - Contact details (name, email, phone, social links)
  - Education history and qualifications
  - Work experience timelines
  - Technical skills and certifications
- **Smart Section Detection**: Identifies common resume sections
- **Output Formats**: JSON and CSV exports
- **Batch Processing**: Handle multiple files simultaneously

## Installation 🛠️

git clone https://github.com/DarshanCode2005/resume-parser.git
cd resume-parser
pip install -r requirements.txt


## Requirements 📦
- Python 3.8+
- spaCy (`en_core_web_sm` model)
- pdfminer.six
- python-docx
- pandas

## Usage 🚀

from resume_parser import ResumeParser

Single file processing
parser = ResumeParser()
parsed_data = parser.parse_resume("resumes/john_doe.pdf")

Batch processing
parser.process_directory("input_resumes/", "output_data/")


## Output Structure 📂

{
"contact_information": {
"name": "John Doe",
"email": "john@example.com",
"phone": "+1-555-123-4567",
"linkedin": "linkedin.com/in/johndoe"
},
"education": [
"BSc Computer Science - University of Tech (2018-2022)"
],
"skills": [
"Python", "Machine Learning", "AWS"
],
"certifications": [
"AWS Certified Developer - 2023"
]
}


## Key Technologies 🔍
| Component          | Technology Used       |
|---------------------|-----------------------|
| NLP Processing      | spaCy NER Model       |
| Text Extraction     | pdfminer, python-docx |
| Data Structuring    | JSON/CSV serialization|
| Pattern Matching    | Regular Expressions   |

## Roadmap 🗺️
- [ ] Add AI-powered section interpretation
- [ ] Implement resume scoring system
- [ ] Support image-based resumes (OCR)
- [ ] Multi-language support
- [ ] REST API integration

## Contributing 🤝
We welcome contributions! Please see our [Contribution Guidelines](CONTRIBUTING.md) for details.

## License 📄
MIT License - See [LICENSE](LICENSE) for details