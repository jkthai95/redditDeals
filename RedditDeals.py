import RedditParser


class RedditDeals:
    def __init__(self, subreddits):
        # Ensure each subreddit is unique
        self.subreddits = self.acquire_unique_subreddits(subreddits)

        # Create parser for each subreddit
        self.reddit_parsers = []
        for subreddit in self.subreddits:
            self.reddit_parsers.append(RedditParser.RedditParser(subreddit))

        # Maximum number of pages to parse for each subreddit
        self.num_pages_parsed = 2

        # Threshold used to filter out lower deals
        self.deal_threshold = 30    # (% off)

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

            reddit_parser.acquire_titles()

            print(" ")
