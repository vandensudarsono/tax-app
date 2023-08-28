from flask import Flask, render_template, request, redirect, url_for, jsonify

product = {

}
app = Flask(__name__)

@app.route("/")
def root():
    return render_template('index.html')

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        user = request.form["name"]
        pwd = request.form["pwd"]
        if user == 'edi' and pwd == 'abdullah':
            return redirect('home')
    else:
        return render_template("login.html")

goods = [
    "book",
    "music CD",
    "chocolate bar",
    "box of chocolates",
    "bottle of parfum",
    "packet of headache pills",
]

@app.route("/home")
def home():
    return render_template("home.html", goods=goods)

@app.route("/buy", methods=["POST"])
def buy():
    #get payload data 
    data = request.get_json()
    #declare variables
    priceTaxed = 0.0
    total = 0.0

    if data is not None:
        #get list of goods
        transactions = data["data"]
        item = []
        result = {
            "data":[],
            "tax":0.0,
            "total":0.0,
        }

        for transaction in transactions:
            tax = 0.1
            if bool(transaction.get("imported")) == True:
                tax += 0.05
            item.append({
                "name": transaction.get("name"),
                "qty": transaction.get("qty"),
                "price": transaction.get("price")
            })

            priceTaxed += transaction.get("price") * tax
            total += transaction.get("price") * transaction.get("qty")

        result["data"] = item
        result["tax"] = round(priceTaxed, 2)
        result["total"] = total

    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True,host="0.0.0.0", port=5000)
