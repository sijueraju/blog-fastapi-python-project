from fastapi import  HTTPException
from openai import OpenAI, AuthenticationError, RateLimitError, OpenAIError
from typing import Optional, List
import os
import sys

def generate_llm_content(
        prompt: str,
        max_tokens: int = 1000,
        temperature: float = 0.7,
        model: str = "gpt-3.5-turbo"
) -> dict:

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    try:
        print(f"=== OpenAI Request ===")
        print(f"Model: {model}")
        print(f"Prompt: {prompt[:100]}...")
        print(f"Max tokens: {max_tokens}")

        response = client.chat.completions.create(
            model= model,
            messages=[
                {"role": "system", "content": "You are a professional content writer for a blog."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=max_tokens,
            temperature=temperature
        )

        # Check if response has content
        if not response.choices or not response.choices[0].message.content:
            raise HTTPException(
                status_code=500,
                detail="OpenAI returned an empty response. Please try again."
            )
        content = response.choices[0].message.content

        result =  {
            "content": content,
            "tokens_used": response.usage.total_tokens,
            "model": model
        }

        return result

    except AuthenticationError:
        raise HTTPException(status_code=401, detail="Invalid OpenAI API key")
    except RateLimitError:
        raise HTTPException(status_code=429, detail="OpenAI rate limit exceeded")
    except OpenAIError as e:
        raise HTTPException(status_code=500, detail=f"OpenAI API error: {str(e)}")
    except HTTPException:
        raise  # Re-raise HTTPException as-is
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")


def build_prompt(
        topic: str,
        tone: str,
        max_words: int,
        keywords: Optional[List[str]] = None
) -> str:
    keyword_text = f"Include these keywords: {', '.join(keywords)}" if keywords else ""

    prompts = f"""Write a {tone} blog post about "{topic}".
                Word count: approximately {max_words} words.
                {keyword_text}
                Include an engaging introduction, well-structured body, and conclusion."""

    return prompts