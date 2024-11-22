from setup import run_setup, prompt_model
from langchain.chains import ConversationalRetrievalChain

number_of_docs_to_load = 15
file_path = "data/movies.csv"
chat_session_id = "example-test-session"
# Add Search Methodology for Embedding Retriever [ MMR, Semantic Search ]

def main():
    llm, retriever, memory, init_prompt, condensed_question_prompt, chat_history = run_setup(number_of_docs_to_load, file_path, chat_session_id)
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