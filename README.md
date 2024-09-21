🚀 PlugTalk: A Conversational AI Chatbot with Dynamic Web Scraping & Retrieval
PlugTalk is an intelligent chatbot designed to provide dynamic, context-aware answers by leveraging large language models (LLMs) like OpenAI's GPT. The chatbot can scrape content from websites, store it in vector databases, and perform document retrieval to answer user queries with precision.

📝 Table of Contents
Introduction
Features
Tech Stack
Installation
Usage
Configuration
Contributing
License
💡 Introduction
PlugTalk is a web-based chatbot built using LangChain, Streamlit, and OpenAI's GPT models. It can ingest custom website data through URL scraping, store it in a vector database, and provide responses by retrieving relevant information. The chatbot can also adapt to various custom API keys, making it versatile for different user requirements.

✨ Features
Conversational Retrieval: Retrieves documents and provides precise answers from scraped content.
Custom API Integration: Users can supply their OpenAI API keys and models directly from the sidebar.
Website Scraping: Dynamically scrapes data from user-specified URLs.
Persistent Chat History: Keeps chat history intact while switching between different models and websites.
Scalable LLM Integration: Works with multiple LLMs including OpenAI’s GPT models.
Error Handling: Detects and notifies users of issues like invalid URLs or API authentication errors.
🛠️ Tech Stack
Backend: LangChain, Chroma, FAISS
Frontend: Streamlit
Language Models: OpenAI GPT
Web Scraping: Python Requests library
Embeddings: OpenAI Embeddings 
🚀 Installation
To install and run PlugTalk locally, follow these steps:

Clone the repository:

bash
Copy code
git clone https://github.com/your-username/PlugTalk.git
cd PlugTalk
Set up a virtual environment:

bash
Copy code
python3 -m venv venv
source venv/bin/activate  # For Windows: venv\Scripts\activate
Install the required dependencies:

bash
Copy code
pip install -r requirements.txt
Set up OpenAI API Key:

Get your OpenAI API key from the OpenAI platform.
You can either set it up via environment variables or directly input it through the Streamlit sidebar.
Run the application:

bash
Copy code
streamlit run Home.py
🧑‍💻 Usage
1. Starting the Chatbot
Run the Streamlit app using the command above.
The app will launch in your web browser.
2. Add Website URLs
Enter the website URLs you want the chatbot to scrape and analyze.
Click on the ":heavy_plus_sign: Add Website" button to add the URLs.
3. Input Custom OpenAI API Key
Use the sidebar to input your custom OpenAI API key and choose a model from the dropdown.
4. Ask Questions
Start asking questions in the chat input box.
The chatbot will retrieve the most relevant information from the scraped websites and generate responses.
5. Clear Website Data
Use the "Clear" button in the sidebar to reset the website list.
⚙️ Configuration
Custom API Key and Model Selection
PlugTalk allows you to enter your custom OpenAI API key in the sidebar.
You can choose from a list of available GPT models like GPT-4, GPT-3, or others.
Vector Store Setup
The chatbot uses the Chroma vector database to store and retrieve website content.
Content is split into smaller chunks using the Recursive Character Text Splitter for efficient retrieval.
🤝 Contributing
Contributions are welcome! Here's how you can get started:

Fork the repository.
Create a new branch (git checkout -b feature/your-feature-name).
Make your changes.
Submit a pull request.
📝 License
This project is licensed under the MIT License. See the LICENSE file for more details.




