import os
from typing import List, Tuple

try:
    from langchain_ollama import OllamaLLM, OllamaEmbeddings
except ImportError:
    from langchain_community.llms import Ollama as OllamaLLM
    from langchain_community.embeddings import OllamaEmbeddings

from langchain_community.vectorstores import Chroma
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate


class RAGSystem:
    def __init__(
        self,
        llm_model: str = "deepseek-r1:7b",
        embedding_model: str = "nomic-embed-text",
        persist_directory: str = "./chroma_db",
    ):
        self.llm_model = llm_model
        self.embedding_model = embedding_model
        self.persist_directory = persist_directory
        
        self.embeddings = OllamaEmbeddings(model=embedding_model)
        self.llm = OllamaLLM(model=llm_model)
        self.vectorstore = None
        self.chain = None
        self.memory = None
        
        self._init_vectorstore()

    def _init_vectorstore(self):
        if os.path.exists(self.persist_directory):
            try:
                self.vectorstore = Chroma(
                    persist_directory=self.persist_directory,
                    embedding_function=self.embeddings,
                )
            except Exception as e:
                print(f"加载向量数据库失败: {e}")
                self.vectorstore = None

    def add_documents(self, documents: List):
        if not self.vectorstore:
            self.vectorstore = Chroma.from_documents(
                documents=documents,
                embedding=self.embeddings,
                persist_directory=self.persist_directory,
            )
        else:
            self.vectorstore.add_documents(documents)
        
        self.vectorstore.persist()
        self._init_chain()

    def retrieve_documents(self, query: str, k: int = 3) -> List:
        if not self.vectorstore:
            return []
        docs = self.vectorstore.similarity_search(query, k=k)
        return docs

    def _init_chain(self):
        if not self.vectorstore:
            return
        
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True,
            output_key="answer",
        )
        
        prompt_template = """你是一个基于知识库的智能问答助手。请基于提供的参考文档回答用户的问题。

参考文档：
{context}

用户问题：
{question}

回答要求：
1. 请基于参考文档中的内容进行回答
2. 如果参考文档中没有相关信息，请明确说"文档中未找到相关答案"
3. 回答要准确、简洁、有条理

回答："""
        
        PROMPT = PromptTemplate(
            template=prompt_template,
            input_variables=["context", "question"],
        )
        
        self.chain = ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            retriever=self.vectorstore.as_retriever(search_kwargs={"k": 3}),
            memory=self.memory,
            combine_docs_chain_kwargs={"prompt": PROMPT},
            return_source_documents=True,
        )

    def ask(self, question: str) -> Tuple[str, List]:
        if not self.chain:
            return "知识库尚未构建，请先上传文档。", []
        
        result = self.chain({"question": question})
        answer = result["answer"]
        source_docs = result.get("source_documents", [])
        return answer, source_docs

    def clear_memory(self):
        if self.memory:
            self.memory.clear()

    def get_knowledge_base_info(self) -> dict:
        if not self.vectorstore:
            return {"document_count": 0, "chunk_count": 0}
        
        collection = self.vectorstore._collection
        chunk_count = collection.count()
        
        sources = set()
        if chunk_count > 0:
            results = collection.get()
            for metadata in results.get("metadatas", []):
                if "source" in metadata:
                    sources.add(metadata["source"])
        
        return {
            "document_count": len(sources),
            "chunk_count": chunk_count,
            "document_names": list(sources),
        }

    def clear_knowledge_base(self):
        if os.path.exists(self.persist_directory):
            import shutil
            shutil.rmtree(self.persist_directory)
        self.vectorstore = None
        self.chain = None
        self.memory = None