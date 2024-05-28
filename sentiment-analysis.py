import tweepy
from textblob import TextBlob
import re
import matplotlib.pyplot as plt


class Sentiment():

    def __init__(self):
        self.tweets = []
        self.tweet_text = []

    def get_data(self):
        # Connect to Tweepy API
        user = 'username'
        secret = 'password'
        token = 'token'
        token_secret = 'token_secret'
        login = tweepy.OAuthHandler(user, secret)
        login.set_access_token(token, token_secret)
        api = tweepy.API(login)

        # Ask user to input keyword and number of tweets to scrape, then scrapes the tweets
        keyword = input('Enter Keyword to scrape: ')
        num_tweets = int(input('Enter number of tweets to scrape: '))
        self.tweets = tweepy.Cursor(api.request, q=keyword, lang="en").items(num_tweets)

        # Initialize sentiment variables and use TextBlob to assign sentiment to each tweet

        strongly_positive = 0
        positive = 0
        somewhat_positive = 0
        neutral = 0
        negative = 0
        somewhat_negative = 0
        strongly_negative = 0
        polarity = 0

        for tweet in self.tweets:
            self.tweet_text.append(self.clean_tweets(tweet.text).encode('utf-8'))
            text = TextBlob(tweet.text)
            polarity += text.sentiment.polarity

            if 0.3 < text.sentiment.polarity <= 0.6:
                positive += 1
            elif 0.6 < text.sentiment.polarity <= 1:
                strongly_positive += 1
            elif 0 < text.sentiment.polarity <= 0.3:
                somewhat_positive += 1
            elif text.sentiment.polarity == 0:
                neutral += 1
            elif -0.3 < text.sentiment.polarity <= 0:
                somewhat_negative += 1
            elif -0.6 < text.sentiment.polarity <= -0.3:
                negative += 1
            elif -1 < text.sentiment.polarity <= -0.6:
                strongly_negative += 1

        # Calculate the sentiment percentages and print

        strongly_positive_percentage = self.percentage(strongly_positive, num_tweets)
        positive_percentage = self.percentage(positive, num_tweets)
        somewhat_positive_percentage = self.percentage(somewhat_positive, num_tweets)
        neutral_percentage = self.percentage(neutral, num_tweets)
        negative_percentage = self.percentage(negative, num_tweets)
        somewhat_negative_percentage = self.percentage(somewhat_negative, num_tweets)
        strongly_negative_percentage = self.percentage(strongly_negative, num_tweets)

        # # Plot a pie chart visualization of sentiments

        self.plot_chart(keyword, num_tweets, strongly_positive_percentage, positive_percentage,
                        somewhat_positive_percentage, neutral_percentage, negative_percentage,
                        somewhat_negative_percentage, strongly_negative_percentage)

    def percentage(self, num, total):
        percent = 100 * float(num) / float(total)
        return f'{percent:.2f}'

    def clean_tweets(self, tweet):
        return ' '.join(re.sub('@#%&<>/`~', ' ', tweet).split())

    def plot_chart(self, keyword, num_tweets, strongly_positive, positive, somewhat_positive,
                   neutral, negative, somewhat_negative, strongly_negative):

        labels = [f'Strongly Positive: {strongly_positive}%',
                  f'Positive: {positive}%', f'Somewhat Positive: {somewhat_positive}%',
                  f'Neutral: {neutral}%', f'Negative: {negative}%', f'Somewhat Negative: {somewhat_negative}%',
                  f'Strongly Negative: {strongly_negative}%']

        # Associate sentiment with respective colors
        categories = [strongly_positive, positive, somewhat_positive, neutral, strongly_negative, negative,
                      somewhat_negative]
        colors = ['green', 'mediumseagreen', 'yellowgreen', 'gray', 'red', 'lightsalmon', 'salmon']

        patches, text = plt.pie(categories, colors=colors, startangle=90)
        plt.legend(patches, labels, loc='best')
        plt.title(f'Sentiment analysis on {keyword} using {num_tweets} tweets.')
        plt.axis('equal')
        plt.tight_layout()
        plt.show()


if __name__ == "__main__":
    model = Sentiment()
    model.get_data()
