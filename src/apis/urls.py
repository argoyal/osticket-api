from apis import views
import os


app_name = os.environ.get("APPLICATION_NAME")


api_urls = [
    ("/", views.index, ["GET"], "{} index url".format(app_name))
]

org_urls = [
    ("/organization", views.organization_list, ["GET", "POST"],
     "get an organization and add an organization")
]

user_urls = [
    ("/user", views.user_list, ["GET", "POST"],
     "get an user and add an user")
]

all_urls = api_urls + org_urls + user_urls
