# LLM_topic_modelling
A project to look into topic modelling using LLM exclusively

#### Prerequisites

1. Ollama

#### Main dependencies:

1. [Haystack](https://haystack.deepset.ai/)
2. [Haystack Ollama](https://haystack.deepset.ai/integrations/ollama) , to run models locally
3. [Ollama](https://github.com/ollama/ollama)

#### Notes
1. I use the nltk TweetTokenizer to get better results tokenizing my data (usually I'd use Spacy)
2. I use [structlog](https://www.structlog.org/en/stable/) to give structured logs
3. I used [gaurdrails-ai](https://www.guardrailsai.com/) to create guardrials