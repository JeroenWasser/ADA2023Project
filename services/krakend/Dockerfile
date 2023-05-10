FROM devopsfaith/krakend

# Copy the KrakenD configuration file into the container
COPY krakend.json /etc/krakend/krakend.json

# Expose the port on which KrakenD will listen
EXPOSE 8080

# Set the entrypoint command to start KrakenD
CMD ["/usr/local/bin/krakend", "run", "-c", "/etc/krakend/krakend.json"]
