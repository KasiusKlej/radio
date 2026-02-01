from flask import Flask, render_template , url_for 
app = Flask(__name__)

@app.route("/")
def hello():
    return render_template('test2.html')
    


#(when running script from here from IDE)
if __name__ == "__main__":
    #launch this app like this (or else you can run batch file to launch)
    app.run(debug=True)
    