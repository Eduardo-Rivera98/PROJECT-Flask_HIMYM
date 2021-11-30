from config import engine
import pandas as pd
from textblob import TextBlob
import spacy
import re
from nltk.corpus import stopwords





def tokenizer(txt):
    """
    Transforms a text, taking out meaningless words, and converting the rest to its original form 
    Args:
        txt: any text
    Returns:
        A list with the tokenized words
    """
    nlp = spacy.load("en_core_web_sm")
    tokens = nlp(txt)
    filtradas = []
    
    for word in tokens:
        if not word.is_stop:
            lemma = word.lemma_.lower().strip()
            if re.search('^[a-zA-Z]+$',lemma):
                filtradas.append(lemma)
            
    return " ".join(filtradas)


def polarity(frase):
    """
    Gets the sentiment of a phrase 
    Args:
        A phrase
    Returns:
        A measure of positiveness or negativeness of the phrase using TextBlob
    """

    blob = TextBlob(f"{frase}")
    
    return blob.sentiment[0]

def check(que,string):
    """
    Función parametrizada que comprueba en cada tabla si existe el user, artista o canción.
    Devuelve True si existe y False si no
    """
    if que== 'personaje':
        query =list(engine.execute(f"SELECT Nombre FROM personaje WHERE Nombre = '{string}'"))
        if len(query) > 0:
            return True
        else:
            return False
    if que == "temporada":
        query = list(engine.execute(f"SELECT NumeroTemp FROM temporada WHERE NumeroTemp = '{string}'"))
        if len(query) > 0:
            return True
        else:
            return False
    elif que == "nombre_episodio":
        query = list(engine.execute(f"SELECT Nombre FROM episodio WHERE Nombre = '{string}'"))
        if len(query) > 0:
            return True
        else:
            return False
    elif que == "frase":
            query = list(engine.execute(f"SELECT Frase FROM frase WHERE Frase = '{string}'"))
            if len(query) > 0:
                return True
            else:
                return False

def frasecita(personaje):
    """
    Query the db for existence of a character and returns all its phrases 
    Args:
        character: name of the character
    Returns:
        A json format dataframe with all the phrases from that character.
    """

    if check('personaje', personaje):
        query = list(engine.execute(f"SELECT idPersonaje FROM personaje WHERE `Nombre` = '{personaje}'"))
        c = query[0][0]
    else: 
        return "The character doesn't exist or match with the ones in the db"
    
    query = f"""
    SELECT Frase FROM frase
    WHERE (Personaje_idPersonaje= {c})
    """
    datos = pd.read_sql_query(query,engine)

    return datos.to_json(orient="records")

def frase():
    query= f""" 
    SELECT Frase FROM frase
    """
    datos= pd.read_sql_query(query,engine)
    return datos.to_json(orient= 'records')

def traduce(x):
    import time
    time.sleep(1)
    texto = TextBlob(x)
    traducido = f"{texto.translate(from_lang='en', to='es')}"
    return traducido 


def lasfrases(personaje):
    if check('personaje', personaje):
        query = list(engine.execute(f"SELECT idPersonaje FROM personaje WHERE `Nombre` = '{personaje}'"))
        c = query[0][0]
    else: 
        return "The character doesn't exist or match with the ones in the db"
    
    query = f"""
    SELECT Frase 
    FROM frase 
    WHERE (Personaje_idPersonaje= {c});
    """

    eldata = pd.read_sql_query(query,engine)
    
    eldata['Frase'] = eldata.Frase.apply(traduce)        
    return eldata.to_json(orient="records")

def nuevomensaje(frase,personaje, Temporada, episodio):

    query = list(engine.execute(f"SELECT idPersonaje FROM personaje WHERE Nombre = '{personaje}'"))
    c = query[0][0]
    query1= list(engine.execute(f"SELECT idTemporada FROM temporada WHERE NumeroTemp = '{Temporada}'"))
    e= query1[0][0]
    query2= list(engine.execute(f"SELECT idEpisosio FROM episodio WHERE Nombre = ' {episodio}'"))
    r= query2[0][0]
   
    engine.execute(f"""
    INSERT INTO frase (Personaje_idPersonaje,Frase, Episosio_idEpisosio, Temporada_idTemporada)
    VALUES ('{c}', '{frase}', '{r}', '{e}');
    """)
    
    return f"Se ha introducido correctamente:  {personaje} {frase} {Temporada} {episodio}"

def quote_sent(personaje, episodio):
    """
    Gets the sentiment of a phrase in the database, for an especific character and episode
    Args:
        character: name of the character
        episode: name of the episode
    Returns:
        A list with the measures of positivness or negativness for the phrases
    """
    query = list(engine.execute(f"SELECT idPersonaje FROM personaje WHERE `Nombre` = '{personaje}'"))
    c = query[0][0]
    query = list(engine.execute(f"SELECT idEpisosio FROM episodio WHERE Nombre = ' {episodio}'"))
    e = query[0][0]
    
    query = f"""
    SELECT * FROM frase
    WHERE (Personaje_idPersonaje = {c} AND Episosio_idEpisosio = {e})
    """
    datos = pd.read_sql_query(query,engine)

    polarities = []
    for i in datos['Frase']:
        t = tokenizer(i)
        p = polarity(t)
        polarities.append(p)
        
    return polarities