import os

from flask import Flask, request

from db import Base, engine
from resources.party import Party

app = Flask(__name__)
app.config["DEBUG"] = True
Base.metadata.create_all(engine)


# @app.route('/parties', methods=['POST'])
# def create_party():
#     req_data = request.get_json()
#     return VotingSession.create(req_data)


# @app.route('/parties/<p_id>/admin', methods=['POST'])
# def create_party_admin(p_id):
#     return Delivery.get(d_id)

@app.route('/sessions', methods=['GET'])
def get_voting_sessions():
    return Party.get()

if __name__ == '__main__':
    app.run(port=int(os.environ.get("PORT", 3000)), host='0.0.0.0', debug=True)
