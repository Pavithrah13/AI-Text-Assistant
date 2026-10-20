import os
import streamlit as st
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

# Load environment variables
load_dotenv()

# Configure the Streamlit page
st.set_page_config(
    page_title="AI Text Assistant",
    page_icon="🤖",
    layout="centered"
)

# Application title
st.title("AI Text Assistant")

st.write("Ask me anything! I'll try to help you.")

# Get Gemini API key
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    try:
        api_key = st.secrets["GOOGLE_API_KEY"]
    except (KeyError, FileNotFoundError):
        api_key = None

# Create the input box
question = st.text_area(
    "Enter your question:",
    placeholder="Example: Explain Python in simple English"
)

# Generate response button
if st.button("Generate Response"):

    if not question.strip():
        st.warning("Please enter a question!")

    elif not api_key:
        st.error("API key not found. Please check your .env file.")

    else:
        try:
            with st.spinner("Generating your answer..."):

                # Initialize Gemini
                llm = ChatGoogleGenerativeAI(
                    model="gemini-3.8-flash",
                    google_api_key=api_key,
                    temperature=0.7
                )

                # Create prompt template
                prompt = PromptTemplate.from_template(
                    "Answer the following question in simple English. "
                    "Be clear and concise.\nQuestion: {question}"
                )

                # Connect prompt and model
                chain = prompt | llm

                # Generate the response
                response = chain.invoke(
                    {"question": question}
                )

            # Display the response
            st.subheader("AI Response")

            if isinstance(response.content, str):
                st.markdown(response.content)
            else:
                for item in response.content:
                    if item.get("type") == "text":
                        st.markdown(item.get("text", ""))

        except Exception as e:
            st.error(f"Something went wrong: {e}")
