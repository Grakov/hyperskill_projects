from django.shortcuts import render
from django.views import View
from django.http import HttpResponse
from datetime import date, datetime, timedelta

import hypernews.settings as settings
import json


class PostView(View):
    def get(self, request, post_id=None, *args, **kwargs):
        with open(settings.NEWS_JSON_PATH) as f:
            posts = json.load(f)

        context = {
            "post": None,
            "page_title": "404 Not found"
        }

        for post in posts:
            if post.get("link", 0) == post_id:
                context = {
                    "post": post,
                    "page_title": post.title
                }
                break
        print(context)
        return render(request, "news/post.html", context=context)


class NewsView(View):
    def get(self, request, *args, **kwargs):
        print("all")
        with open(settings.NEWS_JSON_PATH) as f:
            posts = json.load(f)

        posts.sort(key=lambda item: item["created"], reverse=True)

        previous_date = None
        dates = []
        date_post_bundle = []
        for post in posts:
            post_date = datetime.strptime(post.created, settings.POST_DATETIME_FORMAT).date()
            if previous_date is None or previous_date == post_date:
                date_post_bundle.append(post)
            else:
                previous_date_string = previous_date.strftime(settings.POST_DATE_FORMAT)
                dates.append({
                    "day": previous_date_string,
                    "posts": date_post_bundle
                })
                date_post_bundle = list(post)
                previous_date = post_date

        context = {
            "dates": dates,
            "page_title": "All news"
        }

        return render(request, "news/index.html", context=context)


class IndexView(View):
    def get(self, request, *args, **kwargs):
        print("index")
        return HttpResponse(f"Coming soon")
