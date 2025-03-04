# Interp-Service
A python web app that brokers acces to certain speech-related Google AI services


#### Features
- Authentication with Firebase Auth
- Enumeration of available languages
- WebSockets channels for transcribing and translating audio data

#### Google Cloud APIs used and required
- [Cloud Speech-to-Text API](https://cloud.google.com/speech-to-text/?hl=en)
- [Cloud Translation API](https://cloud.google.com/translate?hl=en)
- [Firebase Auth](https://firebase.google.com/docs/auth/)

#### Prerequisites
- Docker
- GCP account with [Cloud Speech-to-Text API](https://cloud.google.com/speech-to-text/?hl=en), [Cloud Translation API](https://cloud.google.com/translate?hl=en), and [Firebase Auth](https://firebase.google.com/docs/auth/) enabled
- A service account with read access to those APIs and a JSON credentials file
 
#### Instructions
1. Enable all of those APIs in your GCP project. Make sure to enable Firebase Auth in your Firebase project
   - Below is a quick, safe Firebase Auth configuration for playing around with this system. All of these options are available in the setup wizard when you initially enable Auth:
     - enable only email/password auth
     - manually create a user
     - disable user creation via the API
2. Create a service account with access to these APIs. Download its credentials file and put it in the root of this project with the name `google-services.json`
3. Build the image and run it in a container:
```bash
$ docker build -t <image_name> . && docker run -it -p 8080:8080 --name <image_name> <container_name>
```
4. Confirm its running and available (should return a list of languages):
```bash
$ curl http://<ip_appdress>:8080/getSupportedLanguages
```
