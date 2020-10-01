import RedditDeals


subreddits = ["buildapcsales", "GameDeals", "gamedeals"]

def main():
    reddit_deals = RedditDeals.RedditDeals(subreddits, limit=100, deal_threshold=50, upvote_threshold=70)
    print(" ")

    reddit_deals.acquire_deals()


if __name__ == '__main__':
    main()

