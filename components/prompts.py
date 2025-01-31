template = """  
Give the following information, answer the question from the information present in this text: {{text}}.
Question={{query}}?
"""

query = """
List the topics contained in the text provided.
The topic name should be a category for the specific topic some examples are:
Example:

Input: "The poor sound insulation mean't could hear a lot of street noise in my room ."
Expected Output: "noise"

Example:

Input: "The mattress was old and I could feel the springs as I sat on the side of the bed."
Expected Output: "bedroom"

Example:

Input: "The restaurant is a pleasant addition !!"
Expected Output: "food"

Example:

Input: "The toilet was not working"
Expected Output: "bathroom"

Your resonse should be in JSON.
The  JSON format has the key 'topic' and value being the topic name. a key 'comments' with value of the text being looked at 
and a key 'sentiment' with a value  of the sentiment of the text. 
If you cannot answer the question say set the topic name to 'na' and sentiment to 'na'.

AND RESPONSE 
  {
    'topic': 'location',
    'comment': 'Handy location for the train to the airport and for access around the city.', 
    'sentiment': 'positive'
  },
  {
    'topic': 'staff',
    'comment': 'The bar was always busy with good staff and bar meals were good quality.',
    'sentiment': 'positive' 
  },
  {
    'topic': 'gym',
    'comment': 'There was a gym and pool downstairs but I never got that far (!!) although colleagues did say they were good.',
    'sentiment': 'neutral'}
    }

Ignore your own knowledge.
Only return JSON.

"""
