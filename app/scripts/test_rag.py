from rag import answer_question

# This script was a trest run for the RAG workflow and AT responses
result = answer_question(
    "Can I refund a damaged $700 order?"
)


print("\nANSWER\n")

print(
    result["answer"]
)


print("\nSOURCES\n")

for source in result["sources"]:

    print(source)