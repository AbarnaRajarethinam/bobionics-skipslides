import os
from dotenv import load_dotenv
from openai import OpenAI

# ------------------------------
# Load environment variables
# ------------------------------
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("OPENAI_API_KEY not found. Please check your .env file.")

client = OpenAI(api_key=api_key)


# ------------------------------
# Build prompt for LLM
# ------------------------------
def build_prompt(files):
    """
    Convert extracted repo files into a structured prompt
    for the LLM to analyze any type of repository and
    generate slide-ready explanations.
    """

    MAX_FILE_CHARS = 2000
    file_text = ""

    for f in files:
        filename = f.get("filename", "unknown_file")
        content = f.get("content", "")

        file_text += "\n\n===== FILE: " + filename + " =====\n"
        file_text += content[:MAX_FILE_CHARS]

    prompt = f"""
    You are a senior software engineer preparing presentation slides to explain a GitHub repository to technical students.

    Your task is to analyze the repository and produce a structured explanation that can be directly converted into presentation slides.

    IMPORTANT RULES:
    - Use bullet points only.
    - Avoid long paragraphs.
    - Each slide must contain at least 4 bullet points but no more than 6.
    - Each bullet point must be under 20 words.
    - Focus on explaining architecture, workflow, and components.
    - Do not invent functionality that is not present in the repository.
    - Only analyze the files that are provided.
    - If information cannot be determined, output: "Not clearly defined in repository."

    FILE CONTENT NOTE:
    Repository file contents may be truncated to fit analysis limits.
    If content appears incomplete, summarize only what is visible and do not guess missing functionality.

    CODE EXAMPLE RULES:
    - Provide 2–3 short code snippets (maximum 10 lines each).
    - Only use snippets from the provided repository files.
    - Do not invent or fabricate code.
    - If no meaningful snippet exists, state: "No clear code example identified."

    OUTPUT FORMAT REQUIREMENT:
    Each section must start with a slide tag in the exact format:

    [SLIDE: Slide Title]

    Example:
    [SLIDE: Problem Statement]
    • bullet point
    • bullet point
    • bullet point
    • bullet point

    These tags will be used by an automated slide generation system.

    Return the explanation using the following slide structure:

    [SLIDE: Problem Statement]
    • What real-world or technical problem this project solves
    • Why the problem is important

    [SLIDE: Project Overview]
    • What the system does
    • Type of system (ML model, web app, CLI tool, etc.)

    [SLIDE: Key Features]
    • List the most important capabilities

    [SLIDE: Technologies & Tools]
    • Programming languages used
    • Frameworks
    • Libraries
    • APIs or databases

    [SLIDE: System Modules]
    Explain the major components and their responsibilities.

    Example format:
    • main.py → entry point
    • model.py → machine learning model
    • server.js → backend API server

    [SLIDE: Data / Processing Pipeline]
    Explain the step-by-step process of how the system works.

    Examples depending on project type:

    Machine Learning:
    • Load dataset
    • Preprocess data
    • Train model
    • Evaluate performance
    • Output predictions

    Web Application:
    • User sends request
    • Backend processes request
    • Database query executed
    • Response returned to user

    [SLIDE: System Architecture]
    Explain how modules interact and how the system is structured.

    [SLIDE: Deployment & Execution]
    Explain how the system is run or deployed.

    Examples:
    • Run using Python script
    • Backend server deployment
    • Docker container
    • Cloud deployment
    • Local execution

    [SLIDE: Key Code Examples]
    Provide 2–3 short but meaningful code snippets (maximum 10 lines each).

    Format:

    Code Example: <description>

    <code snippet>

    [SLIDE: Real World Applications]
    Explain who would use this system and in what scenarios.

    Repository files:
    {file_text}
    """

    return prompt

# ------------------------------
# Analyze repository using LLM
# ------------------------------
# ------------------------------
# Analyze repository using LLM
# ------------------------------
def analyze_repository(files):
    """
    Send repository files to the LLM and return
    a structured explanation of the project.
    """

    prompt = build_prompt(files)

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        temperature=0.2,
        messages=[
            {
                "role": "system",
                "content": "You are an expert software engineer who explains codebases clearly for technical presentations."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    # Extract explanation
    explanation = response.choices[0].message.content

    # ------------------------------
    # DEV TERMINAL OUTPUT
    # ------------------------------
    print("\n" + "=" * 70)
    print("AI REPOSITORY ANALYSIS (DEV OUTPUT)")
    print("=" * 70)
    print(explanation)
    print("=" * 70 + "\n")

    # Return explanation normally
    return explanation