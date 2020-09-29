import RedditParser

subreddits = ["buildapcsales", "GameDeals"]
reddit_parsers = []


def main():
    for subreddit in subreddits:
        reddit_parsers.append(RedditParser.RedditParser(subreddit))




if __name__ == '__main__':
    main()

