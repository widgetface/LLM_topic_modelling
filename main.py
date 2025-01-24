import csv
from components import pipeline

MODEL = "llama3.2:latest"  # "llama3.2:latest"ollama run nemotron-mini
FILE_PATH = "./data/data.csv"
template = """  
Give the following information, answer the question from the information present in this text: {{text}}.
Ignore your own knwoledge. If you do not have an answer reply 'NA'
Question={{query}}?
"""
# query = """
# Determine if the text contains a sentiment about the following,
# hotel location,
# hotel room.
# Format your response as a JSON object with the following keys,
# 'location',
# 'location_sentiment',
# 'room',
# 'room_sentiment',
# 'cleaning',
# 'cleaning_sentiment',
# 'food',
# 'food_sentiment'
# 'staff_service',
# 'staff_service_sentiment'
# 'cost',
# 'cost_sentiment',
# 'facilities',
# 'facilities_sentiment',
# 'bed',
# 'bed_sentiment',
# 'wifi',
# 'wifi_sentiment',
# 'noise',
# 'noise_sentiment',
# 'anger_sentiment'
# Any sentiment should be either 'positive', 'neutral' or 'negative'.
# The location key value will be the comment about the location of the hotel and nothing else.
# The location_sentiment key value will be the sentiment of the comment about the location of the hotel and nothing else.
# The room key value will be the comment about the room and nothing else.
# The room_sentiment key value will be the sentiment of the comment about the room and nothing else.
# The cleaning key value will be the comment about any dirt, dirty, soiled, filth, unitidiness, unclean, lack or hygiene, stains in the hotel and nothing else.
# The cleaning_sentiment key value will be the sentiment about any dirt, dirty, soiled, filth, unitidiness, unclean, lack or hygiene, stains  in the hotel and nothing else.
# The food key value will be the comment about the food and nothing else.
# The food_sentiment key value will be the sentiment of the comment about the food and nothing else.
# The staff_service key value will be the comment about the any staff members and nothing else.
# The staff_service_sentiment key value will be the sentiment of the comment about the staff and nothing else.
# The cost key value will be the comment about the price of room or cost of hotel but not about any prices of things outside the hotel and nothing else.
# The cost_sentiment key value will be the sentiment of the price of room and or cost of hotel and nothing else.
# The facilities key value will be the comment about the hotel facilities such as elevator, lift, terrace, jacuzzi, ice machine, sauna, shuttle buses, parking parking area, gym, gymnasium, fitness suite, swimming pool, pool, public area.
# The facilities_sentiment key value will be the sentiment of the hotel facilities such as shuttle buses, parking area, gym, swimming pool, public area.
# The bed key value will be the sentence which must contain the word the words  'bed' or 'beds' or 'duvet' or 'sheet' or 'sheets' or 'mattress' or 'blankets' or 'pillows'  and nothing else otherwise the bed key value is 'unknown'.
# The bed_sentiment key value will be the sentiment of sentence which must contain the word  'bed' or 'beds' or 'pillow menu' or 'duvet' or 'sheet' or 'sheets' or 'mattress' or 'blankets' or 'pillows'  and nothing else. otherwise the bed_sentiment  key value is 'neutral'.
# The wifi key value will be the comment about wifi or internet used in hotel and nothing else.
# The wifi_sentiment key value will be the sentiment about wifi or internet used in hotel and nothing else.
# The noise key value will be the sentence containing the words 'noise' or 'noisy'  and nothing else.
# The noise_sentiment key value will be 'negative' if the sentence contains the words 'noise' or 'noisy'  otherwise it will be 'neutral'.
# The anger_sentiment key value will be the true if the tone  or sentiment of the {{text}} is angry and false if not.
# If the information isn't present, use 'unknown' as the value.
# If the sentiment is isn't present use 'neutral' as the value.
# Just return the JSON object as the answer.
# """

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

p = pipeline.ReviewDatasetPipeline(model=MODEL, template=template)
results = []
with open("./data/test.csv", mode="r") as file:
    # Create a CSV reader object
    csv_reader = csv.DictReader(file)

    # Skip the header row (if there is one)
    next(csv_reader, None)
    count = 0
    # Iterate over each row in the CSV file
    for row in csv_reader:
        if count < 5:
            text = row["text"]
            result = p.run(text=text, query=query)
            if isinstance(result, list):

                results.append(result[0])
            count += 1
            print(text)
            print(count)


print(f"Number of results = {len(results)}")

if len(results) > 0:
    with open(f"./data/results/upated_review_dataset_{MODEL}.json", "w") as file:
        for entry in results:
            file.write(entry)
