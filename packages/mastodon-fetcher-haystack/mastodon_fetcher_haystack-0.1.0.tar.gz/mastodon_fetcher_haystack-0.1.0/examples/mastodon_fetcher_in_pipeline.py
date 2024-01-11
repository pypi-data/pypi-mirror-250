import os
from dotenv import load_dotenv
from mastodon_fetcher_haystack.mastodon_fetcher import MastodonFetcher
from haystack import Pipeline
from haystack.components.generators import OpenAIGenerator
from haystack.components.builders import PromptBuilder

load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
mastodon_fetcher = MastodonFetcher()

prompt_template="""Given the follwing Mastodon posts stream, create a short summary of the topics the account posts about. Mastodon posts stream: {{ documents }};\n Answer:"""
prompt_builder = PromptBuilder(template = prompt_template)
llm = OpenAIGenerator(api_key=OPENAI_API_KEY)

pipe = Pipeline()
pipe.add_component("fetcher", mastodon_fetcher)
pipe.add_component("prompt_builder", prompt_builder)
pipe.add_component("llm", llm)

pipe.connect("fetcher.documents", "prompt_builder.documents")
pipe.connect("prompt_builder.prompt", "llm.prompt")
result = pipe.run(data = {"fetcher": {"username": "annthurium@tech.lgbt", "last_k_posts": 3}})
print(result['llm']['replies'][0])