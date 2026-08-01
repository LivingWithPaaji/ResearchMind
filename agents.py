from langchain.agents import create_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from tools import web_search , scrape_url 
from dotenv import load_dotenv
from langchain_ollama import ChatOllama
import os

load_dotenv()

# Local Ollama model setup.  These environment variables make the model
# configurable without changing application code.
OLLAMA_MODEL = os.getenv(
    "OLLAMA_MODEL",
    os.getenv("ollama_model", "cieloforge/Deepseek-r1-7b-spec:latest"),
)
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

llm = ChatOllama(
    model=OLLAMA_MODEL,
    base_url=OLLAMA_BASE_URL,
    temperature=0,
)


#1st agent 
def build_search_agent():
    return create_agent(
        model = llm,
        tools= [web_search]
    )

#2nd agent 

def build_reader_agent():
    return create_agent(
        model = llm,
        tools = [scrape_url]
    )


#writer chain 

writer_prompt = ChatPromptTemplate.from_messages([
    ("system", (
        "You are an expert research writer. Produce exhaustive, structured, and insightful reports with deep analysis and extensive detail. "
        "CRITICAL LINK RULES:\n"
        "1. ONLY use the actual, real URLs provided in the list of 'Available Authentic URLs'. Never invent or hallucinate URLs.\n"
        "2. NEVER use placeholders like 'example.com' or mock URLs.\n"
        "3. Every URL MUST be formatted in clean Markdown without spaces in the parentheses: [Anchor Text](URL). "
        "Use exactly the raw URL: [Title](https://domain.com/path-to-page)."
    )),
    ("human", """
Write a comprehensive research report on the topic below.

Topic: {topic}

Research Gathered:
{research}

Available Authentic URLs (You MUST restrict your references and links ONLY to these URLs):
{urls}

Structure the report with the following sections and detailed content:
- Executive Summary (brief high-level overview)
- Introduction (background, significance, objectives)
- Methodology (how the research was conducted, sources used)
- Key Findings (minimum 5 well-explained points, each with subpoints and examples)
- Detailed Analysis (in‑depth discussion of each finding, implications, comparisons)
- Future Directions (potential next steps, open questions)
- Conclusion (summarize insights and recommendations)
- References (list all raw, actual URLs from the Available Authentic URLs list that are relevant. Do not invent any URLs. Format them as simple markdown links: [Source Title](actual-url))

Write in a professional tone, include data where relevant, and ensure the report is thorough and satisfying for the reader. All links must be fully functional and point to the actual URLs from the Available Authentic URLs list.
""")
])

writer_chain = writer_prompt | llm | StrOutputParser()

#critic_chain 

critic_prompt = ChatPromptTemplate.from_messages([
     ("system", "You are a sharp and constructive research critic. Be honest and specific."),
    ("human", """Review the research report below and evaluate it strictly.

Report:
{report}

Respond in this exact format:

Score: X/10

Strengths:
- ...
- ...

Areas to Improve:
- ...
- ...

One line verdict:
..."""),
])

critic_chain = critic_prompt | llm | StrOutputParser()
