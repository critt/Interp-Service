FROM python:3.10-bookworm
ENV GOOGLE_SERVICE_JSON_FILE=google-services.json

COPY requirements.txt .
RUN pip install -r requirements.txt
COPY google-services.json .
COPY ./src ./src

EXPOSE 8080

CMD ["python", "src/app.py"]

# docker build -t tsi-feb7 . && docker run -it -p 8080:8080 --name tsc-feb7 tsi-feb7
# docker container rm tsc-feb7 && docker image rm tsi-feb7

# docker build --platform linux/amd64,linux/arm64 -t tsi2 . 
# docker tag e2d059d76f8d us-west2-docker.pkg.dev/omega-dahlia-394021/tsi/backend-image
# docker push us-west2-docker.pkg.dev/omega-dahlia-394021/tsi/backend-image 