from brain import ask_chloro
def test_ask_chloro():
    # Test a simple query
    response = ask_chloro("What is the weather today?")
    assert isinstance(response, str) and len(response) > 0, "Response should be a non-empty string."

    # Test a query with visual trigger (assuming snapshot.jpg exists)
    response_with_visual = ask_chloro("Can you analyze the image?")
    assert isinstance(response_with_visual, str) and len(response_with_visual) > 0, "Response with visual trigger should be a non-empty string."

    # Test an empty query
    response_empty = ask_chloro("")
    assert isinstance(response_empty, str), "Response to empty query should still be a string."