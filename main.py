import RedditDeals

subreddits = ["GameDeals", "buildapcsales"]

def main():
    reddit_deals = RedditDeals.RedditDeals(subreddits, limit=50, deal_threshold=50, upvote_threshold=70)
    reddit_deals.acquire_deals()
    reddit_deals.print_deals()


if __name__ == '__main__':
    main()

