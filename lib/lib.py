# Main module for all sentzi classes
 
# `Sentzi` is a web app that generates a visualized output of product reviews through sentiment analysis.

from textblob import TextBlob
import typing

# json and csv lib
import json
import csv

class Sentiment:
    """ Represents a sentiment object """
    
    __emojiDic__ = {
        'positive' : [
            '🙂','😊','😀','👍','😄' ,'😁','😍','🥰','😘','😗'
        ],
        'negative' : [
            '😞','😒','😔','👎','😟','😠','😡','😥','😧','❌'
        ],
        'neutral' : [
            '😐','😶','😑'
        ]
    }
    def __init__(self, text : str):
        """
        Initializes a Sentiment object with the given text .  

        - Note that the accuracy increases as number of words increases. 
        
        `Args`
        ------
        `text` to analyse . 
        """
        self.text = text

        # get sentiment 
        blob = TextBlob(text)
        
        # Analyze sentiment
        sentiment = blob.sentiment
        polarity  = sentiment.polarity

        self.polarity = polarity
    
    def __repr__(self) -> str:
        """ Returns a string representation of the `Sentiment` object """
        return f"""Sentiment(
                score : {self.polarity}
                text  : {self.text}
        )"""

    def get(self) -> typing.Dict[str , typing.Any]:

        # check is its positive negative or neutral
        if self.polarity < 0:
            # negative
            data = {
                'score' : self.polarity,
                'level' : 'negative',
                'emojis' : Sentiment.__emojiDic__['negative']
            }
        elif self.polarity > 0:
            # positive
            data = {
                'score' : self.polarity,
                'level' : 'positive',
                'emojis' : Sentiment.__emojiDic__['positive']
            }
        else:
            # neutral
            data = {
                'score' : self.polarity,
                'level' : 'neutral',
                'emojis' : Sentiment.__emojiDic__['neutral']
            }
        
        return data

def writeCSV(header : list[str],dataList : list[list[str]]):
    with open(r"temp.csv", 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(header)
        # write multiple rows
        writer.writerows(dataList) # write content

def writeJSON(data : dict):
    with open(r"temp.json","w") as json_file:
        json.dump(
            data,
            json_file,
            indent=4,
            sort_keys=True
        )
