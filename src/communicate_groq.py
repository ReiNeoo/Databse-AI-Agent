from langchain_groq import ChatGroq
from typing import Dict, Any
import asyncio
import os
from dotenv import load_dotenv  # pip install python-dotenv

load_dotenv()  # Load environment variables from .env file


class GroqProcessor:
    def __init__(self, config: Dict[str, any]):
        self.config = config.copy()  # Copy to avoid modifying original config
        self.llm = ChatGroq(**self.config)

    async def invoke(self, question: str, system_prompt: str = None):
        """
        Get complete response for a given question

        Args:
            question: User's question
            system_prompt: Optional system prompt to guide the response

        Returns:
            str: Complete response from the LLM
        """
        # Prepare messages
        messages = []

        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})

        messages.append({"role": "user", "content": question})

        try:
            # Get complete response
            response = await self.llm.ainvoke(messages)
            return response.content

        except Exception as e:
            raise Exception(f"Error invoking LLM: {str(e)}")


async def main():
    GROQ_CONFIG = {
        "model": "meta-llama/llama-4-scout-17b-16e-instruct",
        "temperature": 0.1,
        "streaming": False,
    }
    prompt = "meraba televole"
    ai = GroqProcessor(GROQ_CONFIG)
    response = await ai.invoke(prompt)
    print(response)


if __name__ == "__main__":
    print("ele")
    asyncio.run(main())
