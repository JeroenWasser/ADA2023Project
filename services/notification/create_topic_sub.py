from google.cloud import pubsub_v1
import logging

if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    publisher = pubsub_v1.PublisherClient()
    party_managment_topic_path = publisher.topic_path("votingadaproject", "party_managment")
    voting_session_topic_path = publisher.topic_path("votingadaproject", "voting_session")


    party_managment_topic = publisher.create_topic(request={"name": party_managment_topic_path})
    voting_session_topic = publisher.create_topic(request={"name": voting_session_topic_path})

    print(f"Created topic: {party_managment_topic.name}")
    print(f"Created topic: {voting_session_topic.name}")
