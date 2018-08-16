from flask import Flask, request, jsonify, render_template
import os
import dialogflow
import requests
import json
import pusher

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/medicare', methods=['POST'])
def get_medicare_detail():
    medicare_detail = requests.get('https://data.medicare.gov/resource/av4g-y8dz.json').content
    medicare_detail = json.loads(medicare_detail)
    
    response =  """
        Measure 1 : {0}<br>
        Measure 2: {1}<br>
        Measure 3: {2}<br>
        Measure 4: {3}<br>
        Measure 5: {4}<br>
        """.format(medicare_detail[0]['asc1_measure_nat_rate'], medicare_detail[0]['asc2_measure_nat_rate'], medicare_detail[0]['asc3_measure_nat_rate'], medicare_detail[0]['asc4_measure_nat_rate'], medicare_detail[0]['asc5_measure_nat_rate'])
    
    reply = {
        "fulfillmentText": response,
    }
    

    #data = jsonify(medicare_detail)
    return jsonify(reply)
    #return dict(data)

@app.route('/send_message', methods=['POST'])
def send_message():
    message = request.form['message']
    project_id = os.getenv('DIALOGFLOW_PROJECT_ID')
    fulfillment_text = detect_intent_texts(project_id, "unique", message, 'en')
    response_text = { "message":  fulfillment_text }

    return jsonify(response_text)

def detect_intent_texts(project_id, session_id, text, language_code):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)

    if text:
        text_input = dialogflow.types.TextInput(
            text=text, language_code=language_code)
        query_input = dialogflow.types.QueryInput(text=text_input)
        response = session_client.detect_intent(
            session=session, query_input=query_input)

    return response.query_result.fulfillment_text    

# run Flask app
if __name__ == "__main__":
    app.run()