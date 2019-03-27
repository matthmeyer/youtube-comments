## youtube-comments
Analyze all videos of a specific user and get the most common words in a csv file.

## Description
This little tool uses the YouTube v3 api to go through all videos of a specified user, receive all comments made and analyze the most common words. Words are lemmatized and stop words are sorted out with the natural language processing tool SpaCy. The most common words and all the comments are saved to seperate csv files.

## Prerequisites
- Google APIs Client Library for Python (pip install google-api-python-client)
- Google Auth OAuthLib (pip install google-auth-oauthlib)
- SpaCy (pip install spacy)
- A working SpaCy language model (python -m spacy download de)

## Google API
__Important:__ You need a file named __client_secret.json__ in the same directory. The file contains your credentials to use the Google API. You can learn more about how to get your credentials here: https://developers.google.com/youtube/v3/quickstart/python#step_1_turn_on_the_api_name. Furthermore, you have to replace the developerKey by a custom key. You can get this key in the Google Developers Console, too.

## Rate Limiting
The YouTube v3 api has a rate limiting (https://developers.google.com/youtube/v3/getting-started#quota). I recommend to inform yourself about the quota YouTube provides before you start. This script may use up your entire quota and may take up much time for YouTube accounts with millions of comments.

## Language
Please note that I wrote this tool for German YouTube channels. This is why I use the German language model from SpaCy. Feel free to use another model (for more information see: https://spacy.io/usage)
