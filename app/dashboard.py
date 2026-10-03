import sys
import uuid
from pathlib import Path

import streamlit as st


# Allow imports from the project's app package.
PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


from app.agent import run_agent
from app.errors import user_friendly_error_message
from app.result_parser import parse_job_comparison


st.set_page_config(
    page_title="JobMatch Agent",
    page_icon="🎯",
    layout="wide",
)


# Initialize session state.
if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())

if "conversation" not in st.session_state:
    st.session_state.conversation = []

if "last_tools" not in st.session_state:
    st.session_state.last_tools = []

if "saved_jobs" not in st.session_state:
    st.session_state.saved_jobs = []

if "job_text" not in st.session_state:
    st.session_state.job_text = ""


# Button callback functions.
def start_new_conversation():
    """Clear the conversation while preserving saved comparisons."""
    st.session_state.thread_id = str(uuid.uuid4())
    st.session_state.conversation = []
    st.session_state.last_tools = []
    st.session_state.job_text = ""


def clear_comparison_board():
    """Remove all jobs from the temporary comparison board."""
    st.session_state.saved_jobs = []


# Page header.
st.title("🎯 JobMatch Agent")
st.subheader("Evidence-based job analysis for students")

st.write(
    """
    Paste a job advertisement to compare its requirements with a
    verified candidate profile. The agent extracts requirements,
    calls deterministic scoring tools, identifies missing skills,
    and creates an honest application checklist.
    """
)


# Sidebar.
with st.sidebar:
    st.header("How it works")

    st.markdown(
        """
        1. Extract job requirements
        2. Load the verified profile
        3. Calculate a transparent score
        4. Create an application checklist
        """
    )

    st.info(
        "The match score supports decision-making. "
        "It does not predict hiring outcomes."
    )

    st.button(
        "Start a new conversation",
        use_container_width=True,
        on_click=start_new_conversation,
    )


# Job advertisement form.
with st.form("job_analysis_form"):
    job_text = st.text_area(
        "Job advertisement",
        height=320,
        placeholder=(
            "Paste the complete working-student "
            "job advertisement here..."
        ),
        key="job_text",
    )

    analyze_button = st.form_submit_button(
        "Analyze job",
        type="primary",
        use_container_width=True,
    )


# Run the complete agent workflow.
if analyze_button:
    if len(job_text.strip()) < 50:
        st.warning(
            "Please paste a job advertisement containing "
            "at least 50 characters."
        )
    else:
        prompt = f"""
Perform a complete analysis of this job advertisement.

You must:
1. Extract its requirements.
2. Load and use the verified candidate profile.
3. Calculate the match using the scoring tool.
4. Create an honest application checklist.
5. Explain matched and missing skills.

Job advertisement:
{job_text}
"""

        try:
            with st.spinner(
                "The agent is extracting requirements "
                "and calling tools..."
            ):
                result = run_agent(
                    prompt,
                    thread_id=st.session_state.thread_id,
                )

            tools_used = []

            for message in result["messages"]:
                tool_calls = getattr(
                    message,
                    "tool_calls",
                    None,
                )

                if tool_calls:
                    for tool_call in tool_calls:
                        tools_used.append(tool_call["name"])

            final_response = result["messages"][-1].content

            # Extract structured results for the comparison board.
            comparison = parse_job_comparison(
                result["messages"]
            )

            if comparison is not None:
                comparison_data = comparison.model_dump()

                existing_index = next(
                    (
                        index
                        for index, saved_job in enumerate(
                            st.session_state.saved_jobs
                        )
                        if (
                            saved_job["job_title"]
                            == comparison_data["job_title"]
                            and saved_job["company"]
                            == comparison_data["company"]
                        )
                    ),
                    None,
                )

                # Add a new job or update an existing job.
                if existing_index is None:
                    st.session_state.saved_jobs.append(
                        comparison_data
                    )
                else:
                    st.session_state.saved_jobs[
                        existing_index
                    ] = comparison_data

            st.session_state.last_tools = tools_used

            st.session_state.conversation.append(
                {
                    "role": "assistant",
                    "content": final_response,
                }
            )

        except Exception as error:
            st.error(user_friendly_error_message(error))

            with st.expander("Error type"):
                st.code(type(error).__name__)


# Display saved jobs in a comparison table.
if st.session_state.saved_jobs:
    st.divider()
    st.header("📊 Job Comparison")

    st.caption(
        "Analyzed jobs are ranked by their transparent match score."
    )

    sorted_jobs = sorted(
        st.session_state.saved_jobs,
        key=lambda job: job["score"],
        reverse=True,
    )

    table_rows = []

    for job in sorted_jobs:
        recommendation = (
            job["recommendation"]
            .replace("_", " ")
            .capitalize()
        )

        table_rows.append(
            {
                "Job": job["job_title"],
                "Company": (
                    job["company"] or "Not specified"
                ),
                "Score": f'{job["score"]}%',
                "Recommendation": recommendation,
                "Required gaps": (
                    ", ".join(
                        job["missing_required_skills"]
                    )
                    or "None"
                ),
                "Preferred gaps": (
                    ", ".join(
                        job["missing_preferred_skills"]
                    )
                    or "None"
                ),
            }
        )

    st.dataframe(
        table_rows,
        use_container_width=True,
        hide_index=True,
    )

    st.button(
        "Clear comparison board",
        on_click=clear_comparison_board,
    )


# Display tools selected by the agent.
if st.session_state.last_tools:
    with st.expander(
        "Agent activity",
        expanded=True,
    ):
        st.write("The agent selected and called:")

        for tool_name in st.session_state.last_tools:
            st.code(tool_name)


# Display the current conversation.
for message in st.session_state.conversation:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# Follow-up conversation input.
follow_up = st.chat_input(
    "Ask a follow-up question about the analyzed job..."
)

if follow_up:
    st.session_state.conversation.append(
        {
            "role": "user",
            "content": follow_up,
        }
    )

    try:
        with st.spinner(
            "The agent is reviewing the conversation..."
        ):
            result = run_agent(
                follow_up,
                thread_id=st.session_state.thread_id,
            )

        answer = result["messages"][-1].content

        st.session_state.conversation.append(
            {
                "role": "assistant",
                "content": answer,
            }
        )

        st.rerun()

    except Exception as error:
        st.error(user_friendly_error_message(error))

        with st.expander("Error type"):
            st.code(type(error).__name__)