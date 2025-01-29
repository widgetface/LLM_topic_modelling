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
