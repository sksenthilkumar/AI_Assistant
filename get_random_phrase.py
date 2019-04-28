import random
import spacy
import pandas as pd
import json
import numpy as np
from spacy import displacy
from spacy.tokenizer import Tokenizer

print("loading en_core")
nlp = spacy.load('en_core_web_lg')
print("completed the loading")

def random_phrase():
    nouns = ("puppy", "car", "rabbit", "girl", "monkey")
    verbs = ("runs", "hits", "jumps", "drives", "barfs")
    adv = ("crazily.", "dutifully.", "foolishly.", "merrily.", "occasionally.")
    adj = ("adorable", "clueless", "dirty", "odd", "stupid")
    num = random.randrange(0, 5)
    ran_pha = (nouns[num] + ' ' + verbs[num] + ' ' + adv[num] + ' ' + adj[num])
    return(ran_pha)


def query_this(request):
    '''
    Input: Request that is the query given by the mechanic
    Output: Response given after the query has been classified
    '''

    order_responses = [
                   "I have ordered it for you. Thank you!",
                   "Your order is accepted.  Thank you for choosing GC Group.",
                   "Thank you! Your order has been placed. Have a nice day!"
                   ]

    status_responses = [
                       "I am currently waiting for more information from the manufacturer regarding your order. I shall contact you as soon as I have more information.",
                       "The order will be dispatched from the warehouse today. Have a nice day."
                   ]

    delivery_responses = [
                       "Your order will reach you in 2 days.",
                       "The order will be delivered today.",
                       "I just checked your order number. The order will be delivered on 5th February 2019.",
                        "The product is out for delivery. It will reach you today. Thank you for choosing GC Group."
                      ]

    rate_responses = [
                       "Thank you for choosing GC Group. The final price for the requested order is 200 EURO",
                       "Thank you for choosing GC Group. The best price for your order is 400 EURO."
                    ]

    query_to_check = nlp(request)
    combined = []
    for token in query_to_check:
       # do not check the punctuation and determiner(the)
       if token.dep_ != "det" and token.dep_ !="punct" and token.dep_ !="intj":
           # get the children and parents of the token
           token_children = [child for child in token.children if child.dep_!="det" and child.dep_!="punct"]
           token_ancestors = [ancestor for ancestor in token.ancestors if ancestor.dep_!="det" and ancestor.dep_!="punct"]

           combined = combined + token_children + token_ancestors

    combined = set(combined)

    # for status
    status_similarities = [(word.similarity(nlp(u"status")) + word.similarity(nlp(u"situation")) + word.similarity(nlp(u"condition")))/3 for word in combined if word.pos_ == "NOUN"]
    # for delivery
    delivery_similarities = [(word.similarity(nlp(u"arrive")) + word.similarity(nlp(u"travel")) + word.similarity(nlp(u"reach")))/3 for word in combined if word.pos_ == "VERB"]
    # for price/rate
    price_similarities = [(word.similarity(nlp(u"dollar")) + word.similarity(nlp(u"euro")) + word.similarity(nlp(u"cost")))/3 for word in combined if word.pos_ == "NOUN"]
    # for order
    order_similarities = [(word.similarity(nlp(u"ordered")) + word.similarity(nlp(u"place")) + word.similarity(nlp(u"book")))/3 for word in combined if word.pos_ == "VERB"]

    displacy.render(query_to_check.ents, style='ent', jupyter=True)
    try:
        what_query = [max(delivery_similarities), max(status_similarities), max(price_similarities), max(order_similarities), 0.000000000000]
    except ValueError as e:
        print("Value Error")
        what_query = [0,0,0,0,1]

    print(what_query)
    query_str = ["Delivery info", "Current status", "Best price", "New order", "invalid"]
    type_of_query = query_str[np.argmax(what_query)]
    print(type_of_query)
    if type_of_query == "Delivery info":
        print("dl")
        response = delivery_responses[np.random.randint(0,len(delivery_responses))]
    elif type_of_query == "Current status":
        print("cs")
        response = status_responses[np.random.randint(0,len(status_responses))]
    elif type_of_query == "Best price":
        response = rate_responses[np.random.randint(0,len(rate_responses))]
    elif type_of_query == "New order":
        response = order_responses[np.random.randint(0,len(order_responses))]
    elif type_of_query == "invalid":
        print("in")
        response = "Sorry, I couldn't understand you. Can you try again please"

    return response