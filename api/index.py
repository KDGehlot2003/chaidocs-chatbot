from fastapi import FastAPI, HTTPException
from langchain_qdrant import QdrantVectorStore
from langchain_nomic.embeddings import NomicEmbeddings
from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel
import os
import  json
from fastapi.middleware.cors import CORSMiddleware



load_dotenv()

### Create FastAPI instance with custom docs and openapi url
app = FastAPI(docs_url="/api/py/docs", openapi_url="/api/py/openapi.json")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or specify exact frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

embeddings = NomicEmbeddings(model="nomic-embed-text-v1.5", inference_mode="local")


client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=os.getenv("GROQ_API_KEY")
)

vector_stores = {
    "html_retriver":QdrantVectorStore.from_existing_collection(embedding=embeddings,url=os.getenv("url"),prefer_grpc=True,api_key=os.getenv("api_key"),collection_name="html"),
    "git_retriver": QdrantVectorStore.from_existing_collection(embedding=embeddings,url=os.getenv("url"),prefer_grpc=True,api_key=os.getenv("api_key"),collection_name="git"),
    "django_retriver": QdrantVectorStore.from_existing_collection(embedding=embeddings,url=os.getenv("url"),prefer_grpc=True,api_key=os.getenv("api_key"),collection_name="django"),
    "devops_retriver": QdrantVectorStore.from_existing_collection(embedding=embeddings,url=os.getenv("url"),prefer_grpc=True,api_key=os.getenv("api_key"),collection_name="devops"),
    "cpp_retriver": QdrantVectorStore.from_existing_collection(embedding=embeddings,url=os.getenv("url"),prefer_grpc=True,api_key=os.getenv("api_key"),collection_name="cpp"),
}

vector_stores_list = [
    "html_retriver",
    "git_retriver",
    "django_retriver",
    "devops_retriver",
    "cpp_retriver",
    "general_retriver"
]

class ChatRequest(BaseModel):
    query: str



# html_retriver = QdrantVectorStore.from_existing_collection(
#     embedding=embeddings,
#     url=os.getenv("url"),
#     prefer_grpc=True,
#     api_key=os.getenv("api_key"),
#     collection_name="html",
# ).as_retriever()

# git_retriver = QdrantVectorStore.from_existing_collection(
#     embedding=embeddings,
#     url=os.getenv("url"),
#     prefer_grpc=True,
#     api_key=os.getenv("api_key"),
#     collection_name="git",
# ).as_retriever()


# devops_retriver = QdrantVectorStore.from_existing_collection(
#     embedding=embeddings,
#     url=os.getenv("url"),
#     prefer_grpc=True,
#     api_key=os.getenv("api_key"),
#     collection_name="devops",
# ).as_retriever()

# cpp_retriver = QdrantVectorStore.from_existing_collection(
#     embedding=embeddings,
#     url=os.getenv("url"),
#     prefer_grpc=True,
#     api_key=os.getenv("api_key"),
#     collection_name="cpp",
# ).as_retriever()




async def get_retriver(query: str):
    SYSTEM_PROMPT_RETRIVER = f""""
    You are expert at routing user queries into the appropriate category for the chaidocs. Analyze the user query and return only the name of retriver based the user query.

    Here are some retriver that we have:
    1. html_retriver: HTML Docs retriver
    2. git_retriver: GIT Docs retriver
    3. django_retriver: Django Docs retriver
    4. Devops_retriver: Devops Docs retriver
    5. cpp_retriver: C++ Docs retriver
    6. general_retriver: General Chit chat

    Your Task is that based on ther user's query. select the most appropriate retriver for the query.

    ### Output Rules:
        - return only the retriver name in the json format. do not give explanation

    ### Output Format:
    example1:
        {{retriver: html_retriver}}
    example2:
        {{retriver: cpp_retriver}}
    """


    response = client.chat.completions.create(
        # model="llama-3.3-70b-versatile",
        model="llama-3.1-8b-instant",
        response_format={"type": "json_object"},
        messages=[
            { "role": "system", "content": SYSTEM_PROMPT_RETRIVER },
            { "role": "user", "content": query }
        ],
    )

    # print(response.choices[0].message.content)

    return response.choices[0].message.content



async def generateSimilarQuestion(query: str):
    SYSTEM_PROMT_GENERATE_QUESTIONS = f""""
    You are a helpfull assistant which create three sub questions or create question based on the user query.

    ## Your Task:
        - Generate 3 questions in json format.
        - Keep them clear, concise, and contextually related.
        - Questions should be based on the original query.

    ## Output Format:
    {{
        "question1": question1
        "question2": question2
        "question3": question3
    }}

    """

    response = client.chat.completions.create(
        # model="llama-3.3-70b-versatile",
        model="llama-3.1-8b-instant",
        response_format={"type": "json_object"},
        messages=[
            { "role": "system", "content": SYSTEM_PROMT_GENERATE_QUESTIONS },
            { "role": "user", "content": query }
        ],
    )

    # print(response.choices[0].message.content)

    return response.choices[0].message.content


@app.get("/api/py/helloFastApi")
def hello_fast_api():
    return {"message": "Hello from FastAPI"}



@app.post("/api/py/chat")
async def chaidocschat(request: ChatRequest):
    query = request.query

    try:
        generated_questions = await generateSimilarQuestion(query=query)
        parsed_generated_questions = json.loads(generated_questions)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate similar questions: {str(e)}")



    context = []
    sources = set()

    for q_text in parsed_generated_questions.values():
        try:
            output = await get_retriver(query=q_text)
            parsed_output = json.loads(output)
            retriver_name = parsed_output.get("retriver")

            if retriver_name not in vector_stores_list:
                continue

            if retriver_name=="general_retriver":
                continue

            retriver = vector_stores.get(retriver_name.lower())

            if retriver is None:
                raise ValueError(f"Retriever '{retriver_name}' not found.")

            # Assuming retriver.similarity_search is the async method you want
            result = await retriver.asimilarity_search(query=q_text, k=2)
            for i in result:
                sources.add(i.metadata.get("source"))
            context.append(result)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Retriever error for query '{q_text}': {str(e)}")
        
    sources = list(sources)

    SYSTEM_PROMPT = f"""
    You are a helpful assistant for the chaidocs and you expert in giving information based on the context

    {context}
    """

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": query}
            ],
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"LLM generation failed: {str(e)}")


    return {
        "Bot": response.choices[0].message.content,
        "Sources": sources
    }


