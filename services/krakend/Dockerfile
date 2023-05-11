FROM devopsfaith/krakend

# Copy the KrakenD configuration file into the container
COPY krakend.json /etc/krakend/krakend.json

# Expose the port on which KrakenD will listen
EXPOSE 8090

# # Set the entrypoint command to start KrakenD
# ENTRYPOINT [ "/usr/bin/krakend" ]
# CMD [ "run", "-c", "/etc/krakend/krakend.json" ]