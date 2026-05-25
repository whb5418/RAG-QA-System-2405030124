from document_processor import DocumentProcessor
from rag_core import RAGSystem


def main():
    print("=" * 50)
    print("RAG智能问答系统 - 命令行版本")
    print("=" * 50)
    
    doc_processor = DocumentProcessor(chunk_size=1000, chunk_overlap=200)
    rag_system = RAGSystem(
        llm_model="deepseek-r1:7b",
        embedding_model="nomic-embed-text",
        persist_directory="./chroma_db",
    )
    
    print("\n正在加载示例文档...")
    docs_dir = "./docs"
    chunks = doc_processor.process_documents_from_directory(docs_dir)
    
    if chunks:
        print(f"✅ 成功处理 {len(chunks)} 个文本块")
        rag_system.add_documents(chunks)
        
        kb_info = rag_system.get_knowledge_base_info()
        print(f"知识库信息：文档数={kb_info['document_count']}, 文本块数={kb_info['chunk_count']}")
    else:
        print("⚠️ 未找到可处理的文档")
    
    print("\n" + "=" * 50)
    print("开始问答（输入 'quit' 或 'exit' 退出）")
    print("=" * 50)
    
    while True:
        question = input("\n请输入问题: ").strip()
        
        if question.lower() in ["quit", "exit", "退出"]:
            print("👋 再见！")
            break
        
        if not question:
            continue
        
        print("\n正在思考...")
        answer, source_docs = rag_system.ask(question)
        
        print(f"\n💡 答案: {answer}")
        
        if source_docs:
            print(f"\n📚 参考文档 ({len(source_docs)} 个):")
            for i, doc in enumerate(source_docs, 1):
                source = doc.metadata.get("source", "未知")
                snippet = doc.page_content[:150] + "..." if len(doc.page_content) > 150 else doc.page_content
                print(f"\n  [{i}] 来源: {source}")
                print(f"      片段: {snippet}")


if __name__ == "__main__":
    main()