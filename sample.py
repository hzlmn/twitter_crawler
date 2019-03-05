import requests

TWITTER_CONSUMER_KEY = '8GiMi5BBvnjdDo8OF0HtymrKo'
TWITTER_CONSUMER_SECRET = '7Mbhp7N02x7xoGv9qfir1sk9UQ25QUwCEn6zQ3hiqmb1js6wkh'

if __name__ == '__main__':
    token_request: requests.Response = requests.post(
        url='https://api.twitter.com/oauth2/token',
        data={'grant_type': 'client_credentials'},
        auth=(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET),
        headers={'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'},
    )
    token: str = token_request.json().get('access_token', '')

    tweets_data_request: requests.Response = requests.get(
        url='https://api.twitter.com/1.1/search/tweets.json',
        headers={'Authorization': f'Bearer {token}'},
        params={'q': 'Joe Rogan', 'count': 10},
    )
    first_tweet: dict = tweets_data_request.json()
    print(first_tweet)
