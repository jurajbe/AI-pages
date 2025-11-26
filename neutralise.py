import streamlit as st
import google.generativeai as genai
import trafilatura
import os

# Page Configuration
st.set_page_config(page_title="News Neutralizer", page_icon="⚖️")

def neutralize_text_gemini(api_key, text_input):
    """
    Sends text to Google Gemini to remove bias and emotion.
    """
    try:
        # Configure the library with the user's key
        genai.configure(api_key=api_key)
        
        # Select the model (Gemini Pro is free and powerful)
        model = genai.GenerativeModel('gemini-pro')
        
        # The prompt instruction
        prompt = (
            "You are an objective, un-biased news editor. "
            "Rewrite the following text to be purely factual. "
            "Remove emotional language, subjective adjectives, and any political or personal bias. "
            "Keep the core facts intact, but change the tone to be neutral and dry.\n\n"
            f"TEXT TO REWRITE:\n{text_input}"
        )

        # Generate response
        response = model.generate_content(prompt)
        return response.text

    except Exception as e:
        return f"Error: {str(e)}"

def get_text_from_url(url):
    """
    Downloads and extracts the main text from a news URL.
    """
    try:
        downloaded = trafilatura.fetch_url(url)
        if downloaded is None:
            return None
        return trafilatura.extract(downloaded)
    except Exception:
        return None

# --- App Layout ---

st.title("⚖️ News Neutralizer (Free Edition)")
st.markdown("Remove emotional language and bias from articles using Google Gemini.")

# Sidebar for API Key
api_key = st.sidebar.text_input("Enter Google Gemini API Key", type="password")
st.sidebar.caption("Get a free key at aistudio.google.com")

# Tabs for input method
tab1, tab2 = st.tabs(["🔗 Paste Link", "📝 Paste Text"])

article_text = ""

with tab1:
    url_input = st.text_input("Paste Article URL:")
    if url_input:
        with st.spinner("Fetching article content..."):
            extracted = get_text_from_url(url_input)
            if extracted:
                st.info("Article fetched successfully!")
                article_text = extracted
            else:
                st.error("Could not read text from this URL. Some sites block automated readers.")

with tab2:
    text_input = st.text_area("Or Paste Text Here:", height=200)
    if text_input:
        article_text = text_input

# Main Action
if st.button("Neutralize Text"):
    if not api_key:
        st.warning("Please enter your Google API key in the sidebar.")
    elif not article_text:
        st.warning("Please provide a URL or paste text first.")
    else:
        with st.spinner("Analyzing and rewriting..."):
            neutral_text = neutralize_text_gemini(api_key, article_text)
            
            st.subheader("Neutralized Version")
            st.success(neutral_text)
            
            with st.expander("See Original Text"):
                st.text(article_text)
