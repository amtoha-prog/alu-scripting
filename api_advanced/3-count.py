#!/usr/bin/python3
"""Recursively counts keywords in the hot post titles of a subreddit."""
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


def count_words(subreddit, word_list, after=None, counts=None):
    """Print sorted keyword counts found in hot titles."""
    if counts is None:
        counts = {}
    r = get_page(subreddit, "hot", {"limit": 100, "after": after})
    if r.status_code != 200:
        return
    data = r.json().get("data", {})
    for child in data.get("children", []):
        title = child.get("data", {}).get("title", "")
        for word in title.lower().split():
            counts[word] = counts.get(word, 0) + 1
    after = data.get("after")
    if after:
        return count_words(subreddit, word_list, after, counts)

    totals = {}
    for w in word_list:
        w = w.lower()
        totals[w] = totals.get(w, 0) + counts.get(w, 0)
    for word, n in sorted(totals.items(), key=lambda x: (-x[1], x[0])):
        if n > 0:
            print("{}: {}".format(word, n))
