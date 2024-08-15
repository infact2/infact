import json

sources_newsapi = []

def handleSourceName(original):
    # replace spaces w/ dashes and makes everything lowercase
    result = original.replace(" ", "-").lower()
    # remove "digital"
    result = result.replace("-digital", "")
    # remove any parantheses text (they're usually useless)
    for i in range(len(result) - 2):
        if result[i:i + 2] == "-(":
            result = result[:i]
            break

    result = result.replace("!", "")
    
    return result

def getSourceNamesQuery():
    if len(sources_newsapi) == 0:
        with open("media_bias.json", "r") as file:
            media_bias_data = json.load(file)
            for key in media_bias_data:
                for source in media_bias_data[key]:
                    # print(f"{source['name']} -> {handleSourceName(source['name'])}")
                    sources_newsapi.append(handleSourceName(source['name']))
    result = ""
    for source in sources_newsapi:
        result += source + ","

    return result[:-1]

print(getSourceNamesQuery())