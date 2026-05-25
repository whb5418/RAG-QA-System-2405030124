# RAG-QA-System

## 项目简介

这是一个基于本地知识库的RAG（检索增强生成）智能问答系统，使用Ollama本地大模型、LangChain框架和Streamlit开发工具构建，支持对上传的PDF、DOCX和TXT文档进行智能问答。

## 环境要求与安装步骤

### Python版本
- Python 3.9 或更高版本

### 依赖库安装
```bash
pip install -r requirements.txt
```

### Ollama安装
1. 访问 [Ollama官网](https://ollama.com/) 下载并安装Windows版本
2. 打开终端，运行以下命令下载模型：
   ```bash
   ollama pull deepseek-r1:7b
   ollama pull nomic-embed-text
   ```

### 验证Ollama服务
确保Ollama服务正在运行（默认端口：http://localhost:11434）
- 运行测试脚本验证连接：`python test_ollama.py`

## 使用说明

### 运行Web应用
```bash
streamlit run app.py
```
或双击 `run_app.bat` 批处理文件

### 上传文档
1. 在网页界面点击"浏览文件"或拖拽文件到上传区域
2. 支持PDF、DOCX和TXT格式
3. 点击"构建知识库"按钮处理文档

### 提问
1. 在输入框中输入问题
2. 点击"提问"按钮获取答案
3. 系统会显示对话历史和参考文档

### 命令行版本
```bash
python cli_rag.py
```

## 关键技术点说明

### RAG流程
1. **文档加载**：加载PDF、DOCX和TXT文档
2. **文本分块**：使用RecursiveCharacterTextSplitter（chunk_size=1000, chunk_overlap=200）
3. **向量化存储**：使用Ollama的nomic-embed-text嵌入模型，存入Chroma向量数据库
4. **相似性检索**：查询时检索最相关的3个文本块
5. **答案生成**：基于检索到的文档内容，使用DeepSeek-R1模型生成答案

### 所用模型
- **大语言模型**：deepseek-r1:7b（或qwen2:7b）
- **嵌入模型**：nomic-embed-text

### 系统提示词设计
```
你是一个基于知识库的智能问答助手。请基于提供的参考文档回答用户的问题。

参考文档：
{context}

用户问题：
{question}

回答要求：
1. 请基于参考文档中的内容进行回答
2. 如果参考文档中没有相关信息，请明确说"文档中未找到相关答案"
3. 回答要准确、简洁、有条理
```

## 项目结构

```
RAG-QA-System/
├── app.py                 # Streamlit Web应用主文件
├── rag_core.py            # RAG核心功能模块
├── document_processor.py  # 文档处理模块
├── cli_rag.py             # 命令行版本RAG系统
├── test_ollama.py         # Ollama测试脚本
├── build.py               # PyInstaller打包配置
├── run_app.bat            # Windows启动脚本
├── requirements.txt       # 依赖包列表
├── README.md              # 项目说明
├── .gitignore             # Git忽略文件配置
├── AI使用日志.md          # AI开发记录
└── docs/                  # 示例文档目录
    ├── nlp_intro.txt      # 自然语言处理技术简介
    ├── transformer.txt    # Transformer模型详解
    ├── rag_tech.txt       # RAG检索增强生成技术
    ├── llm_intro.txt      # 大语言模型简介
    └── vector_db.txt      # 向量数据库技术
```

## 功能特性

- ✅ 文档上传（PDF、DOCX、TXT）
- ✅ 知识库构建
- ✅ 智能问答
- ✅ 对话历史显示
- ✅ 参考文档展示
- ✅ 知识库状态显示
- ✅ 会话记忆功能
- ✅ 清空知识库
- ✅ 清空对话历史

## 测试示例

**相关问题：**
1. 什么是自然语言处理？
2. Transformer模型的核心组件有哪些？
3. RAG技术的优势是什么？
4. 大语言模型有哪些应用场景？
5. 常用的向量数据库有哪些？

**无关问题（应返回"文档中未找到相关答案"）：**
1. 今天天气怎么样？
2. 如何做红烧肉？

## 打包成EXE

```bash
pip install pyinstaller
python build.py
```

## 已知问题与改进方向

- 可增加对更多文档格式的支持（如Markdown等）
- 可增加夜间模式切换功能
- 可增加批量上传和问答记录导出功能
- 可优化分块策略和检索算法以提高回答质量

## 注意事项

- 确保Ollama服务正在运行
- 首次运行时需要下载模型（约10GB）
- 知识库数据存储在 `./chroma_db` 目录
- 建议使用GPU加速（需NVIDIA GPU）