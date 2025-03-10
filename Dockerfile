FROM python:3.10-bookworm
ENV PYTHONPATH=/src

# Create a directory for logs
RUN mkdir -p /var/log/interp

COPY entrypoint.sh .
RUN chmod +x entrypoint.sh
COPY requirements.txt .
COPY google-services.json .
COPY ./src ./src

RUN pip install -r requirements.txt
EXPOSE 8080
ENTRYPOINT ["/entrypoint.sh"]

###################################
# Running locally:
###################################
# docker container rm tsc-local && docker image rm tsi-local && docker build -t tsi-local . && docker run -it -p 8080:8080 --name tsc-local tsi-local

###################################
# Pushing to GCP Artifact Registry:
###################################
# docker build --platform linux/amd64,linux/arm64 -t tsi . 
# docker tag tsi us-west2-docker.pkg.dev/omega-dahlia-394021/tsi/backend-image
# docker push us-west2-docker.pkg.dev/omega-dahlia-394021/tsi/backend-image