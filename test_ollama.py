try:
    from langchain_ollama import OllamaLLM, OllamaEmbeddings
except ImportError:
    from langchain_community.llms import Ollama as OllamaLLM
    from langchain_community.embeddings import OllamaEmbeddings


def test_ollama_connection():
    print("正在测试Ollama连接...")
    
    try:
        llm = OllamaLLM(model="deepseek-r1:7b")
        response = llm.invoke("你好，请用一句话介绍自己。")
        print("✅ Ollama大模型连接成功！")
        print(f"模型回复: {response}")
    except Exception as e:
        print(f"❌ Ollama大模型连接失败: {e}")
        print("请确保Ollama服务正在运行，并且已下载deepseek-r1:7b模型。")
        print("安装Ollama: https://ollama.com/")
        print("下载模型: ollama pull deepseek-r1:7b")
        return False
    
    try:
        embeddings = OllamaEmbeddings(model="nomic-embed-text")
        test_text = "这是一个测试文本。"
        embedding = embeddings.embed_query(test_text)
        print("\n✅ Ollama嵌入模型连接成功！")
        print(f"嵌入向量维度: {len(embedding)}")
    except Exception as e:
        print(f"\n❌ Ollama嵌入模型连接失败: {e}")
        print("请确保已下载nomic-embed-text模型。")
        print("下载模型: ollama pull nomic-embed-text")
        return False
    
    print("\n🎉 Ollama测试全部通过！")
    return True


if __name__ == "__main__":
    test_ollama_connection()