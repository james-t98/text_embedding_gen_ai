from setup import run_setup, prompt_model, download_project_data
from langchain.chains import ConversationalRetrievalChain
from config import BLOB, STORAGE_BUCKET

number_of_docs_to_load = 15
chat_session_id = "example-test-session"
destination_file_name = f"data/{BLOB}"
# Add Search Methodology for Embedding Retriever [ MMR, Semantic Search ]

def main():
    download_project_data(STORAGE_BUCKET, BLOB, destination_file_name)

    llm, retriever, memory, init_prompt, condensed_question_prompt, chat_history, vector_store = run_setup(number_of_docs_to_load, destination_file_name, chat_session_id)
    rag_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        verbose=False,
        memory=memory,
        condense_question_prompt=condensed_question_prompt,
        combine_docs_chain_kwargs={"prompt": init_prompt},
    )

    # ask some questions
    q = "What movie was Brad Pitt in?"
    ans = prompt_model(rag_chain, q, chat_history)
    print(f"Question: {q}\nAnswer: {ans}\n")

    q = "How about Jonny Depp?"
    ans = prompt_model(rag_chain, q, chat_history)
    print(f"Question: {q}\nAnswer: {ans}\n")

    q = "Are there movies about animals?"
    ans = prompt_model(rag_chain, q, chat_history)
    print(f"Question: {q}\nAnswer: {ans}\n")

if __name__=="__main__":
    main()