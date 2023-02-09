import praw, json

username = ''
password = ''
client_id = ''
client_secrets = ''
user_agent = f'linux:MySearchApp:0.1 (by {username})'

subreddits = ''
keywords = ''

with open('config.json') as f:
    content = json.load(f)

    username = content['username']
    password = content['password']
    client_id = content['client_id']
    client_secret = content['client_secret']
    subreddits = content['subreddits'] if len(content['subreddits'].split(',')) > 1 else 'all'
    keywords = content['keywords'] if len(content['keywords'].split(',')) > 1 else ''

reddit_client = praw.Reddit(client_id=client_id, 
    client_secret=client_secret, 
    user_agent=user_agent,
)

subreddits = subreddits.replace(',', '+')
keywords_set = set(keywords.lower().split(','))

total = 'total'
results = {total: 0}
all_posts = []

# The following code was implemented to refrain from using the following functionality as I felt it was cheating:
# https://praw.readthedocs.io/en/stable/code_overview/models/subreddit.html#praw.models.Subreddit.search
# Increasing the limit will increase the number of Reddit posts that will be returned
for submission in reddit_client.subreddit(subreddits).new(limit=100):
    subreddit = submission.subreddit_name_prefixed
    title = submission.title
    title_set = set(title.lower().split())
    if(keywords_set.intersection(title_set) or len(keywords) == 0):
        if(subreddit in results):
            results[subreddit] = results.get(subreddit) + 1
        else:
            results.update({subreddit: 1})
        
        results[total] = results.get(total) + 1
        all_posts.append([title, submission.author])

for result in results:
    print(f'{result} Count: {results[result]}')

for post in all_posts:
    print(post)
