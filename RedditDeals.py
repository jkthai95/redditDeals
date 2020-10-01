import RedditParser


class RedditDeals:
    def __init__(self, subreddits, limit=3, deal_threshold=30):
        # Maximum no. of submissions to parse for each subreddit
        self.limit = limit

        # Threshold used to filter out lower deals
        self.deal_threshold = deal_threshold    # (% off)

        # Ensure each subreddit is unique
        self.subreddits = self.acquire_unique_subreddits(subreddits)

        # Create parser for each subreddit
        self.reddit_parsers = []
        for subreddit in self.subreddits:
            self.reddit_parsers.append(RedditParser.RedditParser(subreddit, self.limit, self.deal_threshold))

        print("(RedditDeals) Initialized.")


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

            # Display deals
            for title, url in submission_deals.items():
                print("{} ({})".format(title, url))

            print(" ")
