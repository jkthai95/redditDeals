import praw


class RedditParser:
    def __init__(self, subreddit):
        # Title of subreddit
        self.subreddit = subreddit

        # Maximum no. of submissions to parse
        self.limit = 3


        print("(RedditParser) Initialized for %s." % subreddit)

    def acquire_titles(self):
        # TODO: Acquire login from GUI
        # For now, we acquire username and password from a file.
        with open('./redditLogin', 'r') as fp:
            username = fp.readline().strip()
            password = fp.readline().strip()

        # Acquire submissions from subreddit
        reddit = praw.Reddit(client_id='2jCK-om4rxiEqA',
                             client_secret='h5AGIO8gQOlYPm0DuNXuFSnLouQ',
                             user_agent='Reddit Deals',
                             redirect_uri="http://localhost:8080",
                             username=username,
                             password=password)

        submissions = reddit.subreddit(self.subreddit).new(limit=self.limit)
        for submission in submissions:
            print('Title: {}, ups: {}, downs: {}, Have we visited?: {}'.format(submission.title,
                                                                               submission.ups,
                                                                               submission.downs,
                                                                               submission.visited))

