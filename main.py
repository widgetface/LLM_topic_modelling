import csv
import json
from typing import List
import nltk
import pandas as pd

from nltk.tokenize import TweetTokenizer
from guardrails import Guard, OnFailAction
from pydantic import BaseModel, Field
from guardrails.hub import RegexMatch

from components import pipeline, struct_logger
from validators import input_validator, output_validator
from pydantic import BaseModel


class Review(BaseModel):
    topic: str
    comment: str
    sentiment: str
    id: int
    post_date: str


MODEL = "llama3.2:latest"
DATA_FILE_PATH = "./data/small_test.csv"
LOG_FILE_PATH = "./logs/app_logs.jsonl"
RESULTS_FILE_PATH = "./data/results"


logger = struct_logger.create_logger(LOG_FILE_PATH)

template = """  
Give the following information, answer the question from the information present in this text: {{text}}.
Question={{query}}?
"""

query = """
List the topics contained in the text provided. 
Each topic should have a maximum of two words separated by an underscore.
Your resonse should be in JSON.
The  JSON format has the key 'topic' and value being the topic name. a key 'comments' with value of the text being looked at 
and a key 'sentiment' with a value  of the sentiment of the text. 
If you cannot answer the question say set the topic name to 'na'

AND RESPONSE 
  {
    'topic': 'hotel_location',
    'comment': 'Handy location for the train to the airport and for access around the city.', 
    'sentiment': 'positive'
  },
  {
    'topic': 'hotel_staff',
    'comment': 'The bar was always busy with good staff and bar meals were good quality.',
    'sentiment': 'positive' 
  },
  {
    'topic': 'hotel_facilities',
    'comment': 'There was a gym and pool downstairs but I never got that far (!!) although colleagues did say they were good.',
    'sentiment': 'negative'}
    }

Ignore your own knowledge.
Only return JSON.

"""

tokenizer_words = TweetTokenizer()
p = pipeline.ReviewDatasetPipeline(model=MODEL, template=template)
results = []

input_guard = Guard().use(
    input_validator.InputValidator(on_fail=OnFailAction.EXCEPTION)
)

output_guard = Guard().use(
    output_validator.OutputValidatior(
        pydantic_model=Review, on_fail=OnFailAction.EXCEPTION
    )
)


def process_row(values, df_index):
    [text, id, post_date] = values
    output_metadata = {"id": id, "post_date": post_date}

    sentences = [tokenizer_words.tokenize(t) for t in nltk.sent_tokenize(text)]
    for sentence in sentences:
        sentence = " ".join(sentence)
        try:
            input_guard.validate(sentence, metadata={"index": df_index})
            best_result = p.run(text=sentence, query=query)[0]
            output_guard.validate(str(best_result), metadata=output_metadata)
            result = json.loads(best_result)
            if type(result) == dict:
                result.update(output_metadata)
                write_to_file(str(result))
        except Exception as e:
            logger.error(f"Error:{e}", status="failed validation", id=id, text=text)


def write_to_file(result: dict, file_path=RESULTS_FILE_PATH, file_type="jsonl"):
    with open(f"{file_path}_{MODEL}.{file_type}", "a") as file:
        file.write(result + "\n")


df = pd.read_csv(DATA_FILE_PATH)[["text", "hotel_id", "post_date"]]
df.apply(
    lambda row: process_row(values=row.values, df_index=df.index),
    axis=1,
)
