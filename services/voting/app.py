import os

from flask import Flask, request, jsonify


from db import Base, engine
from resources.session import Voting_Session as VotingSession
from resources.vote import Vote


app = Flask(__name__)
app.config["DEBUG"] = True
Base.metadata.create_all(engine)


@app.route('/sessions', methods=['GET'])
def get_voting_sessions():
    return VotingSession.get()

@app.route('/sessions/latest', methods=['GET'])
def get_current_sessions():
    return VotingSession.get_latest_session()

@app.route('/sessions', methods=['POST'])
def create_session():
    req_data = request.get_json()
    return VotingSession.create(req_data)

@app.route('/votes/sessions/<s_id>', methods=['GET'])
def getVotes(s_id):
    try:
        s_id = int(s_id)
    except ValueError:
        return jsonify('id must be an integer', 500)
    return Vote.get_for_session(s_id)

@app.route('/votes/sessions/<s_id>', methods=['POST'])
def placeVote(s_id):
    try:
        s_id = int(s_id)
    except ValueError:
        return jsonify('id must be an integer', 500)
    #ToDo: Add notification create call for confirmation email
    req_data = request.get_json()
    return Vote.create(req_data, s_id)



if __name__ == '__main__':
    app.run(port=int(os.environ.get("PORT", 3003)), host='0.0.0.0', debug=True)
