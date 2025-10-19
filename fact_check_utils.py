"""
Fact-Check 工具 - 智能摘要和验证
结合知识库检索和可选的网络搜索，生成总结性文本
"""

import os
from langchain_community.llms import Tongyi
from dotenv import load_dotenv

load_dotenv()

def get_friendly_filename(source_file):
    """
    Convert technical source file names to user-friendly names
    """
    filename_mapping = {
        # Your Excel mappings
    '37_3_Adamantopoulou.pdf': 'Adamantopoulou et al 2011 - Movements of Mediterranean Monk Seals Monachus monachus in the Eastern Mediterranean Sea',
    'f0da61e8b1bd28b4546f409830e6ddd18257.pdf': 'Simopoulos et al 2013 - Social values of biodiversity conservation for Mediterranean monk seal Monachus monachus',
    'E-AC33-45-04.pdf': 'CITES Animals Committee 2024 - Periodic Review of Monachus tropicalis',
    '278-282-Vol19No2Erdem.pdf': 'Danyer et al 2013 - Preliminary report of a stranding case of Mediterranean Monk Seal Monachus monachus on Antalya coast Turkey',
    'Cave_habitats_used_by_Mediterranean_monk.pdf': 'Bundone 2010 - Cave habitats used by Mediterranean monk seals Monachus monachus in Sardinia',
    'the-mediterranean-monk-seal.pdf': 'Van Wijngaarden 1962 - The Mediterranean Monk Seal',
    'a-brief-note-on-mediterranean-monk-seal.pdf': 'Zareei 2021 - A Brief Note on Mediterranean Monk Seal',
    's41598-020-79712-1.pdf': 'Karamanlidis et al 2021 - Genetic and demographic history define a conservation strategy for earths most endangered pinniped the Mediterranean monk seal Monachus monachus',
    '2020 A Mediterranean Monk Seal Pup on the Apulian Coast (Southern Italy) Sign of an Ongoing Recolonisation.pdf': 'Fioravanti et al 2020 - A Mediterranean Monk Seal Pup on the Apulian Coast Southern Italy Sign of an Ongoing Recolonisation',
    'reestablishment_of_the_mediterranean_monk_seal_monachus_monachus_in_cyprus_priorities_for_conservation.pdf': 'Nicolaou et al 2021 - Re-establishment of the Mediterranean monk seal Monachus monachus in Cyprus priorities for conservation',
    'MA2379_lit180815.pdf': 'Mo et al 2004 - Habitat suitability and sightings of the Mediterranean monk seal in the National Park of Al Hoceima Morocco',
    'a4-flyer_270x194_marine-lifemonk-seal_eng_final.pdf': 'PPNEA undated - Mediterranean Monk Seal conservation flyer',
    '2013_Karamanlidisetal..pdf': 'Karamanlidis et al 2013 - Demographic Structure and Social Behavior of the Unique Mediterranean monk seal Monachus monachus colony of the Island of Gyaros',
    'Ilaria_Gradella.pdf': 'Gradella 2024 - The Mediterranean Monk Seal Monachus monachus Distribution Stranding and Major Threats',
    'mededelingen39_2008b.pdf': 'Johnson 2004 - Monk Seals in Post-Classical History Biography of the Mediterranean Monk Seal',
    '37_3_Adamantopoulou.pdf': 'Adamantopoulou et al 2010 - Movements of Mediterranean Monk Seals Monachus monachus in the Eastern Mediterranean Sea',
    'n045p315.pdf': 'Fernandez de Larrinoa et al 2021 - Age specific survival and reproductive rates of Mediterranean monk seals at the Cabo Blanco Peninsula West Africa',
    'AM-39.1-Alfaghi.pdf': 'Alfaghi et al 2013 - First Confirmed Sighting of the Mediterranean Monk Seal Monachus monachus in Libya Since 1972',
    'n053p341.pdf': 'Karamanlidis et al 2024 - Current status biology threats and conservation priorities of the Vulnerable Mediterranean monk seal',
    '44219.pdf': 'Bundone et al 2024 - Monitoring the Mediterranean monk seal in the central Mediterranean Sea',
    'guide.pdf': 'Johnson et al 1998 - The Mediterranean Monk Seal Conservation Guidelines',
    'the-mediterranean-monk-seal-karamanlidis-et-al-2015.pdf': 'Karamanlidis et al 2015 - The Mediterranean monk seal Monachus monachus status biology threats and conservation priorities',
    'strategie_phoque_en.pdf': 'UNEP-MAP SPA-RAC 2019 - Regional Strategy for the Conservation of Monk Seal in the Mediterranean',
    '2025-006-En.pdf': 'Quintana Martin-Montalvo et al 2025 - Mediterranean monk seal Monachus monachus A comprehensive set of monitoring and research techniques',
    'BDJ_article_120201.pdf': 'Valsecchi et al 2024 - An Observatory to monitor range extension of the Mediterranean monk seal based on its eDNA traces',
    'noaa_66431_DS1.pdf': 'Parsons 2024 - Mediterranean monk seal Monachus monachus 5 Year Review Summary and Evaluation',
        
        # Default fallback
        'unknown': 'Unknown Document'
    }
    
    base_name = os.path.basename(source_file) if source_file else 'unknown'
    return filename_mapping.get(base_name, base_name.replace('_', ' ').replace('-', ' ').title())


def summarize_fact_check(question, retrieved_docs, ai_answer, language="English"):
    """
    对 Fact-Check 内容进行智能摘要
    
    Args:
        question: 用户问题
        retrieved_docs: 检索到的文档列表
        ai_answer: AI 的回答
        language: 语言（English/Portuguese）
    
    Returns:
        str: 总结性文本
    """
    # 提取文档内容
    doc_contents = []
    sources = []
    
    for i, doc in enumerate(retrieved_docs[:3], 1):  # 最多使用3个文档
        content = doc.page_content[:500]  # 每个文档最多500字符
        source = doc.metadata.get('source_file', 'Unknown')
        page = doc.metadata.get('page', 'N/A')

        friendly_name = get_friendly_filename(source)
        
        doc_contents.append(f"[Source {i}: {friendly_name}, Page {page}]\n{content}")
        sources.append(f"{friendly_name} (p.{page})")
    
    combined_docs = "\n\n".join(doc_contents)
    
    # 构建摘要 Prompt
    if language == "Portuguese":
        prompt = f"""
        Tu és um verificador de factos científico. Com base nos documentos fornecidos, cria um resumo claro e conciso.

        **Pergunta do utilizador:** {question}

        **Resposta da IA:** {ai_answer}

        **Documentos de referência:**
        {combined_docs}

        **Tua tarefa:**
        1. Resume os pontos-chave dos documentos que apoiam a resposta
        2. Menciona dados específicos (números, locais, datas) se disponíveis
        3. Mantém o resumo abaixo de 100 palavras
        4. Usa linguagem simples e clara
        5. Se os documentos não apoiam a resposta, indica isso

        **Resumo factual:**
        """
    else:
        prompt = f"""
        You are a scientific fact-checker. Based on the provided documents, create a clear and concise summary.

        **User's Question:** {question}

        **AI's Answer:** {ai_answer}

        **Reference Documents:**
        {combined_docs}

        **Your Task:**
        1. Summarize key points from the documents that support the answer
        2. Mention specific data (numbers, locations, dates) if available
        3. Keep the summary under 100 words
        4. Use simple, clear language
        5. If documents don't support the answer, indicate that

        **Factual Summary:**
        """
    
    # 使用 Qwen LLM 生成摘要
    try:
        api_key = os.getenv("DASHSCOPE_API_KEY")
        llm = Tongyi(
            model_name=os.getenv("QWEN_MODEL_NAME", "qwen-turbo"),
            temperature=0.3,  # 较低温度，确保事实性
            dashscope_api_key=api_key
        )
        
        summary = llm.invoke(prompt)
        
        # 添加来源引用
        if language == "Portuguese":
            source_text = f"\n\n📚 **Fontes:** {', '.join(sources)}"
        else:
            source_text = f"\n\n📚 **Sources:** {', '.join(sources)}"
        
        return summary.strip() + source_text
    
    except Exception as e:
        print(f"[Fact-Check] 摘要生成失败: {str(e)}")
        # 降级：返回简化的文档内容
        source = retrieved_docs[0].metadata.get('source_file', 'Unknown')
        page = retrieved_docs[0].metadata.get('page', 'N/A')
        friendly_name = get_friendly_filename(source)
        
        if language == "Portuguese":
            return f"📄 Informação extraída dos documentos:\n\n{retrieved_docs[0].page_content[:200]}...\n\n📚 Fonte: {friendly_name} (p.{page})"
        else:
            return f"📄 Information from documents:\n\n{retrieved_docs[0].page_content[:200]}...\n\n📚 Source: {friendly_name} (p.{page})"


def optimize_search_query(question, retrieved_docs):
    """
    基于用户问题和 RAG 检索内容优化搜索查询
    
    Args:
        question: 用户原始问题
        retrieved_docs: RAG 检索到的文档
    
    Returns:
        str: 优化后的搜索查询
    """
    # 从 RAG 文档中提取关键概念
    rag_keywords = set()
    for doc in retrieved_docs[:2]:  # 只看前2个最相关的文档
        content = doc.page_content.lower()
        # 提取关键生物学/保护相关词汇
        bio_keywords = ['monk seal', 'mediterranean monk seal', 'seal', 'endemic', 'madeira', 'conservation', 
                        'endangered', 'breeding', 'pup', 'habitat', 'species', 'population', 'marine',
                        'monachus', 'monachus monachus', 'coastal', 'ocean', 'marine mammal']
        for keyword in bio_keywords:
            if keyword in content:
                rag_keywords.add(keyword)
    
    # 构建精准搜索查询
    base_query = "Mediterranean monk seal"
    
    # 添加相关上下文关键词
    if 'conservation' in rag_keywords or 'endangered' in rag_keywords:
        base_query += " conservation status"
    elif 'breeding' in rag_keywords or 'nesting' in rag_keywords:
        base_query += " breeding habitat"
    elif 'madeira' in rag_keywords:
        base_query += " Madeira island"
    else:
        base_query += " marine mammal biology"
    
    # 添加英文关键词确保搜索质量
    base_query += " seal species"
    
    return base_query



def filter_search_results(results, question):
    """
    智能过滤搜索结果，排除无关内容
    
    Args:
        results: 原始搜索结果列表
        question: 用户问题
    
    Returns:
        list: 过滤后的相关结果
    """
    filtered = []
    
    # 相关关键词（生物学/保护相关）
    relevant_keywords = [
        'monk seal', 'seal', 'marine mammal', 'species', 'madeira', 'conservation', 
        'endangered', 'breeding', 'habitat', 'marine biology', 'wildlife',
        'monachus', 'mediterranean', 'endemic', 'biodiversity', 'coastal',
        'pup', 'colony', 'protected', 'marine', 'ocean'
    ]
    
    # 无关关键词（技术/编程相关）
    irrelevant_keywords = [
        'framework', 'programming', 'code', 'software', 'api', 'rust',
        '编程', '框架', '开发', '代码', 'github', 'npm', 'cargo'
    ]
    
    for result in results:
        title = result.get('title', '').lower()
        body = result.get('body', '').lower()
        combined = title + ' ' + body
        
        # 检查是否包含无关关键词
        has_irrelevant = any(keyword in combined for keyword in irrelevant_keywords)
        if has_irrelevant:
            print(f"[Fact-Check] 过滤无关结果: {result.get('title', 'Unknown')[:50]}...")
            continue
        
        # 检查是否包含相关关键词
        has_relevant = any(keyword in combined for keyword in relevant_keywords)
        if has_relevant:
            filtered.append(result)
    
    return filtered


def web_search_supplement(question, retrieved_docs=None, language="English"):
    """
    智能网络搜索补充信息
    支持 DuckDuckGo（免费）和 Tavily（需 API Key）
    
    Args:
        question: 用户问题
        retrieved_docs: RAG 检索到的文档（用于优化搜索查询）
        language: 语言
    
    Returns:
        str: 网络搜索结果摘要（如果启用）
    """
    # 检查是否启用网络搜索
    use_web_search = os.getenv("USE_WEB_SEARCH", "false").lower() == "true"
    
    if not use_web_search:
        return None
    
    # 优化搜索查询（基于 RAG 上下文）
    if retrieved_docs and len(retrieved_docs) > 0:
        optimized_query = optimize_search_query(question, retrieved_docs)
        print(f"[Fact-Check] 优化搜索查询: {optimized_query}")
    else:
        optimized_query = f"Mediterranean monk seal {question} marine mammal"
    
    # 获取搜索提供商（默认 duckduckgo）
    provider = os.getenv("WEB_SEARCH_PROVIDER", "duckduckgo").lower()
    
    # 方案 1: DuckDuckGo（完全免费，无需 API Key）
    results = []  # 初始化 results 变量
    
    if provider == "duckduckgo":
        try:
            from ddgs import DDGS
            
            # 使用新版 API（无需 context manager）
            ddgs = DDGS()
            # 新版 API：参数名是 query 而不是 keywords
            raw_results = list(ddgs.text(
                query=optimized_query,
                max_results=5  # 多获取一些结果，后续过滤
            ))
            
            # 智能过滤结果
            results = filter_search_results(raw_results, question)
            print(f"[Fact-Check] 原始结果: {len(raw_results)} → 过滤后: {len(results)}")
            
            if results:
                if language == "Portuguese":
                    summary = "🌐 **Informação da Internet:**\n\n"
                else:
                    summary = "🌐 **Internet Information:**\n\n"
                
                # 只显示前2个最相关的结果
                for i, result in enumerate(results[:2], 1):
                    title = result.get('title', 'Unknown')
                    body = result.get('body', '')[:150]
                    url = result.get('href', '')
                    
                    summary += f"{i}. **{title}**\n   {body}...\n   🔗 {url}\n\n"
                
                return summary.strip()
        
        except ImportError:
            print("[Fact-Check] DDGS 未安装，运行: pip install ddgs")
        except Exception as e:
            print(f"[Fact-Check] DuckDuckGo 搜索失败: {str(e)}")
            print(f"[Fact-Check] 尝试降级到 Tavily...")
    
    # 方案 2: Tavily（需要 API Key，1000 次/月免费）
    # 如果 DuckDuckGo 失败或提供商设置为 tavily，尝试 Tavily
    if provider == "tavily" or (provider == "duckduckgo" and len(results) == 0):
        try:
            tavily_key = os.getenv("TAVILY_API_KEY")
            if tavily_key and tavily_key != "tvly-your-api-key":
                from tavily import TavilyClient
                
                client = TavilyClient(api_key=tavily_key)
                response = client.search(
                    query=f"Mediterranean monk seal {question}",
                    max_results=2,
                    search_depth="basic"
                )
                
                if response and 'results' in response:
                    results = response['results'][:2]
                    
                    if language == "Portuguese":
                        summary = "🌐 **Informação da Internet:**\n\n"
                    else:
                        summary = "🌐 **Internet Information:**\n\n"
                    
                    for i, result in enumerate(results, 1):
                        title = result.get('title', 'Unknown')
                        content = result.get('content', '')[:150]
                        url = result.get('url', '')
                        
                        summary += f"{i}. **{title}**\n   {content}...\n   🔗 {url}\n\n"
                    
                    return summary.strip()
        
        except ImportError:
            print("[Fact-Check] Tavily 未安装，运行: pip install tavily-python")
        except Exception as e:
            print(f"[Fact-Check] Tavily 搜索失败: {str(e)}")
    
    return None


def generate_fact_check_content(question, retrieved_docs, ai_answer, language="English"):
    """
    生成完整的 Fact-Check 内容（智能优化版）
    
    Args:
        question: 用户问题
        retrieved_docs: 检索到的文档
        ai_answer: AI 回答
        language: 语言
    
    Returns:
        str: HTML 格式的 Fact-Check 内容
    """
    # 1. 生成知识库摘要
    kb_summary = summarize_fact_check(question, retrieved_docs, ai_answer, language)
    
    # 2. 可选：智能网络搜索补充（传递 RAG 文档用于优化搜索查询）
    web_summary = web_search_supplement(
        question=question, 
        retrieved_docs=retrieved_docs,  # 传递 RAG 上下文优化搜索
        language=language
    )
    
    # 3. 组合内容
    if language == "Portuguese":
        header = "📋 **Verificação de Factos Baseada em Conhecimento Científico**\n\n"
    else:
        header = "📋 **Fact-Check Based on Scientific Knowledge**\n\n"
    
    content = header + kb_summary
    
    if web_summary:
        content += f"\n\n---\n\n{web_summary}"
    
    return content

