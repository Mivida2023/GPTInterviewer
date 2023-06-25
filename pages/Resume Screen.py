# langchain: https://python.langchain.com/
import time
from dataclasses import dataclass
import streamlit as st
from speech_recognition.openai_whisper import save_wav_file, transcribe
from audio_recorder_streamlit import audio_recorder
from langchain.callbacks import get_openai_callback
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import RetrievalQA, ConversationChain
from langchain.prompts.prompt import PromptTemplate
from langchain.prompts import (
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    ChatPromptTemplate,
    MessagesPlaceholder
)
from prompts.prompts import templates
from typing import Literal
from azure_service.speech_synthesizer import speech_synthesizer
from azure.cognitiveservices.speech import AudioDataStream
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.text_splitter import NLTKTextSplitter
import nltk
from PyPDF2 import PdfReader
from prompts.prompt_selector import prompt_sector
from streamlit_lottie import st_lottie
import json

### -----------------------------------------------------------------------------------------------------------
if not nltk.data.find('tokenizers/punkt'):
    nltk.download('punkt')

def load_lottiefile(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)

st_lottie(load_lottiefile("images/hello.json"), speed=1, reverse=False, loop=True, quality="high", height=300)
st.markdown("### Instruction: ")
st.markdown("""
    In this session, the GPT Interviewer will review your resume and discuss your past experiences.
    - Press the microphone to start answering.
    - Each Interview will take 10 to 15 mins. 
    - Start introduce yourself and enjoy！ """)

position = st.selectbox("#### Select the position you are applying for", ["Data Analyst", "Software Engineer", "Marketing"])
resume = st.file_uploader("#### Upload your resume", type=["pdf"])

### -----------------------------------------------------------------------------------------------------------

### -----------------------------------------------------------------------------------------------------------
@dataclass
class Message:
    """Class for keeping track of interview history."""
    origin: Literal["human", "ai"]
    message: str

def save_vector(resume):

    pdf_reader = PdfReader(resume)

    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()

    # Split the document into chunks
    text_splitter = NLTKTextSplitter()
    texts = text_splitter.split_text(text)
    text_splitter = NLTKTextSplitter()
    texts = text_splitter.split_text(text)

    embeddings = OpenAIEmbeddings()
    docsearch = FAISS.from_texts(texts, embeddings)

    return docsearch

def load_css():
    with open("static/styles.css", "r") as f:
        css = f"<style>{f.read()}</style>"
        st.markdown(css, unsafe_allow_html=True)

def initialize_session_state():

    # convert resume to embeddings
    if 'docsearch' not in st.session_state:
        st.session_state.docserch = save_vector(resume)

    # retriever for resume screen
    if 'retriever' not in st.session_state:
        st.session_state.retriever = st.session_state.docserch.as_retriever(search_type="similarity")

    # prompt for retrieving information
    if 'chain_type_kwargs' not in st.session_state:
        st.session_state.chain_type_kwargs = prompt_sector(position, templates)

    # interview history
    if "resume_history" not in st.session_state:
        st.session_state.resume_history = []

    # token count
    if "token_count" not in st.session_state:
        st.session_state.token_count = 0

    # memory buffer for resume screen
    if "resume_memory" not in st.session_state:
        st.session_state.resume_memory = ConversationBufferMemory(human_prefix = "Candidate: ", ai_prefix = "Interviewer")

    # guideline for resume screen
    if "guideline" not in st.session_state:

        llm = ChatOpenAI(
        model_name = "gpt-3.5-turbo",
        temperature = 0.5,)

        st.session_state.guideline = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type_kwargs=st.session_state.chain_type_kwargs, chain_type='stuff',
            retriever=st.session_state.retriever, memory = st.session_state.resume_memory).run("Create an interview guideline and prepare only two questions for each topic. Make sure the questions tests the knowledge")

    # llm chain for resume screen
    if "resume_screen" not in st.session_state:

        llm = ChatOpenAI(
            model_name="gpt-3.5-turbo",
            temperature=0.7, )

        PROMPT = PromptTemplate(
            input_variables=["history", "input"],
            template= """I want you to act as an interviewer strictly following the guideline in the current conversation.
            
            Ask me questions and wait for my answers. Do not write explanations.
            
            Do ask follow-up questions if you think it's necessary.
            Do not ask the same question.
            Do not repeat the question.
            Do not ask too many questions at once.
            
            You name is GPTInterviewer.
            I want you to only reply as an interviewer.
            Do not write all the conversation at once. 
            
            Current Conversation:
            {history}
            
            Candidate: {input}
            AI: """)

        st.session_state.resume_screen =  ConversationChain(prompt=PROMPT, llm = llm, memory = st.session_state.resume_memory)

    # llm chain for generating feedback
    if "resume_feedback" not in st.session_state:

        llm = ChatOpenAI(
            model_name="gpt-3.5-turbo",
            temperature=0.5,)

        st.session_state.resume_feedback = ConversationChain(
            prompt=PromptTemplate(input_variables=["history","input"], template=templates.feedback_template),
            llm=llm,
            memory=st.session_state.resume_memory,
        )

### ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————

# sumitted job description
if position and resume:

    progress_text = "Loading..."
    my_bar = st.progress(0, text=progress_text)
    for percent_complete in range(100):
        time.sleep(0.02)
        my_bar.progress(percent_complete + 1, text=progress_text)

    # intialize session state
    initialize_session_state()
    load_css()
    st.markdown(st.session_state.guideline)

    if len(st.session_state.resume_history) < 11:

        chat_placeholder = st.container()
        answer_placeholder = st.container()
        credit_card_placeholder = st.empty()

        def answer_call_back():

            with get_openai_callback() as cb:
                # user input
                human_answer = st.session_state.answer
                # transcribe audio
                save_wav_file("temp/audio.wav", human_answer)
                input = transcribe("temp/audio.wav")
                # save human input to history
                st.session_state.resume_history.append(
                    Message("human", input)
                )

                # GPT Interviewer output and save to history
                llm_answer = st.session_state.resume_screen.run(input)
                # speech synthesis and speak out
                interviewer_answer = speech_synthesizer(llm_answer)
                # save audio data
                stream = AudioDataStream(interviewer_answer)
                # save audio data to history
                st.session_state.resume_history.append(
                    Message("ai", llm_answer)
                )
                st.session_state.token_count += cb.total_tokens

        with answer_placeholder:
            answer = audio_recorder(pause_threshold = 2, sample_rate = 44100)
            if answer:
                st.session_state['answer'] = answer
                answer_call_back()

        with chat_placeholder:
            for answer in st.session_state.resume_history:
                if answer:
                    div = f"""<div class="chat-row 
                                    {'' if answer.origin == 'ai' else 'row-reverse'}">
                                    <img class="chat-icon" src="static/images/{
                    'chat.png' if answer.origin == 'ai'
                    else 'user.png'}"
                                         width=32 height=32>
                                    <div class="chat-bubble
                                    {'ai-bubble' if answer.origin == 'ai' else 'human-bubble'}">
                                        &#8203;{answer.message}
                                    </div>
                                </div>
                                        """
                    st.markdown(div, unsafe_allow_html=True)

                for _ in range(3):
                    st.markdown("")

        credit_card_placeholder.caption(f"""
                Used {st.session_state.token_count} tokens \n
                You are on {(len(st.session_state.resume_history) / 11) ** 100}% of the wat to the end.""")
    # reaching the token limit
    else:
        conclusion = "Thank you for using GPTInterviewer. Please enter you email address to receive the report."
        conclusion = speech_synthesizer(conclusion)

        with st.form(key='my_form'):
            email = st.text_input("Email")
            submit = st.form_submit_button("Submit")

            if submit:
                # evaluation
                evaluation = st.session_state.resume_feedback.run("please give evalution regarding the interview")
                st.markdown(evaluation)

else:
    st.write("Please submit your resume and select desired position first.")