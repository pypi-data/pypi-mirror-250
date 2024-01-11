import pytest
import os
from dotenv import load_dotenv
from mastodon_fetcher_haystack.mastodon_fetcher import MastodonFetcher
from haystack import Pipeline
from haystack.components.generators import OpenAIGenerator
from haystack.components.builders import PromptBuilder

load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
mastodon_fetcher = MastodonFetcher()

class TestMastodonFetcher():
    
    @pytest.mark.integration
    def test_mastodon_fetcher(self):
       mastodon_fetcher.run(username="gogs@mas.to")

    @pytest.mark.integration
    def test_mastodon_fetcher_in_pipeline(self):
      prompt_template = "Given the follwing Mastodon posts, indicate whether the account has a positive or negative tone. Mastodon posts {{ documents }}"
      prompt_builder = PromptBuilder(template=prompt_template)
      llm = OpenAIGenerator(api_key=OPENAI_API_KEY)

      pipe = Pipeline()
      pipe.add_component("fetcher", mastodon_fetcher)
      pipe.add_component("prompt_builder", prompt_builder)
      pipe.add_component("llm", llm)

      pipe.connect("fetcher.documents", "prompt_builder.documents")
      pipe.connect("prompt_builder.prompt", "llm.prompt")
      result = pipe.run(data={"fetcher": {"username": "clonehenge@mas.to"}})
      assert "replies" in result["llm"]
