from langchain_google_genai import ChatGoogleGenerativeAI


def get_chat_model(temperature: float = 0.0) -> ChatGoogleGenerativeAI:
    """
    temperature=0.0 por padrão: para tarefa de classificação/extração,
    queremos a resposta mais determinística possível, não criatividade.
    """
    return ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=temperature,
    )