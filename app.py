from flask import Flask, request, jsonify, render_template
import os
import dialogflow
import requests
import json
import logging

app = Flask(__name__)

app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.ERROR)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/webhook', methods=['POST'])
def webhook():
    reply = {
        "fulfillmentText": "Sorry what was that again?",
    }

    return jsonify(reply)


'''
@app.route('/medicare', methods=['POST'])
def get_medicare_detail():
    medicare_detail = requests.get('https://data.medicare.gov/resource/av4g-y8dz.json').content
    medicare_detail = json.loads(medicare_detail)
    req_dict = json.loads(request.data)
    #intent = req_dict["result"]["metadata"]["intentName"]
    #print(req_dict )
    
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

@app.route('/joke', methods=['POST'])
def get_joke():
    joke = requests.get('https://08ad1pao69.execute-api.us-east-1.amazonaws.com/dev/random_joke').content
    joke = json.loads(joke)
    
    response =  """
        Joke : {0}<br>
        """.format(joke['setup'], )
    
    reply = {
        "fulfillmentText": response,
    }

    return jsonify(reply)
'''

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
    
    print(response.query_result.intent.display_name)
    return response.query_result.fulfillment_text

@app.route('/test', methods=['POST'])
def test():
    joke = requests.get('https://08ad1pao69.execute-api.us-east-1.amazonaws.com/dev/random_joke').content
    joke = json.loads(joke)
    
    response =  """
        Joke : {0}<br>
        """.format(joke['setup'], )
    
    reply = {
        "fulfillmentText": response,
    }

    return jsonify(reply)



# run Flask app
if __name__ == "__main__":
    app.run()