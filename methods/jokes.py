import requests

def GetJoke(argument, argument2):
    contains = False
    number = False
    url = "https://v2.jokeapi.dev/joke/Any?lang=fr&format=txt"
    arguments = [argument,argument2]
    for i in range(0,len(arguments)):
        if arguments[i].isalpha() and not contains:
            url+="&contains="+arguments[i]
            contains = True
        elif arguments[i].isnumeric() and not number:
            url +="&amount="+arguments[i]
            number = True
    r = requests.get(url)
    joke = r.content.decode('utf-8')
    return joke