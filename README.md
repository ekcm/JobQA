<!-- PROJECT LOGO -->
<div align="center">
  <h2 align="center">JobQA</h2>

  <p align="center">
    A LLM-powered application that generates answers to job application questions using documents such as the applicant's Resume and the job posting using Retrieval Augmented Generation (RAG). 
  </p>
</div>

<!-- ABOUT THE PROJECT -->
## About The Project
This project was built for the [Nvidia and LlamaIndex Developer Contest](https://developer.nvidia.com/llamaindex-developer-contest). 
I wanted to address the personal dread of answering questions during the job application process as it is both time-consuming and brain-numbing. I also wanted to real-time feedback on tailoring my resume to job postings. I'm proud to say this project has managed to achieve these 2 core features.

I also implemented Nvidia NeMo Guardrails to safeguard against prompt engineering vulnerabilities, ensuring topical relevance, and maintaining content appropriateness. I do think every RAG and LLM-powered user-facing application needs to have guardrails to prevent abuse.

## Built With
* [LlamaIndex](https://www.llamaindex.ai/)
* [Nvidia NeMo Guardrails](https://docs.nvidia.com/nemo/guardrails/)
* [Python](https://www.python.org/)
* [FastAPI](https://fastapi.tiangolo.com/)
* [Pinecone](https://www.pinecone.io/)

## Project Directory
```
JobQA/
├── backend/
│   ├── app/
│   │   ├── api/        # Routing
│   │   ├── core/       # Configuration Management
│   │   ├── guardrails/ # NeMo Guardrails Configuration
│   │   ├── ingestion/  # Ingestion process
│   │   ├── retrieval/  # Retrieval process
│   │   ├── schemas/    # Pydantic schema
│   │   └── main.py     # Entry point to the application
│   ├── tests/          # Unit tests
│   ├── poetry.lock
│   ├── pyproject.toml
│   ├── pytest.ini
│   └── .env            # Create a .env file here
├── .gitignore
└── README.md
```

## Getting Started

To get a local copy up and running, follow these steps:
### Clone the repository
```bash
git clone https://github.com/ekcm/JobQA
cd JobQA
```

### Download poetry
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

### Install dependencies
```bash
cd backend
poetry install
```

### Activate the virtual environment
```bash
poetry shell
```

### Environment variables setup
Create a .env file in the backend directory. See Project Directory for more informaton.
```bash
OPENAI_API_KEY=<OPENAI_API_KEY>
PINECONE_API_KEY=<PINECONE_API_KEY>
PINECONE_INDEX_NAME=<PINECONE_INDEX>
```

### Starting the application
To start the application in the backend directory, run the following command:
```
uvicorn app.main:app --reload
```
You should see a Uvicorn output indicating that the server is running and accessible at `http://127.0.0.1:8000`

## To do list:
1. Build Frontend to interact with the application
2. Integrate AI Search to query information such as company's culture fit
3. Integrate Feedback Loop
