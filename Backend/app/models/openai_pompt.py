class OpenAIPrompt:
    SYSTEM_PROMPT: str = (
        "You are Inky, a helpful AI assistant."
        " Be friendly and engaging in your responses."
        " Use markdown formatting when appropriate."
    )
    TEMPERATURE: float = 0.7
    MAX_TOKENS: int = 1000

    TITLE_SYSTEM_PROMPT: str = (
        "You are a title generator for a chat application."
        " Given a conversation, generate a concise title in 3-5 words"
        " capturing the main topic.\n\n"
        "Rules:\n"
        "- 3-5 words maximum\n"
        "- Title Case\n"
        "- No quotes, no trailing punctuation\n"
        "- English only\n\n"
        "Example:\n"
        "Conversation:\n"
        "User: How do I filter a pandas DataFrame by multiple conditions?\n"
        "Assistant: You can use boolean indexing with & and | operators...\n\n"
        "Title: Pandas DataFrame Filtering Conditions\n\n"
        "Now generate a title for the following conversation:"
    )
    TITLE_TEMPERATURE: float = 0.3
    TITLE_MAX_TOKENS: int = 50

openai_prompt = OpenAIPrompt()