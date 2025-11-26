import streamlit as st
from openai import OpenAI
import trafilatura

# Page Configuration
st.set_page_config(page_title="News Neutralizer", page_icon="⚖️")

def neutralize_text(api_key, text_input):
    """
    Sends text to OpenAI to remove bias and emotion.
    """
    try:
        client = OpenAI(api_key=api_key)
        
        system_prompt = (
            "You are an objective, un-biased news editor. "
            "Your goal is to rewrite the provided text to be purely factual. "
            "Remove emotional language, subjective adjectives, and any political or personal bias. "
            "Keep the core facts intact, but change the tone to be neutral and dry."
        )

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": text_input}
            ],
            temperature=0.3
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

def get_text_from_url(url):
    """
    Downloads and extracts the main text from a news URL.
    """
    downloaded = trafilatura.fetch_url(url)
    if downloaded is None:
        return None
    return trafilatura.extract(downloaded)

# --- App Layout ---

st.title("⚖️ News Neutralizer")
st.markdown("Remove emotional language and bias from articles.")

# Sidebar for API Key
api_key = st.sidebar.text_input("Enter OpenAI API Key", type="password")

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
                st.error("Could not read text from this URL. Try pasting the text manually.")

with tab2:
    text_input = st.text_area("Or Paste Text Here:", height=200)
    if text_input:
        article_text = text_input

# Main Action
if st.button("Neutralize Text"):
    if not api_key:
        st.warning("Please enter your OpenAI API key in the sidebar.")
    elif not article_text:
        st.warning("Please provide a URL or paste text first.")
    else:
        with st.spinner("Analyzing and rewriting..."):
            neutral_text = neutralize_text(api_key, article_text)
            
            st.subheader("Neutralized Version")
            st.success(neutral_text)
            
            with st.expander("See Original Text"):
                st.text(article_text)
