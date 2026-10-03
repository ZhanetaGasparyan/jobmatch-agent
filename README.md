# JobMatch Agent

A tool-calling AI agent that compares job advertisements with a verified candidate profile, calculates an evidence-based match score, identifies skill gaps, and creates a prioritized application checklist.

The project is designed for students who want structured support when deciding which job opportunities fit their current experience.

## Live demo

Try the deployed application:

[https://zhaneta-jobmatch-agent.streamlit.app](https://zhaneta-jobmatch-agent.streamlit.app)

> The match score supports decision-making only. It does not predict whether an applicant will be interviewed or hired.

## Key features

- Extracts structured requirements from unstructured job advertisements
- Loads a verified candidate profile with evidence for each skill
- Calculates a deterministic and transparent match score
- Separates required skill gaps from preferred skill gaps
- Generates an honest, prioritized application checklist
- Supports follow-up questions with conversation memory
- Compares and ranks multiple job opportunities
- Shows which tools the agent selected and called
- Uses strict structured output to prevent malformed AI responses
- Includes automated tests for scoring, tools, profile validation, error handling, agent behavior, and result parsing
- Runs automated tests through GitHub Actions
- Provides a public Streamlit deployment with protected secrets

## How it works

1. The user pastes a job advertisement.
2. The agent extracts structured job requirements.
3. The verified candidate profile is loaded.
4. Deterministic Python logic compares the profile with the requirements.
5. The agent presents the score, matched skills, missing skills, and an application checklist.
6. The user can ask follow-up questions while the agent remembers the current conversation.
7. Additional jobs can be analyzed and ranked on the comparison board.

```text
Job advertisement
        │
        ▼
Requirement extraction
        │
        ▼
Verified candidate profile
        │
        ▼
Deterministic scoring
        │
        ▼
Match analysis and application checklist
        │
        ▼
Follow-up conversation and job comparison
```

The language model coordinates the workflow, but it does not decide the match score itself. Scoring is performed by deterministic Python logic, making the result reproducible and explainable.

## Agent tools

| Tool | Purpose |
|---|---|
| `get_candidate_profile` | Loads the verified profile and supporting skill evidence |
| `extract_requirements` | Extracts structured requirements from a job advertisement |
| `calculate_job_match` | Calculates the deterministic match score |
| `create_application_checklist` | Produces evidence-based application actions |

The **Agent activity** section in the interface displays which tools were selected and called during an analysis.

## Technology stack

- Python 3.11
- Groq API
- GPT-OSS 20B
- LangChain
- LangGraph
- Pydantic
- Streamlit
- Streamlit Community Cloud
- pytest
- GitHub Actions

## Project structure

```text
jobmatch-agent/
├── .github/
│   └── workflows/
│       └── tests.yml
├── app/
│   ├── __init__.py
│   ├── agent.py
│   ├── dashboard.py
│   ├── errors.py
│   ├── extractor.py
│   ├── profile.py
│   ├── result_parser.py
│   ├── schemas.py
│   ├── scoring.py
│   └── tools.py
├── data/
│   └── candidate_profile.json
├── scripts/
├── tests/
├── .env.example
├── .gitignore
├── README.md
└── requirements.txt
```

## Local setup

### 1. Clone the repository

```bash
git clone https://github.com/ZhanetaGasparyan/jobmatch-agent.git
cd jobmatch-agent
```

### 2. Create a virtual environment

```bash
python3.11 -m venv .venv
source .venv/bin/activate
```

On Windows:

```powershell
py -3.11 -m venv .venv
.venv\Scripts\activate
```

### 3. Install the dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Configure the API key

Copy the example environment file:

```bash
cp .env.example .env
```

Add your private Groq API key to `.env`:

```text
GROQ_API_KEY=your_groq_api_key_here
```

Never commit `.env` or expose an API key publicly.

### 5. Run the tests

```bash
python -m pytest -v
```

Current test suite: **16 passing tests**.

The tests are also executed automatically through GitHub Actions whenever changes are pushed to the repository.

### 6. Start the application

```bash
python -m streamlit run app/dashboard.py
```

Open the local address displayed in the terminal.

## Match scoring

The score is calculated using deterministic Python logic:

- Required skills contribute 80% of the score
- Preferred skills contribute 20% of the score
- Skill aliases are normalized before matching
- Unknown skills are never invented
- Missing skills remain visible in the final result

### Recommendation levels

| Score | Recommendation |
|---|---|
| 75–100 | Strong match |
| 50–74 | Possible match |
| 0–49 | Needs development |

The score measures alignment between the verified profile and the extracted job requirements. It is not a prediction of interview or hiring outcomes.

## Conversation memory

The agent uses a LangGraph in-memory checkpointer and a unique conversation ID. Users can ask follow-up questions about an analyzed job while preserving the context of the current conversation.

Starting a new conversation clears the current job analysis and conversation context but keeps the temporary job-comparison board.

## Job comparison

Every completed analysis is added to a temporary comparison board. Analyzed jobs are ranked by their deterministic match scores.

The board displays:

- Job title
- Company
- Match score
- Recommendation
- Missing required skills
- Missing preferred skills

The comparison data exists only during the current Streamlit session.

## Structured AI output

Job requirements are extracted using a strict structured-output schema. This validates the model response before it enters the scoring workflow and reduces failures caused by malformed JSON.

The extraction process separates:

- Required skills
- Preferred skills
- Required languages
- Responsibilities
- Education requirements

The model is instructed to use only information explicitly stated in the job advertisement.

## Privacy and responsible use

- Job advertisements are sent to the configured Groq model for analysis.
- The verified candidate profile is used as context during the agent workflow.
- The application does not automatically submit job applications.
- The system is instructed not to invent experience or recommend dishonest claims.
- API keys are stored in a local `.env` file during development and in encrypted Streamlit Secrets during deployment.
- API keys are never committed to Git.
- Users should avoid adding private contact information to publicly accessible profile files.
- Public visitors use the deployment owner's configured API quota when running an analysis.

## Current limitations

- The included profile is configured for one candidate.
- The comparison board is stored only in the current Streamlit session.
- Job-requirement extraction depends on an external language-model API.
- Match scores represent skill alignment, not hiring probability.
- The application does not currently parse uploaded CV files.
- The public demo may be affected by external API rate limits.

## Future improvements

- Editable candidate profiles
- Per-user profiles
- CV upload and structured extraction
- Persistent job-comparison history
- Exportable analysis reports
- Rate limiting for the public demonstration
- Additional tests for external API boundaries
- Support for additional model providers

## Responsible interpretation

Job advertisements can be incomplete or ambiguous. The extracted requirements and calculated score should therefore be reviewed by the user.

A lower score does not necessarily mean that somebody should not apply. The application is intended to organize available evidence, reveal skill gaps, and support a more informed decision.

## Author

**Zhaneta Gasparyan**

Computer Science student at TU Darmstadt.