# Interp-Service
A python web app that brokers acces to certain speech-related Google AI services.
Features:
- Authentication with Firebase Auth
- Enumeration of available languages
- WebSockets channels for transcribing and translating audio data

Google Cloud APIs used and required:
- [Cloud Speech-to-Text API](https://cloud.google.com/speech-to-text/?hl=en)
- [Cloud Translation API](https://cloud.google.com/translate?hl=en)
- [Firebase Auth](https://firebase.google.com/docs/auth/)

Prerequisites:
- Docker
- GCP account with [Cloud Speech-to-Text API](https://cloud.google.com/speech-to-text/?hl=en), [Cloud Translation API](https://cloud.google.com/translate?hl=en), and [Firebase Auth](https://firebase.google.com/docs/auth/) enabled
- A service account with read access to those APIs and a JSON credentials file
 
Instructions:
1. Enabled all of those APIs in your GCP project and enable Firebase Auth in your Firebase project
   - For a quick, safe configuration enable only email/password auth and manually create a user during this step
2. Create a service account with access to these APIs. Download its credentials file and put it in the root of this project with the name `google-services.json`
3. Build the image and run it in a container:
```bash
$ docker build -t <image_name> . && docker run -it -p 8080:8080 --name <image_name> <container_name>
```
4. Confirm its running and available (should return a list of languages):
```bash
$ curl https://<ip_appdress>:8080/getSupportedLanguages
```
