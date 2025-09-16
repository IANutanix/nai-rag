# RAG Chat Application

A clean, minimal RAG (Retrieval-Augmented Generation) application with Streamlit frontend and Python backend.

## Features

- 🎨 Beautiful gradient UI with Pasture of Dreams color scheme
- 🔍 PDF document search and retrieval
- 💬 Chat interface with conversation history
- ⚙️ Configurable OpenAI-compatible API endpoints
- 📚 Multiple knowledge bases: Employee, Police, Insurance, Law, and Nutanix
- 🔧 10 comprehensive Nutanix technical documentation PDFs

## Quick Start

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Generate sample documents:**
```bash
python3 create_pdfs.py
python3 create_nutanix_pdfs.py
```

3. **Run the application:**
```bash
streamlit run app.py
```

Or use the runner script:
```bash
python3 run_app.py
```

## Configuration

Configure your API settings in the sidebar:
- **Endpoint URL**: OpenAI-compatible API endpoint
- **Model Name**: Model to use for responses  
- **API Key**: Your API authentication key

Default configuration uses Nutanix AI endpoint with llama3370b model.

## Usage

1. 🧪 Test your API connection using the "Test Connection" button
2. 💬 Start chatting with the documents using the chat input
3. 🔍 The system searches relevant documents and generates contextual responses

## Knowledge Bases

### Employee Knowledge (10 documents)
- **Employee Badge Request Process** - Badge requests and replacements
- **WiFi Setup Guide** - Network connection instructions
- **IT Support Tickets** - Technical support process
- **VPN Setup Instructions** - Remote access configuration
- **Expense Reports** - Business expense submission
- **Conference Room Booking** - Meeting room reservations
- **Time Off Requests** - Leave and vacation process
- **New Employee Onboarding** - First week orientation
- **Password Reset Guide** - Account security procedures
- **Remote Work Policy** - Work-from-home guidelines

### Nutanix Documentation (10 documents)
- **Prism Central Setup** - Centralized management deployment
- **AHV Virtualization** - Hypervisor configuration and management
- **Nutanix Calm** - Application orchestration and automation
- **Nutanix Files** - Enterprise file services
- **Nutanix Objects** - S3-compatible object storage
- **Nutanix Databases** - Database lifecycle management
- **Security Best Practices** - Infrastructure and data protection
- **Disaster Recovery** - Business continuity planning
- **Performance Tuning** - Optimization guidelines
- **Upgrade Procedures** - Software and firmware updates

## Architecture

- **app.py** - Streamlit frontend with chat interface
- **backend.py** - RAG engine with PDF processing and search
- **create_pdfs.py** - Employee document generation script
- **create_nutanix_pdfs.py** - Nutanix documentation generation script
- **documents/** - Employee PDF document storage
- **nutanix_documents/** - Nutanix PDF document storage

## Technical Details

- **PDF Processing**: PyPDF2 for text extraction
- **Search**: Keyword-based scoring with title weighting
- **Context**: Maintains conversation history and document context
- **UI**: Custom CSS with gradient background and modern styling