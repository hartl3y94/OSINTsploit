from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, EntitiesOptions, KeywordsOptions

def analyze_text(text_input):
    authenticator = IAMAuthenticator('l9NWdTYKZXM643V695dRc5Ocs2JoX0UxTy86iZ-JXKFM')
    natural_language_understanding = NaturalLanguageUnderstandingV1(
        version='2019-07-12',
        authenticator=authenticator
    )
    
    natural_language_understanding.set_service_url('https://api.eu-gb.natural-language-understanding.watson.cloud.ibm.com/instances/5827912a-2547-4ee1-b399-78209798cea3')
    
    response = natural_language_understanding.analyze(
        text=text_input,
        features=Features(
            entities=EntitiesOptions(emotion=True, sentiment=True, limit=10),
            keywords=KeywordsOptions(emotion=True, sentiment=True,limit=10))).get_result()
    emotions_dict={'sadness': 0, 'joy': 0, 'fear': 0, 'disgust': 0, 'anger': 0,'confidence':0}
    c=0
    for i in response["keywords"]:
        c=c+1
        emotions_dict['sadness']+=i["emotion"]['sadness']
        emotions_dict['joy']+=i["emotion"]['joy']
        emotions_dict['fear']+=i["emotion"]['fear']
        emotions_dict[ 'disgust']+=i["emotion"][ 'disgust']
        emotions_dict['anger']+=i["emotion"]['anger']
    emotions_dict['sadness']/=c
    emotions_dict['joy']/=c
    emotions_dict['fear']/=c
    emotions_dict[ 'disgust']/=c
    emotions_dict['anger']/=c
    for i in response["entities"]:
        emotions_dict['confidence']+=i["confidence"]
    emotions_dict['confidence']/=c
    return(emotions_dict)

def analyze_url(url_input):
    authenticator = IAMAuthenticator('l9NWdTYKZXM643V695dRc5Ocs2JoX0UxTy86iZ-JXKFM')
    natural_language_understanding = NaturalLanguageUnderstandingV1(
        version='2019-07-12',
        authenticator=authenticator
    )
    
    natural_language_understanding.set_service_url('https://api.eu-gb.natural-language-understanding.watson.cloud.ibm.com/instances/5827912a-2547-4ee1-b399-78209798cea3')
    
    response = natural_language_understanding.analyze(
        url=url_input,
        features=Features(
            entities=EntitiesOptions(emotion=True, sentiment=True, limit=1000),
            keywords=KeywordsOptions(emotion=True, sentiment=True,limit=1000))).get_result()
    emotions_dict={'sadness': 0, 'joy': 0, 'fear': 0, 'disgust': 0, 'anger': 0,'confidence':0}
    c=0
    for i in response["keywords"]:
        c=c+1
        emotions_dict['sadness']+=i["emotion"]['sadness']
        emotions_dict['joy']+=i["emotion"]['joy']
        emotions_dict['fear']+=i["emotion"]['fear']
        emotions_dict[ 'disgust']+=i["emotion"][ 'disgust']
        emotions_dict['anger']+=i["emotion"]['anger']
    emotions_dict['sadness']/=c
    emotions_dict['joy']/=c
    emotions_dict['fear']/=c
    emotions_dict[ 'disgust']/=c
    emotions_dict['anger']/=c
    for i in response["entities"]:
        emotions_dict['confidence']+=i["confidence"]
    emotions_dict['confidence']/=c
    return(emotions_dict)



'''
sample input
text='IBM is an American multinational technology company '
        'headquartered in Armonk, New York, United States, '
        'with operations in over 170 countries.'
'''        
