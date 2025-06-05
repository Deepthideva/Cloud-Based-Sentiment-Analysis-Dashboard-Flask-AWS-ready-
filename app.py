from flask import Flask, render_template, request
from textblob import TextBlob
import boto3
import datetime

app = Flask(__name__)

# Function to analyze sentiment
def analyze_sentiment(text):
    analysis = TextBlob(text)
    polarity = analysis.sentiment.polarity
    if polarity > 0.1:
        return 'Positive'
    elif polarity < -0.1:
        return 'Negative'
    else:
        return 'Neutral'

# Function to log data to AWS S3
def log_to_s3(text, sentiment):
    s3 = boto3.client('s3')
    bucket_name = 'your-s3-bucket-name'
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"logs/{timestamp}.txt"
    s3.put_object(Bucket=bucket_name, Key=filename, Body=f"Text: {text}\nSentiment: {sentiment}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/result', methods=['POST'])
def result():
    user_text = request.form['text']
    sentiment = analyze_sentiment(user_text)
    log_to_s3(user_text, sentiment)
    return render_template('result.html', text=user_text, sentiment=sentiment)

if __name__ == '__main__':
    app.run(debug=True)
