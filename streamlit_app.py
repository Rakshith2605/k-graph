import streamlit as st
import os
import json
import asyncio
from datetime import datetime, timezone
from config import NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD, OPENAI_API_KEY
from graphiti_core import Graphiti
from graphiti_core.nodes import EpisodeType
from agent import get_model, GraphitiDependencies, graphiti_agent

# Set OpenAI API key for the session
os.environ['OPENAI_API_KEY'] = OPENAI_API_KEY

# Helper to run async code in Streamlit
import nest_asyncio
nest_asyncio.apply()

# Initialize Graphiti client (singleton)
@st.cache_resource(show_spinner=False)
def get_graphiti_client():
    return Graphiti(NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD)

graphiti_client = get_graphiti_client()

st.title('Graphiti: Upload & Query Your Document')

# File uploader
uploaded_file = st.file_uploader('Upload a document (text or JSON)', type=['txt', 'json'])

if uploaded_file:
    try:
        # Read file content
        file_content = uploaded_file.read().decode('utf-8')
        # Try to parse as JSON, else treat as text
        try:
            content = json.loads(file_content)
            episode_type = EpisodeType.json
            # Add as a single episode for JSON
            async def add_json_episode():
                await graphiti_client.add_episode(
                    name=f'User Upload: {uploaded_file.name}',
                    episode_body=json.dumps(content),
                    source=EpisodeType.json,
                    source_description='User uploaded JSON document',
                    reference_time=datetime.now(timezone.utc),
                )
            asyncio.run(add_json_episode())
            st.success('JSON document ingested into the knowledge graph!')
        except Exception:
            # Treat as structured text: split into paragraphs (or sentences)
            paragraphs = [p.strip() for p in file_content.split('\n') if p.strip()]
            if not paragraphs:
                raise ValueError('No valid text found in the uploaded file.')
            errors = []
            for i, para in enumerate(paragraphs):
                async def add_text_episode():
                    await graphiti_client.add_episode(
                        name=f'User Upload: {uploaded_file.name} - Part {i+1}',
                        episode_body=para,
                        source=EpisodeType.text,
                        source_description=f'User uploaded text document (part {i+1})',
                        reference_time=datetime.now(timezone.utc),
                    )
                try:
                    asyncio.run(add_text_episode())
                except Exception as e:
                    errors.append(str(e))
            if errors:
                st.error(f'Failed to ingest some parts: {errors}')
            else:
                st.success(f'Text document ingested as {len(paragraphs)} episodes into the knowledge graph!')
    except Exception as e:
        st.error(f'Failed to ingest document: {e}')

# Query interface
st.header('Ask a question about your document')
user_query = st.text_input('Enter your question:')

if user_query:
    async def query_graphiti(question):
        deps = GraphitiDependencies(graphiti_client=graphiti_client)
        try:
            async with graphiti_agent.run_stream(question, deps=deps) as result:
                answer = ""
                async for message in result.stream_text(delta=True):
                    answer += message
                return answer
        except Exception as e:
            return f"Error: {e}"
    answer = asyncio.run(query_graphiti(user_query))
    st.markdown('**Answer:**')
    st.write(answer) 