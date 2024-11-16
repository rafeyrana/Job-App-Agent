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


job_description = '''
Finance is all about the numbers…unless you work at Amazon; it’s knowing the numbers plus so much more. Enthusiasm, energy and diverse perspectives help us deliver new ideas and solutions. Do you view problems as treasures, and are you willing to dive deep to develop those solutions and deliver results? Will you seek to challenge the status quo, and accept that your ideas and mechanisms may be tested daily? At Amazon, we move with purpose and speed, and this requires that we work with a dynamic network of partners across businesses. We help others understand finance and are trusted advisors for every facet of data and communication to ensure our leaders have the most up to date and reliable information to help make the best possible decisions. The challenges we take on span multiple industries and functions across our many businesses and acquisitions, all powered by the same mission—to be Earth's most customer-centric company.

Key job responsibilities

This is an exciting opportunity for a seasoned engineer. In this position, you will play a leading role in architecture, design, implementation and deployment of large-scale critical and complex financial applications. You will push your design and architecture limits by owning all aspects of solutions end-to-end, through full stack software development. You have strong verbal and written communication skills, are self-motivated, and can deliver high quality results in a fast-paced environment. You will work across Amazon engineering teams and business teams across the globe in planning, designing, executing and implementing this new platform across multiple geographies.

Basic Qualifications

 3+ years of non-internship professional software development experience
 2+ years of non-internship design or architecture (design patterns, reliability and scaling) of new and existing systems experience
 Experience programming with at least one software programming language

Preferred Qualifications

 3+ years of full software development life cycle, including coding standards, code reviews, source control management, build processes, testing, and operations experience
 Bachelor's degree in computer science or equivalent

Amazon is committed to a diverse and inclusive workplace. Amazon is an equal opportunity employer and does not discriminate on the basis of race, national origin, gender, gender identity, sexual orientation, protected veteran status, disability, age, or other legally protected status. For individuals with disabilities who would like to request an accommodation, please visit https://www.amazon.jobs/en/disability/us.

Our compensation reflects the cost of labor across several US geographic markets. The base pay for this position ranges from $129,300/year in our lowest geographic market up to $223,600/year in our highest geographic market. Pay is based on a number of factors including market location and may vary depending on job-related knowledge, skills, and experience. Amazon is a total compensation company. Dependent on the position offered, equity, sign-on payments, and other forms of compensation may be provided as part of a total compensation package, in addition to a full range of medical, financial, and/or other benefits. For more information, please visit https://www.aboutamazon.com/workplace/employee-benefits. This position will remain posted until filled. Applicants should apply via our internal or external career site.
'''



print(ResumeLLM(job_description=job_description))