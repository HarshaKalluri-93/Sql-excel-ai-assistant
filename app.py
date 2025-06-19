import streamlit as st
import google.generativeai as genai
import os

st.set_page_config(page_title="SQL & Excel AI Assistant", page_icon="🤖")

# --- API Key Configuration ---
# It's best practice to use Streamlit secrets for deployed apps,
# but for local development, environment variables are fine.
# We'll use os.environ.get here, but know that st.secrets is an option.
api_key = os.environ.get("GEMINI_API_KEY")

if not api_key:
    st.error("GEMINI_API_KEY environment variable not set.")
    st.warning("Please set your API key as an environment variable before running the Streamlit app.")
    st.code("For Windows PowerShell: $env:GEMINI_API_KEY='YOUR_API_KEY_HERE'")
    st.stop() # Stop the app if API key is missing

genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash')

# --- Streamlit UI ---
st.title("💡 SQL & Excel AI Assistant")
st.markdown("Ask me anything about SQL queries, Excel formulas, or cheat sheets. I'm here to help!")

# Input text area for user query
user_query = st.text_area("Your Question:", height=150, placeholder="e.g., 'SQL query to find active users', or 'Excel formula for conditional formatting'")

# Button to trigger AI response
if st.button("Get AI Help", use_container_width=True):
    if user_query:
        # Crafting the prompt for Gemini (using the advanced prompt structure)
        prompt_for_gemini = f"""
        You are an extremely knowledgeable and precise AI assistant specializing in SQL queries and Excel formulas.
        Your goal is to provide accurate, concise, and ready-to-use answers.

        *Instructions:*
        1.  If the request is for an *SQL query*: Provide only the SQL code block, formatted like:
            sql
            -- Your SQL here
            
            Do NOT include any conversational text before or after the code. If an explanation is explicitly requested, provide it clearly.
        2.  If the request is for an *Excel formula*: Provide only the Excel formula, formatted like:
            excel
            =YOUR_FORMULA_HERE
            
            Do NOT include any conversational text before or after the formula. If an explanation is explicitly requested, provide it clearly.
        3.  If the request is for a *cheat sheet or explanation*: Provide a detailed, well-structured, and comprehensive explanation or cheat sheet. Use bullet points or code blocks where appropriate for clarity.
        4.  Always prioritize giving the most common, standard, and efficient solution.
        5.  If you cannot fulfill the request, politely state that you cannot.
        6.  If the request is ambiguous (e.g., could be SQL or Excel), ask the user for clarification before providing an answer.

        Example 1 :
        User:SQL to get distinct product names.
        AI: 
        ```sql
        SELECT DISTINCT product_name FROM products;
        ```
        Example 2 :
        User:Excel formula to concatenate the sum of a range.
        AI: 
        ```excel
        =CONCATANATE(A1:A10)
        ```

        User's request: {user_query}
        """

        try:
            with st.spinner("Thinking..."): # Show a spinner while AI is processing
                response = model.generate_content(prompt_for_gemini)

            if response and response.text:
                st.subheader("AI Assistant's Response:")
                st.markdown(response.text) # Streamlit renders markdown, so code blocks will look nice!
            else:
                st.warning("AI Assistant: I couldn't generate a response for that. Please try rephrasing.")

        except Exception as e:
            st.error(f"An error occurred: {e}")
            st.info("Please ensure your internet connection is stable and your API key is correct and valid.")
    else:
        st.warning("Please enter your question in the text area above!")

st.markdown("---")
st.caption("Built with Gemini and Streamlit")