from fastapi import FastAPI
from langserve import add_routes
from chain import qa_chain
import uvicorn
#from langserve import LangServe

app = FastAPI(
    title="LangChain Server",
    version="1.0",
    description="Spin up a simple api server using Langchain's Runnable interfaces",
)

#langserve = LangServe()
#langserve.add_chain("chat", qa_chain, app)

# Adds routes to the app for using the chain under:
# /invoke
# /batch
# /stream
add_routes(app, qa_chain)

print(app.routes)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)