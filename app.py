from flask import Flask, render_template, request
from calculate import scoreList
#from views import views

app = Flask(__name__)
#app.register_blueprint(views, url_prefix = "/views")

@app.route("/", methods = ["GET", "POST"])
def home():
    if request.method == "POST":
        startingHand = []
        isDealer = True
        if request.form.get("dealer") == "No":
            isDealer = False

        fkeys = list(request.form.keys())
        fkeys.pop()
        for key in fkeys:
            ranknsuit = key.split('_')
            startingHand.append((int(ranknsuit[0]), int(ranknsuit[1])))

        print(startingHand)
        print(isDealer)
        # return render_template("results.html", scores = scoreList(startingHand, isDealer))
        #return render_template_string('index.html', score = scoreList(startingHand, isDealer))
        #return render_template('index.html', scores = scoreList(startingHand, isDealer))
        return scoreList(startingHand, isDealer)
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug = True, port = 8000)



# formerly views.py
# from flask import Blueprint, render_template

# views = Blueprint(__name__, "views")

# @views.route("/")
# def home():
#     return render_template("index.html", name="bunko paraszt")



# formerly results.hmtl
# <!DOCTYPE html>
# <html lang="en">
# 	<head>
# 		<title></title>
    
# 	</head>
# 	<body>
# 		<table id = 'table-results'>
# 			<tr>
# 			  <th>Kept</th>
# 			  <th>Sent to Crib</th>
# 			  <th>Expected Value</th>
# 			</tr>
# 			{% for item in scores: %}
# 			  <tr>
# 				<td>
# 				  <div class = "tablesets">
# 					{% for card in item[0]: %}
# 					  {% set source = "../images/playing_cards/" + ranks[card[0] - 1] + "_of_" + suits[card[1]] + ".png" %}
# 					  <div class = "card"><img src = {{source}}></img></div>
# 					{% endfor %}
# 				  </div>
# 				</td>
# 				<td>
# 				  <div class = "tablesets">
# 					{% for card in item[1]: %}
# 					  {% set source = "../images/playing_cards/" + ranks[card[0] - 1] + "_of_" + suits[card[1]] + ".png" %}
# 					  <div class = "card"><img src = {{source}}></img></div>
# 					{% endfor %}
# 				  </div>
# 				</td>
# 				<td>
# 				  {% set score = item[2]|round(2) %}
# 				  {{score}}
# 				</td>
# 			  </tr>
# 			{% endfor %}
# 		</table>
# 	</body>
# </html>