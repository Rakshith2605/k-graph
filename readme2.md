# Graphiti Agent - Setup & Troubleshooting Guide

## Project Overview
This project demonstrates the use of Graphiti Agent with Neo4j and OpenAI APIs. It connects to a Neo4j database, adds episodes, and performs semantic/graph searches using LLMs.

---

## Prerequisites
- Python 3.8+
- pip (Python package manager)
- Access to a Neo4j Aura instance (or compatible Neo4j DB)
- OpenAI API key

---

## Setup Instructions

### 1. Clone the Repository
```sh
git clone <your-repo-url>
cd graphiti-agent
```

### 2. Install Dependencies
```sh
pip install -r requirements.txt
```

### 3. Configure Environment Variables
Create a `.env` file in the project root with the following content:
```env
# Neo4j Aura connection settings
NEO4J_URI=neo4j+s://<your-neo4j-uri>
NEO4J_USER=<your-neo4j-username>
NEO4J_PASSWORD=<your-neo4j-password>

# OpenAI settings
OPENAI_API_KEY=<your-openai-api-key>
```
**Note:** Never commit your real API keys or passwords to version control.

### 4. Run the Project
```sh
python quickstart.py
```

---

## Troubleshooting API Issues

### OpenAI API Key Issues
- **401 Unauthorized / Invalid API Key:**
  - Double-check your `.env` file for typos in `OPENAI_API_KEY`.
  - Make sure you have not set an incorrect `OPENAI_API_KEY` in your shell environment. You can check with:
    ```sh
    echo $OPENAI_API_KEY
    ```
    If it shows a placeholder or wrong value, unset it:
    ```sh
    unset OPENAI_API_KEY
    ```
  - Ensure your `.env` file is present and correctly formatted.
  - If you update the `.env` file, restart your terminal or Python process to reload variables.
  - Confirm your OpenAI account is active and the key is valid at https://platform.openai.com/api-keys

### Neo4j Connection Issues
- **Authentication or Connection Errors:**
  - Verify `NEO4J_URI`, `NEO4J_USER`, and `NEO4J_PASSWORD` in your `.env` file.
  - Ensure your Neo4j instance is running and accessible from your network.

### Dependency Issues (e.g., NumPy)
- If you see errors about NumPy version incompatibility, downgrade NumPy:
  ```sh
  pip install "numpy<2.0.0" --force-reinstall
  ```

---

## Additional Tips
- If you use conda, ensure you are in the correct environment before running the project.
- If you encounter issues with environment variables not loading, check that `python-dotenv` is installed and that your code calls `load_dotenv()` early in execution.
- For further debugging, add `print(os.environ)` or `print(os.getenv('OPENAI_API_KEY'))` in your script to verify environment variable values.
- **Exiting a Virtual Environment:**  
  - If you activated a venv (using `source venv/bin/activate`), simply run:
    ```sh
    deactivate
    ```
  - If you are using a conda environment, run:
    ```sh
    conda deactivate
    ```
  (This will exit the virtual environment and return you to your system's default Python.)

---

## Support
If you continue to have issues, please open an issue in the repository or contact the maintainer. 