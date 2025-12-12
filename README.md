# GitReadMe - AI-Powered README Generator

GitReadMe is an intelligent, full-stack application designed to transform your GitHub repositories into professional, comprehensive documentation automatically. By leveraging **Google Gemini’s advanced AI capabilities**, GitReadMe analyzes your codebase and generates high-quality README files, significantly streamlining the documentation process for developers.

## ✨ Features

*   **AI-Powered README Generation**: Automatically creates detailed READMEs from GitHub repository URLs using the Gemini model.
*   **Code Analysis & Summarization**: Intelligently processes and summarizes repository code to inform README content.
*   **Standard & Example-Rich READMEs**: Option to generate a standard README or one that includes example code snippets and detailed explanations.
*   **User-Friendly Web Interface**: A modern and intuitive frontend built with Next.js allows for easy input and result management.
*   **FastAPI Backend**: Robust and scalable API to handle repository cloning, code processing, and AI interactions.
*   **Gemini Integrated**: Fully powered by Google’s Gemini API for high-quality LLM responses.
*   **Copy & Download**: Easily copy the generated README content or download it as a Markdown file.

## 🛠️ Tech Stack

### Backend

*   **Python**: Primary language for backend logic.
*   **FastAPI**: A modern, fast (high-performance) web framework for building APIs.
*   **Langchain**: Used for integrating with large language models and managing AI workflows.
*   **GitPython**: For programmatically interacting with Git repositories (cloning, scanning, etc.).

### Frontend

*   **Next.js**: React framework for building the user interface.
*   **React**: JavaScript library for building interactive UIs.
*   **Tailwind CSS**: A utility-first CSS framework for rapid UI development.
*   **Shadcn/ui**: Components for building beautiful, modern interfaces.

### AI / Machine Learning

*   **Google Gemini API**: Gemini 1.5 Flash is used for code summarization and README generation.

## 🚀 Getting Started

These instructions will help you set up the project locally for development and testing.

### Prerequisites

Before you begin, ensure you have the following installed:

*   Python 3.9+ (`python --version`)
*   Node.js 18.18+ (`node --version`)
*   npm (`npm --version`)
*   Git (`git --version`)
*   Gemini API Key

### Installation

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/ANMOLJ1593/GitReadMe.git
    cd GitReadMe
    ```

2.  **Set up Python Backend:**

    ```bash
    python -m venv venv
    source venv/bin/activate # On Windows, use `.\venv\Scripts\activate`
    pip install -r requirements.txt
    ```

3.  **Set up Node.js Frontend:**

    ```bash
    cd gitreadme-frontend
    npm install
    cd ..
    ```

### Running Locally

To start both the backend and frontend in development mode, run the `start-dev.sh` script from the project root:

```bash
./start-dev.sh
```
This will start:
*   FastAPI backend on `http://localhost:8000`
*   Next.js frontend on `http://localhost:3000`

You can access the API documentation at `http://localhost:8000/api/docs`.

### Environment Variables

Create a `.env` file in the project root with your Azure OpenAI credentials:

```dotenv
GEMINI_API_KEY="your_gemini_api_key"
GEMINI_MODEL_NAME="gemini-1.5-flash"

###  Deployment

The project is deployed on **Render**, which handles the hosting of both the FastAPI backend and the Next.js frontend.


### License

This project is licensed under the MIT License - see the `LICENSE` file for details. 
