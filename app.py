from flask import Flask, render_template, request,jsonify
import numpy as np
import pickle
import json

__data_columns=None
__model=None

def estimated_price(airline, source, destination, additional_info, total_stops, day_of_journey,
                    month_of_journey, dep_hr, dep_min):
    xy = np.zeros(len(__data_columns))
    try:
        loc_ind = __data_columns.index(airline.lower())
    except:
        loc_ind=-1


    if loc_ind >= 0:
        xy[loc_ind] = 1

    while source is not None:
        if source == 'Banglore':
            xy[11] = 0
            break
        elif source == 'Kolkata':
            xy[11] = 3
            break
        elif source == 'Delhi':
            xy[11] = 2
            break
        elif source == 'Chennai':
            xy[11] = 1
            break
        else:
            xy[11] = 4
            break

    while destination is not None:
        if destination == 'Banglore':
            xy[12] = 0
            break
        elif destination == 'Kolkata':
            xy[12] = 4
            break
        elif destination == 'Delhi':
            xy[12] = 2
            break
        elif destination == 'Cochi':
            xy[12] = 1
            break
        else:
            xy[12] = 3
            break

    while additional_info is not None:
        if additional_info == 'other':
            xy[13] = 3
            break
        elif additional_info == 'meal_not_included':
            xy[13] = 2
            break
        elif additional_info == 'Business class':
            xy[13] = 0
            break
        else:
            xy[13] = 1
            break

    xy[14] = total_stops
    xy[15] = day_of_journey
    xy[16] = month_of_journey
    xy[17] = dep_hr
    xy[18] = dep_min

    return round(__model.predict([xy])[0])


def load_artifacts():
    global __data_columns
    global __model

    with open('./artifacts/column.json','r') as f:
        __data_columns= json.load(f)['data_columns']
    with open('./artifacts/airline_model.pickle','rb') as g:
        __model=pickle.load(g)

app = Flask(__name__)
@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/math', methods=['POST'])
def predict():
    if request.method == 'POST':
        airline = request.form['air_li']
        source = request.form['source']
        destination = request.form['destination']
        additional_info = request.form['add_inf']
        total_stops = request.form['t_s']
        day_of_journey = request.form['day_j']
        month_of_journey = request.form['month_j']
        dep_hr = request.form['dep_hr']
        dep_min = request.form['dep_min']

        result = estimated_price(airline, source, destination, additional_info, total_stops, day_of_journey,
                                 month_of_journey, dep_hr, dep_min)
        #result2=[airline, source, destination, additional_info, total_stops, day_of_journey,
                                # month_of_journey, dep_hr, dep_min ,result]

        statement='Price ={}' \
                  ',airline= {} ,source= {},destinantion= {},additional_info= {},total stops {},day of journey={},month ={},dep_hour={},dep_min={}'.format(result,airline, source, destination, additional_info, total_stops, day_of_journey,
                                 month_of_journey, dep_hr, dep_min ,result)

    return render_template('index.html', prediction= statement)


if __name__ == '__main__':
    load_artifacts()
    app.run(debug=True, port=5000)
