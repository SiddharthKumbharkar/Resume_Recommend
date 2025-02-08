import streamlit as st
import pdfplumber
from docx import Document
import google.generativeai as genai

# Configure Gemini API
API_KEY = "AIzaSyB7_NrE5fs9CK9vUIrHwFGit--pLM58Opg"  # Replace with your API key
genai.configure(api_key=API_KEY)

# Function to extract text from PDF
def extract_text_from_pdf(pdf_file):
    text = ""
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text

# Function to extract text from DOCX
def get_learning_recommendations(resume_text):
    prompt = f"""
    I have extracted the following resume text:
    {resume_text}
    
    Analyze the **technical skills** mentioned in my resume and structure your response into the following sections:
    
    1. **Current Technical Skills (Based on Resume)**  
       - Extract only technical skills found in the resume.

    2. **Skills to Learn (To Complement Current Skills)**  
       - Recommend advanced or related skills that will enhance my technical expertise.
       - Focus on in-demand technologies, programming languages, frameworks, and tools.

    3. **Market Demand for Current Skills**  
       - Analyze how relevant my current technical skills are in today’s job market.
       - Mention the demand level (**High, Medium, or Low**) and relevant job roles.

    **Example Output:**
    - **Current Technical Skills**: Python, Data Analysis, SQL  
    - **Skills to Learn**: Machine Learning, Cloud Computing, Big Data Analytics  
    - **Market Demand**: Python & Data Analysis have **high** demand in AI, Finance, and Data Science roles. SQL is **medium demand**, useful in database management and backend development.

    **Provide your response in a structured, bullet-point format.**
    """
    
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt)
    return response.text




# Streamlit UI
st.title("📄 Resume Learning Recommendation System")
st.write("Upload your resume (PDF or DOCX), and get learning recommendations!")

uploaded_file = st.file_uploader("Upload Resume", type=["pdf", "docx"])

if uploaded_file is not None:
    st.success("File uploaded successfully!")

    # Extract text based on file type
    file_extension = uploaded_file.name.split(".")[-1]
    resume_text = ""

    if file_extension == "pdf":
        resume_text = extract_text_from_pdf(uploaded_file)
    elif file_extension == "docx":
        resume_text = extract_text_from_docx(uploaded_file)
    else:
        st.error("Unsupported file format! Please upload a PDF or DOCX file.")

    # Display extracted text (optional)
    if st.checkbox("Show Extracted Text"):
        st.text_area("Extracted Resume Text", resume_text, height=200)

    # Get and display recommendations
    if st.button("Get Learning Recommendations"):
        if resume_text:
            with st.spinner("Analyzing your resume..."):
                recommendations = get_learning_recommendations(resume_text)
            st.subheader("📚 Learning Recommendations:")
            st.write(recommendations)
        else:
            st.error("Could not extract text from the resume!")

