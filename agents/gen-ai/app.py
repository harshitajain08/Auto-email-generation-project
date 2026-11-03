
import streamlit as st

from agent import build_email_crew

# Page configuration
st.set_page_config(
    page_title="MailCraft AI",
    page_icon="✉️",
    layout="centered",
)

# Custom styling
st.markdown("""
<style>
    .block-container {
        max-width: 850px;
        padding-top: 2rem;
    }

    .main-title {
        font-size: 2.5rem;
        font-weight: 750;
        text-align: center;
    }

    .subtitle {
        text-align: center;
        color: #888888;
        margin-bottom: 30px;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown(
    '<div class="main-title">✉️ MailCraft AI</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Your intelligent AI-powered email writing assistant.'
    '</div>',
    unsafe_allow_html=True
)

st.divider()

st.subheader("Let's create your email!")

st.write(
    "Answer a few questions so our AI agents can "
    "understand your requirements and draft the email."
)

# Email type
email_types = [
    "Follow-up email",
    "Cold outreach email",
    "Job application email",
    "Apology email",
    "Thank-you email",
    "Meeting request",
    "Business proposal",
    "Complaint email",
    "Resignation email",
    "Leave request",
    "Networking email",
    "Other",
]

email_type = st.selectbox(
    "1. What type of email do you want to write?",
    email_types,
)

if email_type == "Other":
    email_type = st.text_input(
        "Specify your email type",
        placeholder="e.g. Internship acceptance email",
    )

# Recipient
recipient = st.text_input(
    "2. Who is the recipient?",
    placeholder="e.g. Hiring manager, professor, client...",
)

# Context
context = st.text_area(
    "3. What is the email about?",
    placeholder=(
        "Explain the situation, what happened, "
        "and what you want to communicate..."
    ),
    height=130,
)

# Tone
tone = st.selectbox(
    "4. What tone should the email have?",
    [
        "Professional and friendly",
        "Formal",
        "Casual and conversational",
        "Polite and respectful",
        "Persuasive",
        "Apologetic",
        "Confident and assertive",
        "Warm and appreciative",
    ],
)

# Additional details
additional_details = st.text_area(
    "5. Any additional details to include? (Optional)",
    placeholder=(
        "Names, dates, deadlines, important points, "
        "or other information..."
    ),
    height=100,
)

# CTA
call_to_action = st.text_input(
    "6. What action should the recipient take? (Optional)",
    placeholder="e.g. Schedule a meeting, respond to my application...",
)

st.divider()

# Generate email
if st.button("✨ Generate My Email", use_container_width=True):

    if not context.strip():
        st.warning("Please describe what your email is about.")

    elif not recipient.strip():
        st.warning("Please enter the recipient.")

    elif email_type == "Other" and not email_type.strip():
        st.warning("Please specify the email type.")

    else:
        try:
            with st.spinner(
                "Our AI agents are analyzing your requirements "
                "and drafting your email..."
            ):
                email = build_email_crew(
                    context=context,
                    tone=tone,
                    recipient=recipient,
                    email_type=email_type,
                    additional_details=additional_details,
                    call_to_action=call_to_action,
                )

            st.success("Your email has been generated!")

            st.subheader("📧 Your Drafted Email")

            st.text_area(
                "Review and edit your email below:",
                value=email,
                height=350,
                key="generated_email",
            )

            st.download_button(
                label="⬇️ Download Email",
                data=email,
                file_name="generated_email.txt",
                mime="text/plain",
                use_container_width=True,
            )

        except Exception as e:
            st.error(f"Something went wrong: {str(e)}")

st.divider()

st.caption(
    "MailCraft AI | Powered by CrewAI and OpenRouter"
)
