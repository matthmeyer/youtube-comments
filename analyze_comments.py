import os
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow
import spacy
import collections
import csv

# Feel free to use other language models than the German one https://spacy.io/usage/models
nlp = spacy.load('de_core_news_sm', disable=['textcat'])
nlp.vocab.add_flag(lambda s: s.lower() in spacy.lang.de.stop_words.STOP_WORDS, spacy.attrs.IS_STOP)


# The CLIENT_SECRETS_FILE variable specifies the name of a file that contains
# the OAuth 2.0 information for this application, including its client_id and
# client_secret.
CLIENT_SECRETS_FILE = "client_secret.json"

# This OAuth 2.0 access scope allows for full read/write access to the
# authenticated user's account and requires requests to use an SSL connection.
SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'

def get_authenticated_service():
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
    return build(API_SERVICE_NAME, API_VERSION, developerKey='***INSERT YOUR DEVELOPER KEY HERE***')


def channels_list_by_username(service, user):
    # Get a playlist from the user that contains all uploaded videos
    results = service.channels().list(part='contentDetails', id=user).execute()

    playlistId = results['items'][0]['contentDetails']['relatedPlaylists']['uploads']

    all_comments = []
    all_lemmas = []

    playlistitems_left = True
    next_playlistitem_PageToken = None
    id_counter = 0

    # Loop through the user's playlist to get the id of each video 
    while playlistitems_left == True:
        playlist_items = service.playlistItems().list(part='snippet', playlistId=playlistId, pageToken=next_playlistitem_PageToken).execute()

        if 'nextPageToken' in playlist_items:
            next_playlistitem_PageToken = playlist_items['nextPageToken']

        else:
            playlistitems_left = False

        playlistitems_left = False

        for playlist_item in playlist_items['items']:
            video_id = playlist_item['snippet']['resourceId']['videoId']

            comments_left = True
            next_comment_PageToken = None

            while comments_left == True:
                try:
                    comment_threads = service.commentThreads().list(part='snippet',videoId=video_id, pageToken=next_comment_PageToken).execute()

                    if 'nextPageToken' in comment_threads:
                        next_comment_PageToken = comment_threads['nextPageToken']

                    else:
                        comments_left = False

                    # Loop through all the comments, tokenize and lemmatize them with SpaCy
                    for comment in comment_threads['items']:
                        all_comments.append(comment['snippet']['topLevelComment']['snippet']['textOriginal'])
                        doc = nlp(comment['snippet']['topLevelComment']['snippet']['textOriginal'])

                        for token in doc:

                            # Ignore all tokens that are stop words, punctuation or space
                            if token.is_stop == False and token.is_punct == False and token.is_space == False:
                                lemma = token.lemma_
                                all_lemmas.append(token.lemma_)

                # In case comments are disabled for this video, continue with the next one
                except HttpError:

                    comments_left = False

    # Get the frequency of each lemmatized word
    counter = collections.Counter(all_lemmas)
    return counter, all_comments


if __name__ == '__main__':
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    service = get_authenticated_service()

    # List of user ids that shall be analyzed
    username_list = ['UC4teOyQNXzMH94YMYySl9mA']
    username_list = ['UCASLfWxw8atzwL3ymPeuv2Q']

    for user in username_list:
        counter, all_comments = channels_list_by_username(service, user)

        # Write the result to a csv file
        with open('wordlist_%s.csv' % user, 'w', newline='', encoding='utf-8') as csvfile:
            csvwriter = employee_writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

            for el in counter.most_common():
                csvwriter.writerow(el)


        print('User: %s, Found comments: %s' % (user, len(all_comments)))
