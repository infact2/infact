# InFact

Repo to get news from NewsAPI and corroborate it using openai API

> [!WARNING]
> If you are not using docker please follow the next section.
## Docker Related Instructions

### To kill
run `sudo docker stop --signal SIGKILL infact`

### Prepare files for docker to builf
1. Obtain the repo `git clone https://github.com/infact2/infact`
2. Insert your tokens in .env

### Building the image
3. Build the docker image by using `sudo docker build -t infact . `

### Local debugging instructions
4. Run the image `sudo docker run --name infact -it -p 8000:8000 infact`
5. To stop the program run `sudo docker stop --signal SIGKILL infact`

### Server Deployment Instructions
> [!NOTE]
> This is only for deploying to a server where the image run in detached mode (ie: no commnad line args).
4. Run the image `sudo docker run --name infact -d -p 8000:8000 infact`
5. To stop the program run `sudo docker stop --signal SIGKILL infact`


## Legacy Instructions (Still supported)

### To Kill
**IMPORTANT**: In case the Flask server is still up, but you cant Ctrl+C out of it, please follow the instructions or you will die.
1. Run `sudo ps -a` for a list of processes
2. Find the PID of python
3. `sudo kill {the PID you found above}`

### or
```docker stop --signal SIGKILL infact```

## Install requirements
Have docker and see Deploy Server for instructions
`pip install -r requirements.txt`

## Deploy server
1. git clone
2. Use cd to the dir. where the main.py file resides
3. run ```docker build -t infact . ```
4. run ```docker run --name infact -d infact```
5. To stop the program run ```docker stop --signal SIGKILL infact```
=======
### Install requirements
Have docker and see Deploy Server for instructions
`pip install -r requirements.txt`

### Deploy server
`python main.py` or`python3 main.py`


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
