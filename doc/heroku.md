# heroku hosting

A running instance of the bot is hosted on heroku. See:

https://devcenter.heroku.com/articles/git

for details of setting this up. One slight complication here is that in order to do this, we need the grammar to be under source code control so that it can be pushed to heroku. So there is a possibly synchronisation issue to be aware of.

Note also that api keys and tokens are needed to allow the bot to tweet. These are not stored in the repository, but are set as environment variables. This can be done locally or via the heroku config vars for the application. 

To push to heroku use

```
git push heroku master
```

This will push the code, prompting a redeployment of the app. It can then be run explicitly, e.g.

```
heroku run python python/tweetbot.py --config config.json
```

or as a scheduled job. 
