import os

from flask import Flask, request, jsonify


from db import Base, engine
from resources.session import Voting_Session as VotingSession
from resources.vote import Vote
import json
from google.cloud import pubsub_v1

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
    
    req_data = request.get_json()
    vote, status = Vote.create(req_data, s_id)

    if status == 200:
        json_stored_created_vote = json.loads(vote.get_data())

        publisher = pubsub_v1.PublisherClient()
        topic_path = publisher.topic_path("votingadaproject", "voting_session")
        data = [
            {
                "vote": json_stored_created_vote['id'],
                "party_member": json_stored_created_vote['member_uuid'],
                "voter_uuid": json_stored_created_vote['uuid'],
                "status": "pending"
            }
        ]
        data = json.dumps(data).encode("utf-8")
        future = publisher.publish(topic_path, data)

        try:
            future.result()  # see https://docs.python.org/3/library/concurrent.futures.html
        except Exception as ex:
            return jsonify('topic message not send'), 500
        return jsonify({"message": f'Vote with ID {json_stored_created_vote["id"]} created'}), 200
    else:
        return vote



if __name__ == '__main__':
    app.run(port=int(os.environ.get("PORT", 3003)), host='0.0.0.0', debug=True)
