import os

from dotenv import load_dotenv
from google import genai

from models import CodeReview

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY is not set in the .env file")

client = genai.Client(api_key=api_key)


def review_code(code):
    prompt = f"""
You are an expert software engineer performing a code review.

Analyze the following source code.

Look for:

1. Bugs
2. Security vulnerabilities
3. Code-quality problems
4. Performance concerns
5. Improvement opportunities

For every issue you find, provide:

- severity
- category
- title
- description
- suggestion

Severity must be one of:

Critical
High
Medium
Low

Category should be one of:

Bug
Security
Performance
Code Quality

If you don't find a problem, do not invent one.

After analyzing the code, create an improved version of the COMPLETE source code.

The improved code should:
- Fix the identified issues where possible
- Preserve the original functionality
- Follow reasonable coding practices
- Be complete and runnable
- Not contain explanations or Markdown code fences

Source code:

{code}

Provide an accurate and practical review.
"""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt,
        config={
            "response_mime_type": "application/json",
            "response_schema": CodeReview,
        },
    )

    return CodeReview.model_validate_json(response.text)
