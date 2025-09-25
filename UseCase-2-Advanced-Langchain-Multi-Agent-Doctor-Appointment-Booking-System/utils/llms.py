# # import os
# import os
import time
# from dotenv import load_dotenv
# from langchain_groq import ChatGroq
from groq import RateLimitError
from functools import wraps
from dotenv import load_dotenv
# from langchain_openai import ChatOpenAI
# load_dotenv()
# # api_key = os.getenv("GROQ_API_KEY")
# OPENAI_API_KEY=os.getenv("OPENAI_API_KEY")
# os.environ["OPENAI_API_KEY"]=OPENAI_API_KEY

# class LLMModel:
#     def __init__(self, model_name="gpt-4o"):
#         if not model_name:
#             raise ValueError("Model is not defined.")
#         self.model_name = model_name
#         self.openai_model=ChatOpenAI(model=self.model_name)
        
#     def get_model(self):
#         return self.openai_model

# if __name__ == "__main__":
#     llm_instance = LLMModel()  
#     llm_model = llm_instance.get_model()
#     response=llm_model.invoke("hi")

#     print(response)






import os
from dotenv import load_dotenv
from functools import wraps
from langchain_groq import ChatGroq
from groq import RateLimitError
from functools import wraps
from dotenv import load_dotenv
# Load environment variables
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
os.environ["GROQ_API_KEY"] = GROQ_API_KEY

def retry_with_exponential_backoff(func, max_retries=3, base_delay=1):
    @wraps(func)
    def wrapper(*args, **kwargs):
        retries = 0
        while retries < max_retries:
            try:
                return func(*args, **kwargs)
            except RateLimitError as e:
                delay = base_delay * (2 ** retries)
                print(f"RateLimitError: {e}. Retrying in {delay} seconds...")
                time.sleep(delay)
                retries += 1
        raise Exception("Max retries exceeded after RateLimitError.")
    return wrapper

class LLMModel:
    def __init__(self, model_name="llama-3.1-8b-instant"):
        if not model_name:
            raise ValueError("Model is not defined.")
        self.model_name = model_name
        self.groq_model = ChatGroq(model=self.model_name)

    @retry_with_exponential_backoff
    def get_model(self):
        return self.groq_model

if __name__ == "__main__":
    llm_instance = LLMModel()
    llm_model = llm_instance.get_model()
    response = llm_model.invoke("hi")

    print(response)
