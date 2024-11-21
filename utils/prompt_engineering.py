from langchain_core.prompts import PromptTemplate

def init_prompts():
    prompt = PromptTemplate(
        template="""Use all the information from the context and the conversation history to answer new question. If you see the answer in previous conversation history or the context. \
    Answer it with clarifying the source information. If you don't see it in the context or the chat history, just say you \
    didn't find the answer in the given data. Don't make things up.

    Previous conversation history from the questioner. "Human" was the user who's asking the new question. "Assistant" was you as the assistant:
    ```{chat_history}
    ```

    Vector search result of the new question:
    ```{context}
    ```

    New Question:
    ```{question}```

    Answer:""",
        input_variables=["context", "question", "chat_history"],
    )

    condense_question_prompt_passthrough = PromptTemplate(
        template="""Repeat the following question:
    {question}
    """,
        input_variables=["question"],
    )

    return prompt, condense_question_prompt_passthrough