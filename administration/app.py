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

# @app.route('/sessions', methods=['POST'])
# def create_voting_session():
#     status = request.args.get('status')
#     return Status.update(d_id, status)

# @app.route('/sessions/<s_id>', methods=['PUT'])
# def update_voting_session(s_id):
#     return Delivery.delete(d_id)


if __name__ == '__main__':
    app.run(port=int(os.environ.get("PORT", 5000)), host='0.0.0.0', debug=True)
