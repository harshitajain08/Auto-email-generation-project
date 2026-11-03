
"""
MailCraft AI - Intelligent Email Drafting Agent
Built using CrewAI and OpenRouter.
"""

import argparse
import os

from crewai import Agent, Crew, Process, Task
from dotenv import load_dotenv

load_dotenv()


def build_email_crew(
    context: str,
    tone: str,
    recipient: str,
    email_type: str = "General email",
    additional_details: str = "",
    call_to_action: str = "",
) -> str:

    if not os.getenv("OPENROUTER_API_KEY"):
        raise ValueError("OPENROUTER_API_KEY is missing from .env")

    llm = "openrouter/openrouter/free"

    # AGENT 1: Email Context Analyst
    analyst = Agent(
        role="Email Context Analyst",
        goal="Understand the user's email requirements and create a detailed writing brief.",
        backstory=(
            "You are an expert in professional communication. "
            "You identify the purpose, audience, key information, "
            "and appropriate structure of different types of emails."
        ),
        llm=llm,
        verbose=False,
    )

    # AGENT 2: Professional Email Writer
    writer = Agent(
        role="Professional Email Writer",
        goal="Create personalized, clear, and contextually appropriate emails.",
        backstory=(
            "You are an experienced business communication specialist "
            "who writes natural, effective and professional emails."
        ),
        llm=llm,
        verbose=False,
    )

    # TASK 1: Analyze requirements
    analyze_task = Task(
        description=f"""
Analyze the following email requirements.

EMAIL TYPE: {email_type}
RECIPIENT: {recipient}
USER'S CONTEXT: {context}
PREFERRED TONE: {tone}
ADDITIONAL DETAILS: {additional_details}
CALL TO ACTION: {call_to_action}

Identify:
1. Main purpose of the email.
2. Important information to include.
3. Appropriate email structure.
4. Suitable greeting and closing.
5. Whether a call to action is required.

Do not add information that the user has not provided.
""",
        agent=analyst,
        expected_output="A structured email writing brief.",
    )

    # TASK 2: Generate email
    write_task = Task(
        description=f"""
Using the analyst's brief, write a complete email.

EMAIL TYPE: {email_type}
RECIPIENT: {recipient}
CONTEXT: {context}
TONE: {tone}
ADDITIONAL DETAILS: {additional_details}
CALL TO ACTION: {call_to_action}

REQUIREMENTS:

1. Create a relevant subject line.
2. Use an appropriate greeting.
3. Write a clear and natural email body.
4. Include the requested call to action, if provided.
5. End with an appropriate closing and signature placeholder.
6. Adapt the structure to the selected email type.
7. Keep the email concise and relevant.

IMPORTANT:
- Never invent names, dates, times, links, prices,
  company details or other factual information.
- Never create fake meeting availability or calendar links.
- If essential information is missing, use a clear
  placeholder such as [Recipient Name].
- Do not include unnecessary generic sales language.
- Do not mention the AI or explain how the email was generated.

Return only the final formatted email.
""",
        agent=writer,
        expected_output="A complete, personalized email ready for review.",
        context=[analyze_task],
    )

    crew = Crew(
        agents=[analyst, writer],
        tasks=[analyze_task, write_task],
        process=Process.sequential,
        verbose=False,
    )

    result = crew.kickoff()

    return str(result)


def main():

    parser = argparse.ArgumentParser(
        description="MailCraft AI - Email Drafting Agent"
    )

    parser.add_argument("--context", default="Follow up on our product demo from last Tuesday.")
    parser.add_argument("--tone", default="Professional and friendly")
    parser.add_argument("--recipient", default="A potential client")
    parser.add_argument("--email-type", default="Follow-up email")
    parser.add_argument("--details", default="")
    parser.add_argument("--cta", default="")

    args = parser.parse_args()

    print("\n✉️ MailCraft AI - Drafting your email...\n")

    email = build_email_crew(
        context=args.context,
        tone=args.tone,
        recipient=args.recipient,
        email_type=args.email_type,
        additional_details=args.details,
        call_to_action=args.cta,
    )

    print("=" * 60)
    print("📧 YOUR GENERATED EMAIL")
    print("=" * 60)
    print(email)


if __name__ == "__main__":
    main()
