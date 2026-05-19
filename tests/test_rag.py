from Backend.src.LLM import gemini_response
def test_rag_search():

    query = "What fertilizer for potato disease?"

    result = gemini_response(query)

    assert len(result) > 0