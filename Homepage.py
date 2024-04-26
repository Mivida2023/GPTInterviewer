import streamlit as st
from streamlit_option_menu import option_menu
from app_utils import switch_page
import streamlit as st
from PIL import Image

im = Image.open("icon.png")
st.set_page_config(page_title = "Mivida Recruteur", layout = "centered",page_icon=im)

lan = st.selectbox("#### Language", ["Français", "English"])

if lan == "Français":
    home_title = "Mivida Recruteur IA"
    home_introduction = "Bienvenue chez Mivida Recruteur IA, renforçant votre préparation aux entretiens grâce à l'IA générative."
    with st.sidebar:
        st.markdown('Mivida Recruteur IA - V0.1.0')
        st.markdown(""" 
        #### Propulsé par
    
        [Ollama](https://ollama.com/)
    
        [FAISS](https://github.com/facebookresearch/faiss)
    
        [Langchain](https://github.com/hwchase17/langchain)
    
                    """)
    st.markdown(
        "<style>#MainMenu{visibility:hidden;}</style>",
        unsafe_allow_html=True
    )
    st.image(im, width=100)
    st.markdown(f"""# {home_title} <span style=color:#2E9BF5><font size=5>Beta</font></span>""", unsafe_allow_html=True)
    st.markdown("""\n""")
    #st.markdown("#### Salutations")
    st.markdown("Bienvenue chez Mivida Recruteur IA ! 👏 Mivida Recruteur IA est votre intervieweur personnel alimenté par une IA générative qui conduit des entretiens simulés."
                "Vous pouvez télécharger votre CV et saisir des descriptions de postes, et Mivida Recruteur IA vous posera des questions personnalisées. De plus, vous pouvez configurer votre propre Intervieweur !")
    st.markdown("""\n""")
    with st.expander("Quoi de neuf prochainement ?"):
        st.write("""
        Interaction vocale améliorée pour une expérience sans accroc. """)
    st.markdown("""\n""")
    st.markdown("#### Pour commencer !")
    st.markdown("Sélectionnez l'un des écrans suivants pour commencer votre entretien !")
    selected = option_menu(
            menu_title= None,
            options=["Professionnel", "CV", "Compétences"],
            icons = ["cast", "cloud-upload", "cast"],
            default_index=0,
            orientation="horizontal",
        )
    if selected == 'Professionnel':
        st.info("""
            📚Dans cette session, Mivida Recruteur IA évaluera vos compétences techniques en rapport avec la description du poste.
            Remarque : La longueur maximale de votre réponse est de 4097 jetons !
            - Chaque entretien durera de 10 à 15 minutes.
            - Pour commencer une nouvelle session, rafraîchissez simplement la page.
            - Choisissez votre style d'interaction préféré (chat/voix)
            - Présentez-vous et profitez-en ! """)
        if st.button("Commencer l'Entretien !"):
            switch_page("Écran Professionnel")
    if selected == 'CV':
        st.info("""
        📚Dans cette session, Mivida Recruteur IA passera en revue votre CV et discutera de vos expériences passées.
        Remarque : La longueur maximale de votre réponse est de 4097 jetons !
        - Chaque entretien durera de 10 à 15 minutes.
        - Pour commencer une nouvelle session, rafraîchissez simplement la page.
        - Choisissez votre style d'interaction préféré (chat/voix)
        - Présentez-vous et profitez-en ! """
        )
        if st.button("Commencer l'Entretien !"):
            switch_page("Écran CV")
    if selected == 'Compétences':
        st.info("""
        📚Dans cette session, Mivida Recruteur IA évaluera vos compétences Compétenceses en rapport avec la description du poste.
        Remarque : La longueur maximale de votre réponse est de 4097 jetons !
        - Chaque entretien durera de 10 à 15 minutes.
        - Pour commencer une nouvelle session, rafraîchissez simplement la page.
        - Choisissez votre style d'interaction préféré (chat/voix)
        - Présentez-vous et profitez-en ! 
        """)
        if st.button("Commencer l'Entretien !"):
            switch_page("Écran Compétences")



if lan == "English":
    home_title = " Mivida Recruit Agent"
    home_introduction = "Welcome to  Mivida Recruit Agent, empowering your interview preparation with generative AI."
    with st.sidebar:
        st.markdown('Mivida Recruteur IA - V0.1.0')
        st.markdown(""" 
    
        #### Powered by
    
        [OLllama](https://ollama.com/)
    
        [FAISS](https://github.com/facebookresearch/faiss)
    
        [Langchain](https://github.com/hwchase17/langchain)
    
                    """)
    st.markdown(
        "<style>#MainMenu{visibility:hidden;}</style>",
        unsafe_allow_html=True
    )
    st.image(im, width=100)
    st.markdown(f"""# {home_title} <span style=color:#2E9BF5><font size=3>Beta</font></span>""",unsafe_allow_html=True)
    st.markdown("""\n""")
    #st.markdown("#### Greetings")
    st.markdown("Welcome to  Mivida Recruit Agent! 👏  Mivida Recruit Agent is your personal interviewer powered by generative AI that conducts mock interviews."
                "You can upload your resume and enter job descriptions, and  Mivida Recruit Agent will ask you customized questions. Additionally, you can configure your own Interviewer!")
    st.markdown("""\n""")
    with st.expander("Updates"):
        st.write("""
        08/13/2023
        - Fix the error that occurs when the user input fails to be recorded. """)
    with st.expander("What's coming next?"):
        st.write("""
        Improved voice interaction for a seamless experience. """)
    st.markdown("""\n""")
    st.markdown("#### Get started!")
    st.markdown("Select one of the following screens to start your interview!")
    selected = option_menu(
            menu_title= None,
            options=["Professional", "Resume", "Behavioral"],
            icons = ["cast", "cloud-upload", "cast"],
            default_index=0,
            orientation="horizontal",
        )
    if selected == 'Professional':
        st.info("""
            📚In this session,  Mivida Recruit Agent will assess your technical skills as they relate to the job description.
            Note: The maximum length of your answer is 4097 tokens!
            - Each Interview will take 10 to 15 mins.
            - To start a new session, just refresh the page.
            - Choose your favorite interaction style (chat/voice)
            - Start introduce yourself and enjoy！ """)
        if st.button("Start Interview!"):
            switch_page("Professional Screen")
    if selected == 'Resume':
        st.info("""
        📚In this session,  Mivida Recruit Agent will review your resume and discuss your past experiences.
        Note: The maximum length of your answer is 4097 tokens!
        - Each Interview will take 10 to 15 mins.
        - To start a new session, just refresh the page.
        - Choose your favorite interaction style (chat/voice)
        - Start introduce yourself and enjoy！ """
        )
        if st.button("Start Interview!"):
            switch_page("Resume Screen")
    if selected == 'Behavioral':
        st.info("""
        📚In this session,  Mivida Recruit Agent will assess your soft skills as they relate to the job description.
        Note: The maximum length of your answer is 4097 tokens!
        - Each Interview will take 10 to 15 mins.
        - To start a new session, just refresh the page.
        - Choose your favorite interaction style (chat/voice)
        - Start introduce yourself and enjoy！ 
        """)
        if st.button("Start Interview!"):
            switch_page("Behavioral Screen")
    st.markdown("""\n""")