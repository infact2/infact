# InFact

Repo to get news from NewsAPI and corroborate it using openai API

## Kill Instructions

**IMPORTANT**: In case the Flask server is still up, but you cant Ctrl+C out of it, please follow the instructions or you will die.

1. Run `sudo ps -a` for a list of processes
2. Find the PID of python
3. `sudo kill {the PID you found above}`

### or
```docker stop --signal SIGKILL newssite```

## Install requirements
Have docker and see Deploy Server for instructions
`pip install -r requirements.txt`

## Deploy server
1. git clone
2. Use cd to the dir. where the main.py file resides
3. run ```docker build -t newssite . ```
4. run ```docker run --name newsSite -d newssite```
5. To stop the program run ```docker stop --signal SIGKILL newssite```

## Documentation

### `extractText(url)`

Extract text from a news article provided in the URL parameter

#### Usage
`extractText("https://www.cnn.com/2023/11/29/politics/vivek-ramaswamy-aide-trump-campaign/index.html")`

#### Returns
A `string` containing all the content of the news article. May not always be accurate

#### Parameters
url `string` - The URL you dipshit








### `corroborate(url1, url2)`

Corroborate two news sources with the two URLs provided

#### Usage
`corroborate("https://www.cnn.com/2023/11/29/politics/vivek-ramaswamy-aide-trump-campaign/index.html", "https://abcnews.go.com/US/fbi-investigating-south-carolina-couple-accused-harassing-neighbors/story?id=105825286")`

#### Returns
A `string` containing the corroborated content, may take a while to finish.

#### Parameters
url1, url2 `string` - The URL you dipshit







### `textToHTML(text)`

Edits text for HTML support

#### Usage
`textToHTML("There is a newline\n\nCrazy.") # Returns "There is a newline<br><br>Crazy."`

#### Returns
A `string` containing HTML-ified stuff.

#### Parameters
text `string` - A string of stuff to convereturttttt
