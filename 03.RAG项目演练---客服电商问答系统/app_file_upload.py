####用户上传知识库web页面
import time
import streamlit as st
from knowledge_base import KnowledgeService

# st添加标题
st.title('知识库更新服务')

# file_opload
file_data = st.file_uploader(
    '请上传文件',
    type=['txt'],
    accept_multiple_files=False  # 表示仅接受一个文件
)
# 因为streamlit的机制，刷新页面或者web页面得dom结构发生改变时都会导致页面重新加载
if 'service' not in st.session_state:
    st.session_state['service'] = KnowledgeService()

if file_data is not None:
    file_name = file_data.name
    file_type = file_data.type
    file_size = file_data.size / 1024  # 原来单位是B，转成KB

    st.subheader(file_name)
    st.write(f"格式：{file_type}| 大小：{file_size:.2f}KB")

    text = file_data.getvalue().decode('utf-8')
    with st.spinner("载入知识中"):
        time.sleep(1)
        result = st.session_state['service'].upload_by_str(text, file_name)
        st.write(result)
