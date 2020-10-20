import praw
from parse import parse
import numpy as np
import Utils

class RedditParser:
    def __init__(self, subreddit, limit, deal_threshold, upvote_threshold, reddit=None):
        """

        :param subreddit: Title of subreddit
        :param limit: Maximum no. of submissions to parse.
        :param deal_threshold: Threshold for percent off.
        :param upvote_threshold: Threshold for upvote to downvote ratio.
        :param reddit: Python Reddit API wrapper object.
        """
        if reddit:
            # Link reddit instance
            self.reddit = reddit
        else:
            # Acquire login information from text file.
            login_info = Utils.get_login_info()

            # Create reddit instance
            self.reddit = praw.Reddit(client_id=login_info['client_id'],
                                      client_secret=login_info['client_secret'],
                                      user_agent=login_info['user_agent'],
                                      redirect_uri="http://localhost:8080",
                                      username=login_info['username'],
                                      password=login_info['password'])

        # Title of subreddit
        self.subreddit = subreddit

        # Maximum no. of submissions to parse
        self.limit = limit

        # Threshold used to filter out lower deals
        self.deal_threshold = deal_threshold  # (% off)

        # Threshold used to filter out less upvoted deals
        self.upvote_threshold = float(upvote_threshold)/100  # (ratio between upvotes and downvotes)

    def acquire_submission_deals(self):
        """
        Acquires all deals better than deal threshold.
        :return: List of reddit submission IDs
        """
        # Holds results
        submission_deals = []

        subreddit = self.reddit.subreddit(self.subreddit)
        submissions = subreddit.new(limit=self.limit)

        # Parse each submission for deals
        for submission in submissions:
            # Check if submission passes upvote threshold.
            if submission.upvote_ratio < self.upvote_threshold:
                # Upvote threshold not passed.
                continue

            # Acquire deals
            deals = []
            self.acquire_deal(submission.title, deals)
            deals = np.array(deals)

            # Check if deal is better than deal threshold.
            if any(deals > self.deal_threshold):
                # Deal threshold not passed.
                continue

            # Deal passed all thresholds, save deal to list
            # submission_deals.append(submission.permalink)
            submission_deals.append(submission.id)

        return submission_deals

    def acquire_deal(self, title, deals):
        """
        Modifies "deals" to contain all deals (percentages).
        :param title: String to parse for deals.
        :param deals: List of percentages.
        :return:
        """
        # Note: currently, assumes specific format. "<ITEM> (<DEAL>%)"
        # TODO: Add ability to parse title without % off. Ex: (10.00 - 5.00), ($10.00 - $5.00)
        parsed_title = title.split("(")
        for element in parsed_title:
            element = element.split(")")
            if len(element) > 1:
                # "element" contains <DEAL>
                # pad with random character to work with parse format
                element = "(" + element[0] + ")"

                # Acquire deal percentage
                # - Decimal value.
                parsed_element = parse("{}{:d}%{}", element)
                deal = None
                if parsed_element:
                    deal = float(abs(parsed_element[1]))

                # - Float value.
                parsed_element = parse("{}{:d}%{}", element)
                if parsed_element:
                    deal = abs(parsed_element[1])

                # Add deal to list if found.
                if deal:
                    deals.append(abs(deal))
