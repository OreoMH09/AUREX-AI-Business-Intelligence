"""
AUREX Prompt Templates
Pre-defined prompts for different use cases
"""

# System prompt for business analysis
BUSINESS_ANALYST_SYSTEM_PROMPT = """You are AUREX, an expert AI Business Analyst and Decision Support Assistant.

Your role is to:
- Analyze business documents (PDFs, Excel files, CSV data)
- Answer questions based on provided context
- Provide data-driven insights and recommendations
- Generate clear, concise, and professional responses
- Use evidence from the documents to support your answers

Guidelines:
1. Always base your answers on the provided context
2. If information is not in the context, clearly state that
3. Provide specific numbers, dates, and facts when available
4. Structure responses clearly with bullet points or sections when appropriate
5. Be professional and objective in your analysis
6. If asked for recommendations, provide actionable insights

Remember: Only use information from the provided context. Do not make up facts or figures."""


# Prompt template for RAG queries
RAG_QUERY_TEMPLATE = """Context from documents:
{context}

Question: {question}

Instructions:
- Answer the question based ONLY on the context provided above
- Be specific and cite relevant details from the context
- If the context doesn't contain enough information, say so
- Format your response clearly and professionally

Answer:"""


# Prompt template for document summarization
SUMMARIZATION_TEMPLATE = """Please provide a concise summary of the following document:

{document_text}

Summary should include:
- Key points and main findings
- Important numbers and statistics
- Critical insights and conclusions

Summary:"""


# Prompt template for data analysis
DATA_ANALYSIS_TEMPLATE = """Analyze the following data and provide insights:

{data}

Analysis should include:
- Key trends and patterns
- Notable observations
- Potential implications
- Recommendations if applicable

Analysis:"""


# Prompt template for comparison queries
COMPARISON_TEMPLATE = """Based on the following information:

{context}

Compare and analyze: {comparison_request}

Provide:
- Side-by-side comparison
- Key differences and similarities
- Insights and conclusions

Comparison:"""


def build_rag_prompt(context: str, question: str) -> str:
    """
    Build RAG prompt from context and question
    
    Args:
        context: Retrieved context from documents
        question: User question
        
    Returns:
        Formatted prompt
    """
    return RAG_QUERY_TEMPLATE.format(context=context, question=question)


def build_summary_prompt(document_text: str) -> str:
    """
    Build document summarization prompt
    
    Args:
        document_text: Text to summarize
        
    Returns:
        Formatted prompt
    """
    return SUMMARIZATION_TEMPLATE.format(document_text=document_text)


def build_analysis_prompt(data: str) -> str:
    """
    Build data analysis prompt
    
    Args:
        data: Data to analyze
        
    Returns:
        Formatted prompt
    """
    return DATA_ANALYSIS_TEMPLATE.format(data=data)


def build_comparison_prompt(context: str, comparison_request: str) -> str:
    """
    Build comparison prompt
    
    Args:
        context: Context information
        comparison_request: What to compare
        
    Returns:
        Formatted prompt
    """
    return COMPARISON_TEMPLATE.format(
        context=context,
        comparison_request=comparison_request
    )
