# LLM_topic_modelling
A project to look into topic modelling using LLM exclusively

#### Description

An llm (Large language model) is assesssed for its usefulness in topic modelling.
This project demonstrates LLMs can be useful when  used with appropriate prompting techniques. Sppecifically this project used hotel review data which has proved difficult to apply more traditional approaches of topic modelling to (such as Bertopic).

Approaches such as Bertopic have proved to be useful in certain contexts but can also:
1. Generate topics with hard to understand labels and  overlapping topics
2. Lack semantic understanding of the data which makes topic identification sub-optimal
3. Produce poor results on certain document types , such as short reviews.




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