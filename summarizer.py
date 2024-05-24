import bs4 as bs
import urllib.request
import re
import nltk
import os
from gtts import gTTS
nltk.download('punkt')
nltk.download('stopwords')
import transformers
from transformers import pipeline
from youtube_transcript_api import YouTubeTranscriptApi

"""**WEB SCRAPPING FUNCTION**"""

def web_scrapping(link):
  scraped_data = urllib.request.urlopen(link)
  article = scraped_data.read()

  parsed_article = bs.BeautifulSoup(article,'lxml')

  paragraphs = parsed_article.find_all('p')

  article_text = ""

  for p in paragraphs:
      article_text += p.text
  article_text = re.sub(r'\[[0-9]*\]', ' ', article_text)
  article_text = re.sub(r'\s+', ' ', article_text)
  formatted_article_text = re.sub('[^a-zA-Z]', ' ', article_text )
  formatted_article_text = re.sub(r'\s+', ' ', formatted_article_text)
  sentence_list = nltk.sent_tokenize(article_text)
  stopwords = nltk.corpus.stopwords.words('english')

  word_frequencies = {}
  for word in nltk.word_tokenize(formatted_article_text):
      if word not in stopwords:
          if word not in word_frequencies.keys():
              word_frequencies[word] = 1
          else:
              word_frequencies[word] += 1
      maximum_frequncy = max(word_frequencies.values())
  for word in word_frequencies.keys():
      word_frequencies[word] = (word_frequencies[word]/maximum_frequncy)
      sentence_scores = {}
  for sent in sentence_list:
      for word in nltk.word_tokenize(sent.lower()):
          if word in word_frequencies.keys():
              if len(sent.split(' ')) < 30:
                  if sent not in sentence_scores.keys():
                      sentence_scores[sent] = word_frequencies[word]
                  else:
                      sentence_scores[sent] += word_frequencies[word]
  import heapq
  summary_sentences = heapq.nlargest(7, sentence_scores, key=sentence_scores.get)

  summary = ' '.join(summary_sentences)
  return summary

"""**TEXT SUMMARIZATION**"""

import nltk
def text_summarization(article_text):
  article_text = re.sub(r'\[[0-9]*\]', ' ', article_text)
  article_text = re.sub(r'\s+', ' ', article_text)
  formatted_article = re.sub('[^a-zA-Z]', ' ', article_text)
  formatted_article = re.sub(r'\s+', ' ', formatted_article)
  tokenize_sentence = nltk.sent_tokenize(article_text)
  stopwords = nltk.corpus.stopwords.words('english')
  word_frequency = {}
  for word in nltk.word_tokenize(formatted_article):
      if word not in stopwords:
          if word not in word_frequency.keys():
              word_frequency[word] = 1
          else:
              word_frequency[word] += 1
  maximum_frequency = max(word_frequency.values())
  for word in word_frequency.keys():
      word_frequency[word] = (word_frequency[word] / maximum_frequency)
      #Sentence score
  sentence_score = {}
  for sent in tokenize_sentence:
      for word in nltk.word_tokenize(sent.lower()):
          if word in word_frequency.keys():
              if len(sent.split(' ')) < 30:
                  if sent not in sentence_score.keys():
                      sentence_score[sent] = word_frequency[word]
                  else:
                      sentence_score[sent] += word_frequency[word]
  import heapq
  sentence_summary = heapq.nlargest(7, sentence_score, key = sentence_score.get)
  summary = ' '.join(sentence_summary)
  return summary

"""**YOUTUBE TRANSCRIPT SUMMARIZATION**"""

from IPython.display import YouTubeVideo

summarizer = pipeline('summarization')

def youtube_summarization(youtube_video):
  video_id = youtube_video.split("=")[1]

  YouTubeVideo(video_id)

  YouTubeTranscriptApi.get_transcript(video_id)
  transcript = YouTubeTranscriptApi.get_transcript(video_id)

  result = ""
  for i in transcript:
    result += ' ' + i['text']

  num_iters = int(len(result)/1000)
  summarized_text = []
  for i in range(0, num_iters + 1):
    start = 0
    start = i * 1000
    end = (i + 1) * 1000
    out = summarizer(result[start:end])
    out = out[0]
    out = out['summary_text']
    summarized_text.append(out)

  summary= str(summarized_text)
  return summary

"""**TEXT TO SPEECH**"""

def text_to_speech(text):
    tts = gTTS(text)
    filename = "output.mp3"
    filepath = os.path.join("static", filename)
    tts.save(filepath)
    return filename

def play_audio(filename):
    os.system(f"start {filename}")

"""**MAIN FUNCTION CALLING**"""

def main():
    print("Welcome to the model selector program!")
    print("1. WEB SCRAPPING")
    print("2. TEXT SUMMARIZATION")
    print("3. YOUTUBE TRANSCRIPT SUMMARIZATION")
    choice = input("Please enter your choice (1/2/3): ")

    if choice == '1':
      link=str(input())
      summary=web_scrapping(link)
      print(summary)
    elif choice == '2':
      text=str(input())
      summary=text_summarization(text)
      print(summary)
    elif choice == '3':
      video_link=str(input())
      summary=youtube_summarization(video_link)
      print(summary)
    else:
        print("Invalid choice. Please enter 1/2/3: ")

    listen=input("want to listen audio: ")
    if listen=="yes":
      audio_file = text_to_speech(summary)
      play_audio(audio_file)

if __name__ == "__main__":
    main()

