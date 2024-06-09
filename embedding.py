import os
from dotenv import load_dotenv
from llama_index.core.node_parser import SimpleNodeParser
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core import download_loader, ServiceContext, VectorStoreIndex,SimpleDirectoryReader,StorageContext,set_global_service_context
from llama_index.vector_stores.pinecone import PineconeVectorStore
from llama_index.core.node_parser import SentenceSplitter

from llama_index.core import Settings

from pinecone import Pinecone,ServerlessSpec

load_dotenv()

UnstructuredReader = download_loader("UnstructuredReader")
dir_reader = SimpleDirectoryReader('./qiskit-docs', file_extractor={".html": UnstructuredReader(),})
documents = dir_reader.load_data()
    #print(documents)
node_parser = SimpleNodeParser.from_defaults(chunk_size=500,chunk_overlap=20)



Settings.llm = OpenAI(model="gpt-3.5-turbo")
Settings.embed_model = OpenAIEmbedding(model="text-embedding-ada-002")
Settings.node_parser = SentenceSplitter(chunk_size=512, chunk_overlap=20)
Settings.num_output = 512
Settings.context_window = 3900


# initialize connection to pinecone (get API key at app.pinecone.io)
api_key = os.environ.get('PINECONE_API_KEY') or 'PINECONE_API_KEY'

# configure client
pc = Pinecone(api_key=api_key)

index_name = "qiskit-documentation-helper"
cloud = os.environ.get('PINECONE_CLOUD') or 'aws'
region = os.environ.get('PINECONE_REGION') or 'us-east-1'

spec = ServerlessSpec(cloud=cloud, region=region)
# check if index already exists (it shouldn't if this is first time)
if index_name not in pc.list_indexes().names():
    # if does not exist, create index
    pc.create_index(
        index_name,
        dimension=1536,  # dimensionality of text-embedding-ada-002
        metric='cosine',
        spec=spec
    )
# connect to index
index = pc.Index(index_name)
# view index stats
print(index.describe_index_stats())

pinecone_index= pc.Index(index_name)
vector_store=PineconeVectorStore(pinecone_index= pinecone_index)
storage_context = StorageContext.from_defaults(vector_store = vector_store)
index  = VectorStoreIndex.from_documents(documents,storage_context =storage_context,show_progress=True,)
