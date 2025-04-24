from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_nomic.embeddings import NomicEmbeddings
from langchain_community.document_loaders import WebBaseLoader
from langchain_qdrant import QdrantVectorStore
import os

# Set user-agent to avoid request block
os.environ["USER_AGENT"] = "chaidocs-chatbot/1.0"


embeddings = NomicEmbeddings(model="nomic-embed-text-v1.5", inference_mode="local")


# HTML
html_urls = [
    "https://chaidocs.vercel.app/youtube/chai-aur-html/welcome/",
    "https://chaidocs.vercel.app/youtube/chai-aur-html/introduction/",
    "https://chaidocs.vercel.app/youtube/chai-aur-html/emmit-crash-course/",
    "https://chaidocs.vercel.app/youtube/chai-aur-html/html-tags/"
]

html_docs = []
for url in html_urls:
    loader = WebBaseLoader(url)
    html_docs.extend(loader.load())


text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
    chunk_size=800, chunk_overlap=200
)

html_doc_splits = text_splitter.split_documents(html_docs)

html_store = QdrantVectorStore.from_documents(
    documents=[],
    url="http://localhost:6333",
    collection_name="html",
    embedding=embeddings
)


html_store.add_documents(documents=html_doc_splits)
print("Injection Done -> html_store")



# GIT
git_urls = [
    "https://chaidocs.vercel.app/youtube/chai-aur-git/welcome/",
    "https://chaidocs.vercel.app/youtube/chai-aur-git/introduction/",
    "https://chaidocs.vercel.app/youtube/chai-aur-git/terminology/",
    "https://chaidocs.vercel.app/youtube/chai-aur-git/behind-the-scenes/",
    "https://chaidocs.vercel.app/youtube/chai-aur-git/branches/",
    "https://chaidocs.vercel.app/youtube/chai-aur-git/diff-stash-tags/",
    "https://chaidocs.vercel.app/youtube/chai-aur-git/managing-history/",
    "https://chaidocs.vercel.app/youtube/chai-aur-git/github/"
]

git_docs = []
for url in git_urls:
    loader = WebBaseLoader(url)
    git_docs.extend(loader.load())


text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
    chunk_size=800, chunk_overlap=200
)

git_doc_splits = text_splitter.split_documents(git_docs)

git_store = QdrantVectorStore.from_documents(
    documents=[],
    url="http://localhost:6333",
    collection_name="git",
    embedding=embeddings
)

git_store.add_documents(documents=git_doc_splits)
print("Injection Done -> git_store")




# CPP
cpp_urls = [
    "https://chaidocs.vercel.app/youtube/chai-aur-c/welcome/",
    "https://chaidocs.vercel.app/youtube/chai-aur-c/introduction/",
    "https://chaidocs.vercel.app/youtube/chai-aur-c/hello-world/",
    "https://chaidocs.vercel.app/youtube/chai-aur-c/variables-and-constants/",
    "https://chaidocs.vercel.app/youtube/chai-aur-c/data-types/",
    "https://chaidocs.vercel.app/youtube/chai-aur-c/operators/",
    "https://chaidocs.vercel.app/youtube/chai-aur-c/control-flow/",
    "https://chaidocs.vercel.app/youtube/chai-aur-c/loops/",
    "https://chaidocs.vercel.app/youtube/chai-aur-c/functions/"
]


cpp_docs = []
for url in cpp_urls:
    loader = WebBaseLoader(url)
    cpp_docs.extend(loader.load())


text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
    chunk_size=800, chunk_overlap=200
)

cpp_doc_splits = text_splitter.split_documents(cpp_docs)

cpp_store = QdrantVectorStore.from_documents(
    documents=[],
    url="http://localhost:6333",
    collection_name="cpp",
    embedding=embeddings
)


cpp_store.add_documents(documents=cpp_doc_splits)
print("Injection Done -> cpp_store")





# DJANGO
django_urls = [
    "https://chaidocs.vercel.app/youtube/chai-aur-django/welcome/",
    "https://chaidocs.vercel.app/youtube/chai-aur-django/getting-started/",
    "https://chaidocs.vercel.app/youtube/chai-aur-django/jinja-templates/",
    "https://chaidocs.vercel.app/youtube/chai-aur-django/tailwind/",
    "https://chaidocs.vercel.app/youtube/chai-aur-django/models/",
    "https://chaidocs.vercel.app/youtube/chai-aur-django/relationships-and-forms/"
]

django_docs = []
for url in django_urls:
    loader = WebBaseLoader(url)
    django_docs.extend(loader.load())


text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
    chunk_size=800, chunk_overlap=200
)

django_doc_splits = text_splitter.split_documents(django_docs)

django_store = QdrantVectorStore.from_documents(
    documents=[],
    url="http://localhost:6333",
    collection_name="django",
    embedding=embeddings
)


django_store.add_documents(documents=django_doc_splits)
print("Injection Done -> django_store")



# SQL
sql_urls = [
    "https://chaidocs.vercel.app/youtube/chai-aur-sql/welcome/",
    "https://chaidocs.vercel.app/youtube/chai-aur-sql/introduction/",
    "https://chaidocs.vercel.app/youtube/chai-aur-sql/postgres/",
    "https://chaidocs.vercel.app/youtube/chai-aur-sql/normalization/",
    "https://chaidocs.vercel.app/youtube/chai-aur-sql/database-design-exercise/",
    "https://chaidocs.vercel.app/youtube/chai-aur-sql/joins-and-keys/",
    "https://chaidocs.vercel.app/youtube/chai-aur-sql/joins-exercise/"
]

sql_docs = []
for url in sql_urls:
    loader = WebBaseLoader(url)
    sql_docs.extend(loader.load())


text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
    chunk_size=800, chunk_overlap=200
)

sql_doc_splits = text_splitter.split_documents(sql_docs)

sql_store = QdrantVectorStore.from_documents(
    documents=[],
    url="http://localhost:6333",
    collection_name="sql",
    embedding=embeddings
)


sql_store.add_documents(documents=sql_doc_splits)
print("Injection Done -> sql_store")




# DEVOPS
devops_urls = [
    "https://chaidocs.vercel.app/youtube/chai-aur-devops/welcome/",
    "https://chaidocs.vercel.app/youtube/chai-aur-devops/setup-vpc/",
    "https://chaidocs.vercel.app/youtube/chai-aur-devops/setup-nginx/",
    "https://chaidocs.vercel.app/youtube/chai-aur-devops/nginx-rate-limiting/",
    "https://chaidocs.vercel.app/youtube/chai-aur-devops/nginx-ssl-setup/",
    "https://chaidocs.vercel.app/youtube/chai-aur-devops/node-nginx-vps/",
    "https://chaidocs.vercel.app/youtube/chai-aur-devops/postgresql-docker/",
    "https://chaidocs.vercel.app/youtube/chai-aur-devops/postgresql-vps/",
    "https://chaidocs.vercel.app/youtube/chai-aur-devops/node-logger/"
]


devops_docs = []
for url in devops_urls:
    loader = WebBaseLoader(url)
    devops_docs.extend(loader.load())


text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
    chunk_size=800, chunk_overlap=200
)

devops_doc_splits = text_splitter.split_documents(devops_docs)

devops_store = QdrantVectorStore.from_documents(
    documents=[],
    url="http://localhost:6333",
    collection_name="devops",
    embedding=embeddings
)

devops_store.add_documents(documents=devops_doc_splits)
print("Injection Done -> devops_store")









