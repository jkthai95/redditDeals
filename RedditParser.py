import praw
from parse import parse
import numpy as np


class RedditParser:
    def __init__(self, subreddit, limit, deal_threshold, upvote_threshold):
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
        :return: Dictionary of submissions (title, url)
        """
        # Holds results
        submission_deals = dict()  # (title, url)

        # TODO: Acquire data from GUI
        # For now, we acquire necessary data from a file.
        with open('./redditLogin', 'r') as fp:
            client_id = fp.readline().strip()
            client_secret = fp.readline().strip()
            user_agent = fp.readline().strip()
            username = fp.readline().strip()
            password = fp.readline().strip()

        # Acquire submissions from subreddit
        reddit = praw.Reddit(client_id=client_id,
                             client_secret=client_secret,
                             user_agent=user_agent,
                             redirect_uri="http://localhost:8080",
                             username=username,
                             password=password)

        subreddit = reddit.subreddit(self.subreddit)
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
                # Found deal better than threshold
                # submission_deals[submission.title] = submission.url       # links to deal
                submission_deals[submission.title] = \
                    "https://www.reddit.com" + submission.permalink   # links to reddit submission

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
