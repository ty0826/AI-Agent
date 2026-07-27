import time

import streamlit as st
from agent.react_agent import ReactAgent
st.title('智能客服')  # 标题
st.divider()  # 分割线

prompt = st.chat_input()  # 聊天框

if 'agent' not in st.session_state:
    st.session_state['agent'] = ReactAgent()

if 'history_message' not in st.session_state:
    st.session_state['history_message'] = []

for message in st.session_state['history_message']:
    st.chat_message(message['role']).write(message['content'])

if prompt:
    st.chat_message('user').write(prompt)
    st.session_state['history_message'].append({'role': 'user', 'content': prompt})
    res_message=[]
    with st.spinner("智能客服思考中......"):
        res_stream = st.session_state['agent'].execult_stream(prompt)

        def capture(generator,cache_list):
            for chunk in generator:
                cache_list.append(chunk)
                for i in chunk:
                    time.sleep(0.01)
                    yield i

        st.chat_message('assistant').write_stream(capture(res_stream,res_message))
        st.session_state['history_message'].append({'role': 'assistant', 'content': res_message[-1]})
        st.rerun()
