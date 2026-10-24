#!/usr/bin/python3
"""Returns the number of subscribers of a subreddit."""
import os
import requests

UA = {"User-Agent": "linux:alu-scripting:v1.0 (by /u/alu_student)"}


def get_page(subreddit, page, params=None):
    """Query a subreddit endpoint, using OAuth if credentials are set."""
    headers = dict(UA)
    host, ext = "https://www.reddit.com", ".json"
    cid = os.getenv("REDDIT_ID")
    secret = os.getenv("REDDIT_SECRET")
    if cid and secret:
        auth = requests.auth.HTTPBasicAuth(cid, secret)
        tok = requests.post("https://www.reddit.com/api/v1/access_token",
                            auth=auth,
                            data={"grant_type": "client_credentials"},
                            headers=UA)
        headers["Authorization"] = "bearer {}".format(
            tok.json().get("access_token"))
        host, ext = "https://oauth.reddit.com", ""
    url = "{}/r/{}/{}{}".format(host, subreddit, page, ext)
    return requests.get(url, headers=headers, params=params,
                        allow_redirects=False)


def number_of_subscribers(subreddit):
    """Return total subscribers, or 0 if the subreddit is invalid."""
    r = get_page(subreddit, "about")
    if r.status_code != 200:
        return 0
    return r.json().get("data", {}).get("subscribers", 0)
