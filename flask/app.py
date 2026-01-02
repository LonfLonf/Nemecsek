import json
from flask import Flask, render_template, request

app = Flask(__name__)

NMAP_SCAN_FILE = "./cache/nmapScan.json"
FFUF_OUTPUT_FILE = "./cache/ffufOut.json"

@app.route("/")
def home():
    with open(NMAP_SCAN_FILE, "r", encoding="utf-8") as f:
        dataNMAP = json.load(f)
    
    with open(FFUF_OUTPUT_FILE, "r", encoding="utf-8") as f:
        dataFFUF = json.load(f)
        
    ffuf_results = dataFFUF["results"]
    nmap_results = dataNMAP["nmaprun"]["host"]["ports"]["port"]

    return render_template("home.html", nmap_results=nmap_results, ffuf_results=ffuf_results)

@app.route("/post", methods=["POST"])
def post():
    return "POST request received"

if __name__ == "__main__":
    app.run(debug=True, port=1111)
