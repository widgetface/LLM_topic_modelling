import csv
import json
from typing import List
import nltk
import pandas as pd

from nltk.tokenize import TweetTokenizer
from guardrails import Guard
from pydantic import BaseModel, Field
from guardrails.hub import RegexMatch

from components import pipeline, struct_logger
from validators import input_validator

TOPIC_REGEX = "^\w+(_\w+)?$"
COMMENT_REGEX = "\w+"
SENTIMENT_REGEX = "^(positive|negative|neutral)+$"

MODEL = "llama3.2:latest"
DATA_FILE_PATH = "./data/small_test.csv"
LOG_FILE_PATH = "./logs/app_logs.jsonl"
RESULTS_FILE_PATH = "./data/results"


logger = struct_logger.create_logger(LOG_FILE_PATH)

query = """
List the topics contained in the text provided. 
Each topic should have a maximum of two words separated by an underscore.
list the topics as JSON objects JSON format with the key 'topic' and value being the topic name. a key 'comments' with value of the text being looked at 
and a key 'sentiment' wuth a value  of the sentiment of the text. 
Ignore your own knowledge.
If you cannot answer the question say "I don't know"

AND RESPONSE 
[
  {
    "topic": "hotel_location",
    "comment": "Handy location for the train to the airport and for access around the city.", 
    "sentiment": "positive" 
  },
  {
    "topic": "hotel_staff",
    "comment": "The bar was always busy with good staff and bar meals were good quality.",
    "sentiment": "positive" 
  },
  {
    "topic": "hotel_facilities",
    ""comment": "There was a gym and pool downstairs but I never got that far (!!) although colleagues did say they were good.",
      sentiment: "negative"}
    }
Ignore your own knowledge.
If you cannot answer the question say 'NA'
ONLY RETURN THE JSON REQUESTED AND NOTHING ELSE

"""

tokenizer_words = TweetTokenizer()
p = pipeline.ReviewDatasetPipeline(model=MODEL, template=template)
results = []

input_guard = Guard().use(input_validator.InputValidator(on_fail="exception"))


class JSON_RESPONSE(BaseModel):
    topic: str = Field(validators=[RegexMatch(regex=TOPIC_REGEX)])
    comment: str = Field(validators=[RegexMatch(regex=COMMENT_REGEX)])
    sentiment: str = Field(validators=[RegexMatch(regex=SENTIMENT_REGEX)])


output_guard = Guard.for_pydantic(JSON_RESPONSE)


def process_row(values, df_index):
    [text, id, post_date] = values
    sentences = [tokenizer_words.tokenize(t) for t in nltk.sent_tokenize(text)]
    for sentence in sentences:
        sentence = " ".join(sentence)
        try:
            input_guard.validate(sentence, metadata={"index": df_index})
            best_result = p.run(text=sentence, query=query)[0]
            print(best_result, type(best_result))

            # output_guard.validate(json.loads(str(best_result)))
            # write_to_file(best_result)
        except Exception as e:
            print(e)
            logger.error(f"Error:{e}", status="failed validation", id=id, text=text)


def write_to_file(
    results: List[JSON_RESPONSE], file_path=RESULTS_FILE_PATH, file_type="jsonl"
):
    print(f"write to file {results}")
    if len(results) > 0:
        with open(f"{file_path}_{MODEL}.{file_type}", "a") as file:
            file.write(results + "\n")


df = pd.read_csv(DATA_FILE_PATH)[["text", "hotel_id", "post_date"]]
df.apply(
    lambda row: process_row(values=row.values, df_index=df.index),
    axis=1,
)
