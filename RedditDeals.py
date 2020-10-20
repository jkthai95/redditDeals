import RedditParser
import Database
import Utils
import praw

class RedditDeals:
    def __init__(self, subreddits, limit=100, deal_threshold=50, upvote_threshold=70):
        # Maximum no. of submissions to parse for each subreddit
        self.limit = limit

        # Threshold used to filter out lower deals
        self.deal_threshold = deal_threshold    # (% off)

        # Threshold used to filter out less upvoted deals
        self.upvote_threshold = upvote_threshold  # (% ratio between upvotes and downvotes)

        # Ensure each subreddit is unique
        self.subreddits = self.acquire_unique_subreddits(subreddits)

        # Acquire login information from text file.
        login_info = Utils.get_login_info()

        # Acquire submissions from subreddit
        self.reddit = praw.Reddit(client_id=login_info['client_id'],
                             client_secret=login_info['client_secret'],
                             user_agent=login_info['user_agent'],
                             redirect_uri="http://localhost:8080",
                             username=login_info['username'],
                             password=login_info['password'])

        # Create parser for each subreddit
        self.reddit_parsers = []
        for subreddit in self.subreddits:
            self.reddit_parsers.append(RedditParser.RedditParser(subreddit,
                                                                 self.limit,
                                                                 self.deal_threshold,
                                                                 self.upvote_threshold,
                                                                 self.reddit))
        # Create mySQL database to hold data
        self.database = Database.Database()

    def acquire_unique_subreddits(self, subreddits):
        """
        Converts a list of subreddits to a list of unique subreddits.
        :param subreddits: List of subreddits (list of strings)
        :return: List of unique subreddits (list of strings)
        """
        # Keeps track of unique subreddits
        subreddits_seen = set()

        # Add subreddits to set
        for subreddit in subreddits:
            # Convert to lowercase
            subreddit = subreddit.lower()

            # Add to set
            subreddits_seen.add(subreddit)

        # Return list of unique subreddits
        return list(subreddits_seen)


    def acquire_deals(self):
        """
        Acquires all filtered deals from each subreddit.
        """
        for reddit_parser in self.reddit_parsers:
            print("Acquiring deals from %s." % reddit_parser.subreddit)

            # Acquire filtered deals
            submission_deals = reddit_parser.acquire_submission_deals()

            # Insert deals into table
            for submission_id in submission_deals:
                reddit_deal = Database.RedditDealStruct('"%s"' % submission_id)     # Encapsulate with " for mySQL commands
                self.database.insert_deal(reddit_deal)
                # print("{} ({})".format(title, url))

    def print_deals(self):
        """
        Prints table of reddit deals.
        """
        results = self.database.get_table()
        for row in results:
            reddit_submission = self.reddit.submission(id=row[0])
            title = reddit_submission.title
            permalink = reddit_submission.permalink
            print("{} ({}) ".format(title, permalink))


