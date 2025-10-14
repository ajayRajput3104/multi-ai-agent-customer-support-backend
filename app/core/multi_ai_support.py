from typing import TypedDict, Dict
from langgraph.graph import StateGraph, END
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
import re
from app.config import get_settings

settings = get_settings()

class State(TypedDict):
    query: str
    category: str
    sentiment: str
    response: str

# Initialize model
llm = ChatGroq(
    temperature=0,
    api_key=settings.groq_api_key,
    model_name="llama-3.3-70b-versatile"
)

def clean_response(text: str) -> str:
    if not isinstance(text, str):
        return ""
    text = text.encode('utf-8').decode('unicode_escape')
    text = re.sub(r"\*\*(.*?)\*\*", r"\1", text)
    text = re.sub(r"\*(.*?)\*", r"\1", text)
    text = re.sub(r"^\s*[-*]\s*", "- ", text, flags=re.MULTILINE)
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"[ \t]+", " ", text)
    return text.strip()

def categorize(state: State) -> State:
    prompt = ChatPromptTemplate.from_template(
        "Categorize the following customer query into one of these categories: "
        "Technical, Billing, or General. Respond with only the category name. Query: {query}"
    )
    chain = prompt | llm
    category = chain.invoke({"query": state["query"]}).content
    return {"category": category.strip()}

def analyze_sentiment(state: State) -> State:
    prompt = ChatPromptTemplate.from_template(
        "Analyze the sentiment of this customer query. "
        "Respond with 'Positive', 'Neutral', or 'Negative'. Query: {query}"
    )
    chain = prompt | llm
    sentiment = chain.invoke({"query": state["query"]}).content
    return {"sentiment": sentiment.strip()}

def handle_technical(state: State) -> State:
    prompt = ChatPromptTemplate.from_template(
        "Provide a concise technical support response for this query (no labels). Query: {query}"
    )
    chain = prompt | llm
    response = clean_response(chain.invoke({"query": state["query"]}).content)
    return {"response": response}

def handle_billing(state: State) -> State:
    prompt = ChatPromptTemplate.from_template(
        "Provide a concise billing support response for this query (no labels). Query: {query}"
    )
    chain = prompt | llm
    response = clean_response(chain.invoke({"query": state["query"]}).content)
    return {"response": response}

def handle_general(state: State) -> State:
    prompt = ChatPromptTemplate.from_template(
        "Provide a concise general support response for this query (no labels). Query: {query}"
    )
    chain = prompt | llm
    response = clean_response(chain.invoke({"query": state["query"]}).content)
    return {"response": response}

def escalate(state: State) -> State:
    return {"response": "This query has been escalated to a human agent due to its negative sentiment."}

def route_query(state: State) -> str:
    if state["sentiment"].lower() == "negative":
        return "escalate"
    elif state["category"].lower().startswith("tech"):
        return "handle_technical"
    elif state["category"].lower().startswith("bill"):
        return "handle_billing"
    else:
        return "handle_general"

# Build Workflow Graph
workflow = StateGraph(State)

workflow.add_node("categorize", categorize)
workflow.add_node("analyze_sentiment", analyze_sentiment)
workflow.add_node("handle_technical", handle_technical)
workflow.add_node("handle_billing", handle_billing)
workflow.add_node("handle_general", handle_general)
workflow.add_node("escalate", escalate)

workflow.add_edge("categorize", "analyze_sentiment")
workflow.add_conditional_edges(
    "analyze_sentiment",
    route_query,
    {
        "handle_technical": "handle_technical",
        "handle_billing": "handle_billing",
        "handle_general": "handle_general",
        "escalate": "escalate",
    },
)
workflow.add_edge("handle_technical", END)
workflow.add_edge("handle_billing", END)
workflow.add_edge("handle_general", END)
workflow.add_edge("escalate", END)
workflow.set_entry_point("categorize")

app_graph = workflow.compile()

def run_customer_support(query: str) -> Dict[str, str]:
    results = app_graph.invoke({"query": query})
    clean_text = clean_response(results.get("response", ""))

    return {
        "category": results.get("category", "").strip(),
        "sentiment": results.get("sentiment", "").strip(),
        "response": clean_text,
    }