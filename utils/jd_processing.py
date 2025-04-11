import os
import pandas as pd
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
llm = ChatGroq(model_name="mistral-saba-24b", temperature=0.2)

def summarize_jd(jd_text):
    prompt = PromptTemplate(
        input_variables=["jd"],
        template="""
Summarize the following job description into key responsibilities and qualifications:

{jd}

Return a concise summary.
        """
    )
    chain = LLMChain(llm=llm, prompt=prompt)
    result = chain.invoke({"jd": jd_text})
    return result.get("text", "")

def save_job_description(job_title, job_description, file_path):
    new_data = pd.DataFrame({"Job Title": [job_title], "Job Description": [job_description]})
    if os.path.exists(file_path):
        existing = pd.read_csv(file_path, encoding="ISO-8859-1")
        df = pd.concat([existing, new_data], ignore_index=True)
    else:
        df = new_data
    df.to_csv(file_path, index=False, encoding="ISO-8859-1")
