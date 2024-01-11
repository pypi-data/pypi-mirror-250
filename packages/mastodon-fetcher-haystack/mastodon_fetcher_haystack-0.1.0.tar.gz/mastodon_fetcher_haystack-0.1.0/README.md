![PyPI](https://img.shields.io/pypi/v/mastodon-fetcher-haystack)

# 🎾 MastodonFetcher Node for Haystack

This custom component for Haystack is designed to fetch the latest posts from a given Mastodon username and return the contents as a list of Haystack Documents.
This way, it can be used as a replacement for a retriever node in a pipeline.

## Instllation

### For Haystack 2.0-Beta onwards:
```bash
pip install mastodon-fetcher-haystack
```
### For Haystack 1.x
```bash
pip install mastodon-fetcher-haystack==0.0.1
```

## Usage in Haystack 2.0-Beta onwards

1. The node expects a full Mastodon username as the `username` input. E.g. 'tuana@sigmoid.social'.
2. You can set the number of posts you want to retrieve by setting the `last_k_posts` parameter while initializing the MastodonFetcher, or in the `run` method. This can be a maximum of 40.

```python
from mastodon_fetcher_haystack.mastodon_fetcher import MastodonFetcher

mastodon_fetcher = MastodonFetcher()
mastodon_fetcher.run(username="tuana@sigmoid.social")
```
### In a pipeline

```python
from haystack import Pipeline
from mastodon_fetcher_haystack.mastodon_fetcher import MastodonFetcher
from haystack.components.generators import OpenAIGenerator
from haystack.components.builders import PromptBuilder

prompt_builder = PromptBuilder(template='YOUR_PROMPT_TEMPLATE')
llm = OpenAIGenerator(api_key'YOUR_OPENAI_API_KEY')

pipe = Pipeline()
pipe.add_component("fetcher", mastodon_fetcher)
pipe.add_component("prompt_builder", prompt_builder)
pipe.add_component("llm", llm)

pipe.connect("fetcher.documents", "prompt_builder.documents")
pipe.connect("prompt_builder.prompt", "llm.prompt")
pipe.run(data={"fetcher": {"username": "tuana@sigmoid.social"}})
```

## Usage in Haystack 1.x

1. The node expects a full Mastodon username as the `query` input. E.g. 'tuana@sigmoid.social'.
2. You can set the number of posts you want to retrieve by setting the `last_k_posts` parameter while initializing the MastodonFetcher, or in the `run` method. This can be a maximum of 40.

```python
from mastodon_fetcher_haystack.mastodon_fetcher import MastodonFetcher

mastodon_fetcher = MastodonFetcher()
mastodon_fetcher.run(query="tuana@sigmoid.social")
```
### In a pipeline

```python
from haystack import Pipeline
from mastodon_fetcher_haystack.mastodon_fetcher import MastodonFetcher

mastodon_fetcher = MastodonFetcher(last_k_posts=15)
prompt_node = PromptNode(default_prompt_template="YOUR_PROMPT_TEMPLATE", model_name_or_path="text-davinci-003", api_key="YOUR_API_KEY")

pipeline = Pipeline()
pipeline.add_node(component=mastodon_fetcher, name="MastodonFetcher", inputs=["Query"])
pipeline.add_nide(component=prompt_node, name="PromptNode", inputs=["MastodonFetcher"])
pipeline.run(query="tuana@sigmoid.social")
```
