from flask import Blueprint, jsonify, request
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_groq import ChatGroq

lm = Blueprint('lm', __name__)

@lm.route('/', methods=['GET'])
def default_status():
    try:
        # Return a success message to indicate the server is running
        return jsonify({"message": "Server is running!"}), 200
    except Exception as e:
        print("An error occurred:", e)
        return jsonify({"error": "An internal error occurred"}), 500

def initialize_llm():
    try:
        llm = ChatGroq(
            temperature=0,
            groq_api_key="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",
            model_name="llama-3.3-70b-versatile"
        )
        print("LLM initialized successfully.")
        return llm
    except Exception as e:
        print("Error initializing LLM:", e)
        raise

def setup_llm_chain(llm):
    prompt_template = """You are an expert IELTS examiner with extensive experience in evaluating Writing Task responses. Your task is to provide detailed, constructive, and accurate feedback based on the official IELTS Writing Task assessment criteria:

    1. **Task Achievement (Task Response)**:
        - Does the response fully address all parts of the task?
        - Is the position clear and well-developed?
        - Are ideas relevant, fully extended, and well-supported?

    2. **Coherence and Cohesion**:
        - Is the information logically organized?
        - Are paragraphs used effectively?
        - Are cohesive devices (e.g., linking words, pronouns) used appropriately?

    3. **Lexical Resource**:
        - Is there a wide range of vocabulary used accurately and appropriately?
        - Are there any inaccuracies in word choice or collocation?
        - Is the language precise and varied?

    4. **Grammatical Range and Accuracy**:
        - Is there a variety of sentence structures (simple, compound, complex)?
        - Are grammar and punctuation used accurately?
        - Are there frequent errors that impede communication?

    ---

    ### **Instructions for Feedback**:
    1. **Provide a Band Score (0-9)** for each of the four criteria above.
    2. **Summarize the overall band score** based on the individual scores.
    3. **Give detailed feedback** for each criterion, highlighting strengths and areas for improvement.
    4. **Offer specific suggestions** for improvement, including examples where applicable.
    5. **Maintain a professional and encouraging tone** to motivate the user.

    ---

    ### **User's Writing Task Response**:
    {question}

    ---

    ### **Your Feedback**:"""


    PROMPT = PromptTemplate(template=prompt_template, input_variables=["question"])

    llm_chain = LLMChain(llm=llm, prompt=PROMPT)
    print("LLM chain setup successfully.")
    return llm_chain

# Initialize LLM and chain globally for reuse
llm = initialize_llm()
llm_chain = setup_llm_chain(llm)

@lm.route('/chatbot', methods=['GET'])
def chatbot():
    try:
        # Get question from query parameters
        question = request.args.get('question')
        if not question:
            return jsonify({"error": "Missing 'question' parameter"}), 400

        # Generate response from the LLM chain
        response = llm_chain.run({"question": question})

        # Return the response as JSON
        return jsonify({"response": response})

    except Exception as e:
        print("An error occurred:", e)
        return jsonify({"error": "An internal error occurred"}), 500
