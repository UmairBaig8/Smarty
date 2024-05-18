import streamlit as st
import openai
from streamlit_chat import message
from streamlit_extras.colored_header import colored_header
from streamlit_extras.add_vertical_space import add_vertical_space
from hugchat.login import Login

#os.getenv("OPENAI_API_KEY")
cookie_path_dir = "./cookies_snapshot"
try:
    # Load cookies when you restart your program:
    sign = Login("umairbaig808@gmail.com", None)
    cookies = sign.loadCookiesFromDir(cookie_path_dir) # This will detect if the JSON file exists, return cookies if it does and raise an Exception if it's not.
except:
    # Log in to huggingface and grant authorization to huggingchat
    sign = Login("umairbaig808@gmail.com", "xuwsy5-cenxin-dAnxyz")
    cookies = sign.login()

    # Save cookies to the local directory
    sign.saveCookiesToDir(cookie_path_dir)


# Sidebar contents
with st.sidebar:
    ## Streamlit APP
    st.title("Smarty | Your GenAI Companion!")
    st.subheader('Generative Q&A with AI')
    st.markdown('''
    ## About
    This app is an LLM-powered chatbot built using:
    - [Streamlit](https://streamlit.io/)
    - [OpenAI](https://platform.openai.com/playground/p/default-explain-code) OpenAI
    
    💡 Note: Add API key required!
    ''')
    add_vertical_space(5)
    openai_api_key = st.text_input("OpenAI API key", type="password")
    st.write('Made with ❤️ by Tushar & Umair')

if not openai_api_key:
    openai_api_key = st.secrets["OPENAI_API_KEY"]   
    
openai.api_key = openai_api_key

# Generate empty lists for generated and past.
## generated stores AI generated responses
if 'generated' not in st.session_state:
    st.session_state['generated'] = ["I'm Smarty, How may I help you?"]
## past stores User's questions
if 'past' not in st.session_state:
    st.session_state['past'] = ['Hi!']

# Layout of input/response containers
input_container = st.container()
colored_header(label='', description='', color_name='blue-30')
response_container = st.container()

# User input
## Function for taking user provided prompt as input
def get_text():
    input_text = st.text_input("You: ", "", key="input")
    return input_text
## Applying the user input box
with input_container:
    user_input = get_text()

# Response output
## Function for taking user prompt as input followed by producing AI generated responses
def generate_response(prompt):
  """Generates a response to the user's input."""

  response = openai.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
      {
        "role": "system",
        "content": "You will be provided with a piece of code, and your task is to explain it in a concise way line by line. With code examples if needed."
      },
      {
        "role": "user",
        "content": prompt
      },
      {
        "role": "assistant",
        "content": ""
      }
    ],
    temperature=0.3,
    max_tokens=1024,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
  )

  print(response)
  return response.choices[0].message.content.strip()
  ##return response["choices"][0]["message"]["content"]


## Conditional display of AI generated responses as a function of user provided prompts
with response_container:
    if user_input:
        response = generate_response(user_input)
        st.session_state.past.append(user_input)
        st.session_state.generated.append(response)
        
    if st.session_state['generated']:
        for i in range(len(st.session_state['generated'])):
            message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
            message(st.session_state["generated"][i], key=str(i))
