__author__ = 'shivangi'
from textblob import TextBlob


class analysis():

    def sentiment_percent(pos, neg, neu):
        global sent
        global result
        total = pos + neg + neu
        if pos > neg and pos > neu:
            sent = "Positive"
            try:
                result = pos / total * 100
            except:
                print("An error occurred")
        elif neg > pos and neg > neu:
            sent = "Negative"
            try:
                result = neg / total * 100
            except:
                print("An error occurred")
        else:
            sent = "Neutral"
            try:
                result = neu / total * 100
            except:
                print("An error occured")
        return sent,result


