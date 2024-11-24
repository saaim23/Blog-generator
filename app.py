import streamlit as st
from transformers import pipeline
import time

# Function to get response from a text generation model
def getResponse(input_text, no_words, blog_style, tone, format_type):
    try:
        pipe = pipeline("text-generation", model="gpt2")
    except Exception as e:
        st.error(f"Error loading model: {e}")
        return "Error loading model."

    # Prompt Template
    template = f"""
        Write a blog for {blog_style} job profile on the topic "{input_text}" in a {tone} tone and {format_type} format within {no_words} words.
    """

    # Generate the response from the model
    response = pipe(template, max_length=no_words, num_return_sequences=1)[0]['generated_text']
    return response

# Streamlit configuration
st.set_page_config(
    page_title="Generate Blogs",
    page_icon='🤖',
    layout='centered',
    initial_sidebar_state='collapsed'
)

st.header("Generate Blogs 🤖")

input_text = st.text_input("Enter the Blog Topic")

# Creating two more columns for additional fields
col1, col2 = st.columns([5, 5])

with col1:
    no_words = st.number_input('Number of Words', min_value=50, max_value=2000, value=500, step=50)
with col2:
    blog_style = st.selectbox('Writing the blog for', ['Researchers', 'Data Scientist', 'Common People'], index=0)

# Additional options for tone and format
tone = st.selectbox('Select Tone', ['Informative', 'Casual', 'Professional', 'Humorous'], index=0)
format_type = st.selectbox('Select Format', ['Essay', 'Listicle', 'Narrative'], index=0)

submit = st.button("Generate")

# Final response
if submit:
    if not input_text:
        st.error("Please enter a blog topic.")
    else:
        with st.spinner('Generating your blog...'):
            response = getResponse(input_text, no_words, blog_style, tone, format_type)
            st.write(response)
            
            # Display a progress bar
            for i in range(100):
                time.sleep(0.01)
                st.progress(i + 1)
            
            # Word count check
            word_count = len(response.split())
            st.write(f"Generated blog contains {word_count} words.")
            
            # Provide a download button for the generated blog
            st.download_button(
                label="Download Blog",
                data=response,
                file_name='generated_blog.txt',
                mime='text/plain'
            )