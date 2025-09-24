import google.generativeai as genai

# Configure Gemini API
def configure_gemini(api_key):
    """Initialize and return Gemini model"""
    genai.configure(api_key=api_key)
    return genai.GenerativeModel('gemini-2.0-flash-exp')


# Generate AI response
def get_response(model, prompt):
    """
    Generate AI response for a given prompt.
    Returns the text or an error message.
    """
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"


# Session history management
def save_to_history(question, answer, history):
    """
    Save a question-answer pair to history list
    """
    history.append({"question": question, "answer": answer})
    return history
