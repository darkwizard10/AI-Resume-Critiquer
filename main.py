import streamlit as st
import io
import PyPDF2 
from langchain_together import ChatTogether
from dotenv import load_dotenv
import os

load_dotenv()


st.set_page_config(page_title="AI Resume Critiquer",page_icon="📃",layout="centered")

st.title("AI Resume Critiquer")
st.markdown("Upload your resume and get AI-powered feedback tailored to  your needs!")

TOGETHER_API_KEY=os.getenv("TOGETHER_API_KEY")
uf=st.file_uploader("Upload your (PDF or TXT)",type=["pdf","txt"])
job_role=st.text_input("Enter the job role you're targeting (optional)")

analyze=st.button("Analyze Resume")

def extract_pdf(pdf_file):
    pdf_reader=PyPDF2.PdfReader(pdf_file)
    text=""
    for page in pdf_reader.pages:
        text+=page.extract_text()+"\n"
    return text    

def extractor(uf):
    if uf.type =="application/pdf":
        return extract_pdf(io.BytesIO(uf.read()))
    return uf.read().decode("utf-8")

if analyze and uf:
    try:
        file_content=extractor(uf)

        if not file_content.strip():
            st.error("File does not have any content")
            st.stop()

        prompt = f"""Assume yourself as an expert resume analyzer who has worked with big mnc and startups and has many years of experience Please analyze this resume and provide constructive feedback. 
            Focus on the following aspects:
            1. Content clarity and impact
            2. Skills presentation
            3. Experience descriptions
            4. Specific improvements for {job_role if job_role else 'general job applications'}    

        Resume content:
        {file_content}

        Please provide your analysis in a clear,well defiend,structured format with specific recomadations"""
        
        llm = ChatTogether(
    model="deepseek-ai/DeepSeek-V3",  # You can also try Llama-3-8b or Llama-4-Maverick
    temperature=0.7
)

        response=llm.invoke(prompt )
        st.markdown("### Analysis Results")
        st.markdown(response.content)
    except  Exception as e:
        st.error(f"An error occured {str(e)}")   
