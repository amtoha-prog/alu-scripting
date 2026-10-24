#!/usr/bin/python3
"""Recursively returns the titles of all hot posts of a subreddit."""
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


def recurse(subreddit, hot_list=None, after=None):
    """Return a list of all hot titles, or None if invalid."""
    if hot_list is None:
        hot_list = []
    r = get_page(subreddit, "hot", {"limit": 100, "after": after})
    if r.status_code != 200:
        return None
    data = r.json().get("data", {})
    for child in data.get("children", []):
        hot_list.append(child.get("data", {}).get("title"))
    after = data.get("after")
    if after:
        return recurse(subreddit, hot_list, after)
    return hot_list
