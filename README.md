# Crypto Chatbot WebSocket API Backend

Welcome to the Crypto Chatbot WebSocket API Backend! This project is designed to provide API WebSocket endpoints specifically for a cryptocurrency-focused chatbot. Built with the modern FastAPI framework, this backend leverages the Langchain NLP framework to deliver insightful and intelligent chat interactions about cryptocurrencies.

## Features

- **FastAPI**: A cutting-edge, high-performance web framework perfect for creating robust APIs using Python 3.6+.
- **WebSocket Support**: Facilitates real-time, bi-directional communication between clients and the server, enabling seamless, dynamic interactions with the chatbot.
- **Langchain NLP Framework**: Enhances natural language processing capabilities to provide informed and context-aware responses about cryptocurrencies.
- **Cryptocurrency Knowledge**: The chatbot is pre-loaded with knowledge specific to the crypto industry, including market trends, coin information, and trading tips.

## Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/yourusername/crypto-chatbot-websocket-api-backend.git
   cd crypto-chatbot-websocket-api-backend
   ```

2. **Create a Virtual Environment:**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Server:**

   ```bash
   uvicorn main:app --reload
   ```

   The server will start on `http://127.0.0.1:8000`.

## Usage

### WebSocket Endpoint

The WebSocket endpoint for the crypto chatbot is accessible at:

```
/api/server1/chat
/api/server2/chat
/api/server3/chat
```

Clients can connect to this endpoint to engage in real-time chat interactions focusing on cryptocurrency topics. The server processes incoming messages using the Langchain NLP framework and responds with relevant cryptocurrency information.

## Configuration

To configure the necessary settings, create a `.env` file in the root directory with the following:

- `PINECONE_API_KEY`: Your Pinecone API key for accessing Pinecone services.
- `PINECONE_ENV`: The environment setting for Pinecone (us-west1-gcp, etc.).

## Contributing

Contributions to improve the Crypto Chatbot WebSocket API Backend are welcome! Whether it's bug fixes, feature enhancements, or general improvements, feel free to open issues or submit pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

For questions or further information, contact [drozd.dev@outlook.com](mailto:drozd.dev@outlook.com).

---

Elevate your cryptocurrency conversations with our feature-rich crypto chatbot. Enjoy real-time, intelligent interaction with up-to-the-minute crypto insights and advice!