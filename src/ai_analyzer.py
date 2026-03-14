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
You are a senior software engineer analyzing a GitHub repository.

The repository could be ANY type of software project, including:
- algorithm / data structures projects
- AI / machine learning systems
- deep learning models (CNN, GAN, transformers)
- data science or data visualization
- web applications (frontend/backend)
- APIs or microservices
- CLI tools or automation scripts
- research prototypes

Your task is to analyze the repository and produce a clear,
structured explanation that could be directly converted into
presentation slides for technical students.

Guidelines:
- Use concise bullet points
- Avoid long paragraphs
- Focus on explaining how the system works
- Adapt explanation depending on project type

Return the explanation using this structure:

1. Project Overview
• What the project does
• What problem it solves
• What type of system it is (ML model, web app, CLI tool, etc.)

2. Key Features
List the most important capabilities or functionalities.

3. Technologies & Tools
Identify major technologies used such as:
• programming languages
• frameworks
• ML libraries
• visualization tools
• databases or APIs

4. Main Components
List the important files/modules and explain their responsibilities.

Example format:
- main.py → entry point that launches the application
- model.py → defines machine learning model
- server.js → backend API server
- visualizer.py → generates charts

5. System Architecture
Explain how the components interact and how the system is structured.

6. Application Workflow
Describe the step-by-step flow of how the program works.

Examples depending on project type:

Example (ML pipeline):
1. Load dataset
2. Preprocess data
3. Train model
4. Evaluate performance
5. Output predictions

Example (web application):
1. User sends request
2. Backend API processes request
3. Database query executed
4. Response returned to client

Example (algorithmic tool):
1. User inputs data
2. Algorithm processes input
3. Results computed
4. Output displayed

7. Important Code Examples
Select 2–3 short but meaningful code snippets that represent key logic.
Keep snippets under 10 lines.

Format:

Code Example: <description>

<code snippet>

8. Real-World Use Cases
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