import streamlit as st
from rag import RagService
import config_data as config

st.title('智能客服')  # 标题
st.divider()  # 分割线

prompt = st.chat_input()  # 聊天框

if 'org' not in st.session_state:
    st.session_state['org'] = RagService()

if 'history_message' not in st.session_state:
    st.session_state['history_message'] = []

for message in st.session_state['history_message']:
    st.chat_message(message['role']).write(message['content'])

if prompt:
    st.chat_message('user').write(prompt)
    st.session_state['history_message'].append({'role': 'user', 'content': prompt})
    with st.spinner("AI思考中......"):
        res_stream = st.session_state['org'].chain.stream({'input': prompt}, config.session_config)
        res = st.chat_message('assistant').write_stream(res_stream)
        st.session_state['history_message'].append({'role': 'assistant', 'content': res})
