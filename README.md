# LLM_topic_modelling
A project to look into topic modelling using LLM exclusively. Given growth of online social network platforms and data arising from them, finding topic modelling approaches that handle these types of corpus effectively ould be useful.

#### Description
Topic modeling can become a competitive advantage for organisations, seeking to utilize NLP techniques for improved understanding of their customers or processes and use such data for predictive analysis, opinion monitoring ,  trend analysis and applied research.

In this project a llm (Large language model) is assesssed for its usefulness in topic modelling.

This project demonstrates LLMs can be useful when  used with appropriate prompting techniques. Sppecifically this project used hotel review data which has proved difficult to apply more traditional approaches of topic modelling to (such as Bertopic).

Approaches such as Bertopic have proved to be useful in certain contexts but can also:
1. Generate topics with hard to understand labels and  overlapping topics
2. Lack semantic understanding of the data which makes topic identification sub-optimal
3. Produce poor results on certain document types , such as short reviews.

This may be due to:

A corpus of short texts which often contain multiple topics, like hotel reviews, 
provide a limited context for understanding of the topics contained within the text. 

Bertopic relies on embeding based models which are trained on corpuses with longer texts (contexts).

Extensive  manipulation and refinement of tool parameters is required to produce useful results, which is often manual and requires time-consuming fine-tuning of model parameters. Topic modelling tools lack hyper-parameter optimization tools like [Optuna](https://optuna.org/) for LLM's.

Often human experts are required to refine topic modelling results to make them more human readable.

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