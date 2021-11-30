from flask import Flask, request
import src.SQLtools as sql
from flask import jsonify
import markdown.extensions.fenced_code

app = Flask(__name__)

@app.route('/')
def index():
    readme_file = open("InfoAPI.md")
    template = markdown.markdown(readme_file.read(), extensions = ["fenced_code"])
    return template

@app.route("/frasesbycharacter/<nombre>")
def phrase_by_char(nombre):
    frases = sql.frasecita(nombre)
    return frases

@app.route("/todaslasfrases")
def todasfrases():
    frases = sql.frase()
    return frases

@app.route("/frases/<name>")
def frases(name):
    frasecitas = sql.lasfrases(name)
    return jsonify(frasecitas)

@app.route("/nuevafrase", methods=["POST"])
def mensajito():
    frase = request.form.get("frase")
    personaje = request.form.get("personaje")
    Temporada= request.form.get('Temporada')
    episodio= request.form.get('episodio')
    print(frase, personaje,Temporada, episodio)

    return sql.nuevomensaje(frase, personaje,Temporada, episodio)

@app.route("/sentiment/<personaje>/<episodio>")
def sentiment(personaje, episodio):
    sentiment = sql.quote_sent(personaje, episodio)
    return str(sentiment)







if __name__ == '__main__':
    app.run(debug=True)