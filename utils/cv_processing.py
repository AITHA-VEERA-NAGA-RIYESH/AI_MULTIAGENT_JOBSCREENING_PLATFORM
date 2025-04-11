import os
import re
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_groq import ChatGroq
from langchain.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv

load_dotenv()
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
llm = ChatGroq(model_name="mistral-saba-24b", temperature=0.2)
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

def process_cv(file_path):
    loader = PyPDFLoader(file_path)
    pages = loader.load()
    full_text = "\n\n".join([p.page_content for p in pages])

    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_text(full_text)

    vectordb = FAISS.from_texts(chunks, embedding_model)
    vectordb.save_local("faiss_index/cv")

    name_match = re.search(r"(?:Name[:\-]?\s*)([A-Z][a-z]+(?:\s[A-Z][a-z]+)+)", full_text)
    email_match = re.search(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", full_text)

    name = name_match.group(1) if name_match else "Candidate"
    email = email_match.group(0) if email_match else "ajaykumarmeeturi@gmail.com"

    return chunks, full_text, name, email

def evaluate_candidate(jd_summary, cv_chunks, name, job_title):
    prompt = PromptTemplate(
        input_variables=["jd", "cv", "candidate_name", "job_title"],
        template="""
Given the following job summary:
{jd}

And the following candidate CV:
{cv}

Determine whether the candidate is suitable for the {job_title} position.
Return ONLY your answer in the EXACT following format (with no additional text):
Decision: <Suitable / Not Suitable>
Reason: <Justify the decision>
Basis: <Criteria used, e.g., skills, experience, education>
        """
    )
    chain = LLMChain(llm=llm, prompt=prompt)
    result = chain.invoke({
        "jd": jd_summary,
        "cv": "\n".join(cv_chunks),
        "candidate_name": name,
        "job_title": job_title
    })
    return result.get("text", "No result")
