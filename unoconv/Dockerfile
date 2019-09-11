FROM debian:buster-slim

RUN apt-get update \
 && apt-get install -y unoconv \
 && rm -rf /var/lib/apt/lists/*

CMD /bin/sh -c "while true; do unoconv --server 0.0.0.0 --port 2002  --listener; done"
