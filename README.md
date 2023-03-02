# Chat Application

This is a chat application that allows users to chat with an AI assistant powered by OpenAI's GPT-3 language model.

Note that this code is only the backend implementation of a chat application. The frontend implementation is in a separate repository.

## Features

- Allows users to send messages to the assistant.
- The assistant replies with an appropriate message using the GPT-3 language model.
- The chat messages are displayed in real-time.

## Requirements

- Python 3.6 or higher
- OpenAI API key
- FastAPI
- Uvicorn

## Getting started

1. Clone this repository: `git clone https://github.com/yourusername/chat-app.git`
2. Install the required packages: `pip install -r requirements.txt`
3. Create config.py file as below

    import os
    environ = {"OPENAI_API_KEY" : "REPLACE WITH YOUR SECRET KEY"}

    def load_env_var():
        for e in environ:#e is just keys
            os.environ[e]=environ[e]
        return None

4. Run the application: `uvicorn main:app --reload`
5. Open http://localhost:8000 in your browser.

## Usage

1. Enter your message in the input field and click on the send button.
2. The assistant will reply with a message.
3. The conversation history is displayed in the chat window.

## Contributing

Contributions are welcome! If you find any issues or want to add new features, feel free to submit a pull request.

## License

This project is licensed under the MIT License 