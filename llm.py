from groq import Groq
from dotenv import load_dotenv
import os

from config import RESUME_EXTRACT
from prompts import SYSTEM_PROMPT


def ResumeLLM(job_description):
  load_dotenv()
  client = Groq(api_key=os.getenv("GROQ_API_KEY"))
  chat_completion = client.chat.completions.create(
      messages=[
          {
              "role": "system",
              "content": SYSTEM_PROMPT
          },
          {
              "role": "user",
              "content": f"##\n{RESUME_EXTRACT}\n##\n\n^^\n{job_description}\n^^"
          }
      ],
      model="llama3-70b-8192",
      stream=False,
  )
  return chat_completion.choices[0].message.content
