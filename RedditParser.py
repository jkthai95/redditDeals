import praw
from parse import parse
import numpy as np


class RedditParser:
    def __init__(self, subreddit, limit, deal_threshold):
        # Title of subreddit
        self.subreddit = subreddit

        # Maximum no. of submissions to parse
        self.limit = limit

        # Threshold used to filter out lower deals
        self.deal_threshold = deal_threshold  # (% off)

        print("(RedditParser) Initialized for %s." % subreddit)

    def acquire_submission_deals(self):
        """
        Acquires all deals better than deal threshold.
        :return: Dictionary of submissions (title, url)
        """
        # Holds results
        submission_deals = dict()  # (title, url)

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

        subreddit = reddit.subreddit(self.subreddit)
        submissions = subreddit.new(limit=self.limit)

        # Parse each submission for deals
        for submission in submissions:
            # acquire deals
            deals = []
            self.acquire_deal(submission.title, deals)
            deals = np.array(deals)

            # Deal is better than specified threshold
            if any(deals > self.deal_threshold):
                submission_deals[submission.title] = submission.url

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
