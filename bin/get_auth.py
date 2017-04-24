import tweepy

consumer_token = "HD1ymMHAGyVtASCX3cYINu2Zf"
consumer_secret = "VNxozUhB7NmVgxrjnAaShJRUAHKq6rekmzuOl1nwZaeRR7DO7p"

auth = tweepy.OAuthHandler(consumer_token, consumer_secret)

try:
    redirect_url = auth.get_authorization_url()
except tweepy.TweepError:
    print("Error! Failed to get request token.")

verifier = raw_input('Verifier:')

try:
    auth.get_access_token(verifier)
except tweepy.TweepError:
    print("Error! Failed to get access token.")

new_token = auth.access_token
print new_token
new_secret = auth.access_token_secret
print new_secret
