import RedditDeals


subreddits = ["buildapcsales", "GameDeals", "gamedeals"]

def main():
    reddit_deals = RedditDeals.RedditDeals(subreddits)
    print(" ")

    reddit_deals.acquire_deals()


if __name__ == '__main__':
    main()

