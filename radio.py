#this serves my homepage at miha.zvezda2.si
from flask import Flask, render_template , url_for 
from cardgames.routes import cardgames_bp
from metropoly.engine.routes import metropoly_bp 
from pingpong.routes import pingpong_bp
from clovek.routes import clovek_bp

import os

# correct way for server
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, "templates")
)

app.secret_key = "428ef008c81fd2d317876eb94ffeb68039d6a0d304b7a9e4cc5a7f47ec5fea00"
app.register_blueprint(cardgames_bp, url_prefix="/cardgames")
app.register_blueprint(metropoly_bp, url_prefix="/metropoly")
app.register_blueprint(pingpong_bp, url_prefix="/pingpong")
app.register_blueprint(clovek_bp, url_prefix="/clovek")


@app.route("/")
def hello():
    return render_template('test2.html')
    
@app.route("/umetnost/film/")
def film():
    return render_template("film.html")


#january 2026
if __name__ == "__main__":
    #launch this app like this (or else you can run batch file to launch)
    app.run(debug=True)
    


    