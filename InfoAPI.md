# API HIMYM **DOCUEMENTATION**

#### This API was created to access or modify certain information of the How I Met Your Mother data base I created. It is specially interesting the sentiment analysis endpoints, where you are able to analyze the sentiment of the frases said by a specific character in a specific episode.

![alt text](https://i.gifer.com/origin/88/88906c7c19b03dba4a3606d9d70aa543.gif "Logo Title Text 1")

## Endpoints:
We are going to have two type of endpoints, the Get and the Post
   
   ### GET:
   * With this endpoints we can get all the phrases of one character, or all the phrases in the TV show:
   
   #### **Get all the phrases in the TV show for each character:**
    /frasesbycharacter/<nombre>
   The paramater that you need to pass is a character name (nombre).
   
  #### **Get all the phrases in the TV show:**
    /todaslasfrases
    
  ### POST:
  * With this endpoint we will be able to add a phrase, given the phrase the character, the name of the episode, and the season. The information needs to be passed in a dictionary format:
  
  #### **Adds a new phrase to the data base:**
    /nuevafrase
    
  ### SENTIMENT ANALYSIS:
  * With these endpoints, we will be able to analyze the embedded sentiment in the phrases that are said by the different characters.It will recieve a number that measures the positiveness or negativeness of each phrase.
  
  #### **Get the sentiment of all the phrases from one character in one episode:** 
    /sentiment/<personaje>/<episodio>
  The parameters that you need to pass are a character (personaje) and episode (episodio).
