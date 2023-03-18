import os
from flask import Flask, request, jsonify, render_template, redirect,url_for
from flask_cors import CORS, cross_origin
from restaurant.pipeline.single_prediction import start_single_prediction


os.putenv('LANG', 'en_US.UTF-8')
os.putenv('LC_ALL', 'en_US.UTF-8')

app = Flask(__name__)
CORS(app)


@app.route("/", methods=['GET'])
@cross_origin()
def home():
    return render_template('index.html')


# @app.route("result/<predicted_rating>")
# @cross_origin
# def result(predicted_rating):
#     return render_template('prediction.html')


@app.route("/predict", methods=['GET','POST'])
@cross_origin()
def predict():
    if request.method=='POST':
        has_table_booking = request.form['hasTableBooking'].upper()
        if(has_table_booking=='YES'):
            has_table_booking='Yes'
        else:
            has_table_booking='No'
        
        has_online_delivery = request.form['hasOnlineDelivery'].upper()
        if(has_online_delivery=='YES'):
            has_online_delivery='Yes'
        else:
            has_online_delivery='No'

        avg_cost_for_two = request.form['avgCost']
        price_range = request.form['priceRange']
        votes = request.form['votes']
        user_input = [[votes, avg_cost_for_two, has_table_booking, has_online_delivery, price_range]]
        predicted_rating = start_single_prediction(input=user_input)
        predicted_rating = round(predicted_rating,2)
        input_with_rating = [votes, avg_cost_for_two, has_table_booking, has_online_delivery, price_range, predicted_rating]
        return render_template('prediction.html',input_with_rating=input_with_rating)
    return render_template('index.html')




if __name__ == "__main__":
    # clApp = ClientApp()
    app.run(host='0.0.0.0', port=8080)