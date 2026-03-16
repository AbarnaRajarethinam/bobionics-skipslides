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

    prompt =  f"""
You are a senior software engineer preparing presentation slides explaining a software repository to technical students.

Your task is to analyze the repository and generate structured slide content.

GENERAL GUIDELINES
- Use bullet points only.
- Avoid long paragraphs.
- Prefer 3–5 bullet points per slide.
- Keep bullets concise and technical.
- Focus on architecture, workflow, features, and implementation.
- Only describe functionality visible in the provided files.
- If information cannot be determined, write: "Not clearly defined in repository."
- Avoid repeating the same information across slides.

OUTPUT FORMAT

Each slide must begin with a tag exactly like this:

[SLIDE: Slide Title]

Example:

[SLIDE: Project Overview]
• bullet
• bullet
• bullet

These tags are used by an automated slide generator.

OPTIONAL SECTIONS

You may include the following sections when appropriate.

CODE SNIPPET FORMAT

If a slide includes important implementation logic, include a short code snippet using this exact format:

[CODE]
code line
code line
code line
[/CODE]

Rules:
- Maximum 8 lines
- Only include code that exists in the repository
- Do not fabricate code

Example:

[CODE]
def evaluate(node):
    left = evaluate(node.left)
    right = evaluate(node.right)
    return apply(node.op, left, right)
[/CODE]


WORKFLOW / PIPELINE DIAGRAM FORMAT

If a slide explains system workflow, processing flow, or data pipeline, include a diagram using this format:

[DIAGRAM]
Step 1 → Step 2 → Step 3 → Step 4
[/DIAGRAM]

Rules:
- Use arrows "→"
- Maximum 6 steps
- Each step should be short (2–4 words)


SLIDE GENERATION RULES

Generate approximately 6–8 slides describing the repository.

Include these core slides when possible:
• Problem & Motivation
• Project Overview
• System Architecture

Additional slides should be generated based on repository structure. Possible slides include:

• Key Features
• System Workflow
• Core Components
• Implementation Highlights
• Running the Project
• Limitations or Future Improvements


FEATURE SLIDE GUIDELINES

If the repository contains multiple capabilities, group them into feature-focused slides.

Example feature slide titles:
• Feature: Expression Management
• Feature: Evaluation Engine
• Feature: Data Processing Pipeline


IMPLEMENTATION DETAILS

When useful:
- include short code snippets using the [CODE] format
- include workflow diagrams using the [DIAGRAM] format


IMPORTANT FORMATTING RULES

- Always start slides with [SLIDE: Title]
- Use bullet points starting with "•"
- Place [CODE] or [DIAGRAM] sections AFTER the bullet points
- Do not include markdown formatting
- Do not include triple backticks


REPOSITORY FILES
{file_text}
"""

    return prompt

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