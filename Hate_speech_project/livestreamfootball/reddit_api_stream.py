#!/usr/bin/env python3

# taken from https://towardsdatascience.com/scraping-reddit-data-1c0af3040768
import praw # x https://praw.readthedocs.io/en/latest/getting_started/authentication.html#script-application
import pandas as pd

#authentication
reddit = praw.Reddit(client_id='XXX', client_secret='XXX', user_agent='myBot')

# get 10 new posts from the MachineLearning subreddit

posts = []
ml_subreddit = reddit.subreddit('worldcup')
for post in ml_subreddit.new(limit=2000):
    posts.append([post.title, post.score, post.id, post.subreddit, post.url, post.num_comments, post.selftext, post.created])
posts = pd.DataFrame(posts,columns=['title', 'score', 'id', 'subreddit', 'url', 'num_comments', 'body', 'created'])
print(posts)
posts.to_csv('reddit_stream.csv')

# getting the comments related to the posts above
comments =[]
for id in posts.id:
    submission = reddit.submission(id=id) # or submission = reddit.submission(url=url)

    submission.comments.replace_more(limit=0)
    for comment in submission.comments.list():
        comments.append([comment.body, comment.id, comment.created, id])
        print(comment.body)
comments = pd.DataFrame(comments,columns=['body',  'id', 'created', 'postid'])
comments.to_csv('reddit_comments_stream.csv')