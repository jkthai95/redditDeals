import RedditDeals


subreddits = ["buildapcsales", "GameDeals", "gamedeals"]

def main():
    reddit_deals = RedditDeals.RedditDeals(subreddits, limit=300, deal_threshold=50)
    print(" ")

    reddit_deals.acquire_deals()


if __name__ == '__main__':
    main()

