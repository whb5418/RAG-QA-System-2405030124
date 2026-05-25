import os
import tempfile
import streamlit as st
from document_processor import DocumentProcessor
from rag_core import RAGSystem


st.set_page_config(
    page_title="RAG智能问答系统",
    page_icon="🤖",
    layout="wide",
)


@st.cache_resource
def get_rag_system():
    return RAGSystem(
        llm_model="deepseek-r1:7b",
        embedding_model="nomic-embed-text",
        persist_directory="./chroma_db",
    )


@st.cache_resource
def get_doc_processor():
    return DocumentProcessor(chunk_size=1000, chunk_overlap=200)


def main():
    st.title("🤖 基于本地知识库的RAG智能问答系统")
    st.markdown("---")
    
    rag_system = get_rag_system()
    doc_processor = get_doc_processor()
    
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    if "kb_loaded" not in st.session_state:
        st.session_state.kb_loaded = False
    
    kb_info = rag_system.get_knowledge_base_info()
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("📁 文档管理")
        
        uploaded_files = st.file_uploader(
            "上传PDF、DOCX或TXT文档",
            type=["pdf", "docx", "txt"],
            accept_multiple_files=True,
        )
        
        if uploaded_files:
            st.success(f"已上传 {len(uploaded_files)} 个文件")
        
        if st.button("🔨 构建知识库", type="primary"):
            if not uploaded_files:
                st.warning("请先上传文档！")
            else:
                with st.spinner("正在处理文档..."):
                    all_chunks = []
                    for uploaded_file in uploaded_files:
                        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp_file:
                            tmp_file.write(uploaded_file.getvalue())
                            tmp_file_path = tmp_file.name
                        
                        try:
                            text = doc_processor.load_document(tmp_file_path)
                            chunks = doc_processor.split_text(text, uploaded_file.name)
                            all_chunks.extend(chunks)
                        finally:
                            os.unlink(tmp_file_path)
                    
                    if all_chunks:
                        rag_system.add_documents(all_chunks)
                        st.session_state.kb_loaded = True
                        st.success(f"✅ 知识库构建完成！添加了 {len(all_chunks)} 个文本块")
                        st.rerun()
                    else:
                        st.error("未能处理任何文档")
        
        st.markdown("---")
        st.subheader("📊 知识库状态")
        st.metric("文档数量", kb_info["document_count"])
        st.metric("文本块数量", kb_info["chunk_count"])
        
        if kb_info["document_names"]:
            with st.expander("查看文档列表"):
                for doc_name in kb_info["document_names"]:
                    st.write(f"- {doc_name}")
        
        st.markdown("---")
        if st.button("🗑️ 清空知识库"):
            rag_system.clear_knowledge_base()
            rag_system.clear_memory()
            st.session_state.messages = []
            st.session_state.kb_loaded = False
            st.success("知识库已清空")
            st.rerun()
        
        if st.button("🔄 清空对话历史"):
            rag_system.clear_memory()
            st.session_state.messages = []
            st.success("对话历史已清空")
            st.rerun()
    
    with col2:
        st.subheader("💬 问答交互")
        
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
                if "sources" in message:
                    with st.expander("📚 参考文档"):
                        for i, source in enumerate(message["sources"], 1):
                            st.markdown(f"**[{i}] {source['name']}**")
                            st.markdown(f"```\n{source['content']}\n```")
        
        if prompt := st.chat_input("请输入您的问题..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            
            with st.chat_message("user"):
                st.markdown(prompt)
            
            with st.chat_message("assistant"):
                with st.spinner("正在思考..."):
                    answer, source_docs = rag_system.ask(prompt)
                    st.markdown(answer)
                    
                    sources = []
                    if source_docs:
                        with st.expander("📚 参考文档"):
                            for i, doc in enumerate(source_docs, 1):
                                source_name = doc.metadata.get("source", "未知")
                                source_content = doc.page_content
                                sources.append({"name": source_name, "content": source_content})
                                st.markdown(f"**[{i}] {source_name}**")
                                st.markdown(f"```\n{source_content}\n```")
            
            st.session_state.messages.append({
                "role": "assistant",
                "content": answer,
                "sources": sources,
            })


if __name__ == "__main__":
    main()