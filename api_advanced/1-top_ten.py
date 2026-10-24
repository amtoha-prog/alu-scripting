#!/usr/bin/python3
"""Prints the titles of the first 10 hot posts of a subreddit."""
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


def top_ten(subreddit):
    """Print 10 hot post titles, or None if the subreddit is invalid."""
    r = get_page(subreddit, "hot", {"limit": 10})
    if r.status_code != 200:
        print(None)
        return
    for post in r.json().get("data", {}).get("children", []):
        print(post.get("data", {}).get("title"))
