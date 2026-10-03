import sys
import uuid
from pathlib import Path

import streamlit as st


PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.agent import run_agent


st.set_page_config(
    page_title="JobMatch Agent",
    page_icon="🎯",
    layout="wide",
)

if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())

if "conversation" not in st.session_state:
    st.session_state.conversation = []

if "last_tools" not in st.session_state:
    st.session_state.last_tools = []


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

    if st.button("Start a new conversation"):
        st.session_state.thread_id = str(uuid.uuid4())
        st.session_state.conversation = []
        st.session_state.last_tools = []
        st.rerun()


with st.form("job_analysis_form"):
    job_text = st.text_area(
        "Job advertisement",
        height=320,
        placeholder=(
            "Paste the complete working-student job advertisement here..."
        ),
    )

    analyze_button = st.form_submit_button(
        "Analyze job",
        type="primary",
        use_container_width=True,
    )


if analyze_button:
    if len(job_text.strip()) < 50:
        st.warning(
            "Please paste a job advertisement containing at least "
            "50 characters."
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
                "The agent is extracting requirements and calling tools..."
            ):
                result = run_agent(
                    prompt,
                    thread_id=st.session_state.thread_id,
                )

            tools_used = []

            for message in result["messages"]:
                tool_calls = getattr(message, "tool_calls", None)

                if tool_calls:
                    for tool_call in tool_calls:
                        tools_used.append(tool_call["name"])

            final_response = result["messages"][-1].content

            st.session_state.last_tools = tools_used
            st.session_state.conversation.append(
                {
                    "role": "assistant",
                    "content": final_response,
                }
            )

        except Exception as error:
            st.error(
                "The analysis could not be completed. "
                "Please try again shortly."
            )

            with st.expander("Technical details"):
                st.code(str(error))


if st.session_state.last_tools:
    with st.expander("Agent activity", expanded=True):
        st.write("The agent selected and called:")

        for tool_name in st.session_state.last_tools:
            st.code(tool_name)


for message in st.session_state.conversation:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


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
        with st.spinner("The agent is reviewing the conversation..."):
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
        st.error("The follow-up could not be completed.")

        with st.expander("Technical details"):
            st.code(str(error))