
import os, sys
from flask import Flask, render_template, redirect, request, jsonify 
import json
import pandas as pd
from flask_cors import CORS

# --------------------------
# $$$$$$$ API (FLASK GET) $$$$$$$$
# --------------------------


app=Flask(__name__)
CORS(app)

@app.route("/")
def landing_page():
    return render_template('bienvenidx.htm')

@app.route('/datos', methods=['GET'])
def get_json():

    def cargar_preguntas(tot,cantidad=10):
        juego=pd.read_json(tot).sample(n=cantidad,axis=1)
        juego.to_json(tot[4:])
        juego=tot[4:]
        with open (juego,"r") as json_file_readed:
            peticion=json.load(json_file_readed)
        return json.dumps(peticion)

    if "juego" in request.args:
        play=request.args["juego"]
        return cargar_preguntas(tot="data/tot_"+play+".json")
    else:
        return render_template('bienvenidx.htm')


# -------------------------------
# $$$$$$$ SERVIDOR FLASK $$$$$$$$
# -------------------------------

def main():
    
    print("STARTING PROCESS")
    #print(os.path.dirname(__file__))
    

    #settings_file = os.path.dirname(__file__) + "\settings.json" # puede que esto sea sin barras
    with open("settings/settings.json", "r") as json_file_readed:
        json_readed = json.load(json_file_readed)

    SERVER_RUNNING = json_readed["server_running"]
    
    if SERVER_RUNNING:
        DEBUG = json_readed["debug"]
        HOST = json_readed["host"]
        #PORT_NUM = json_readed["port"]
        PORT = os.getenv("PORT", 6060)

        app.run(debug=DEBUG, host=HOST, threaded = True,port=PORT)

    else:
        print("Server settings.json doesn't allow to start server. " + 
              "Please, allow it to run it.")
          
if __name__ == "__main__":
    main()