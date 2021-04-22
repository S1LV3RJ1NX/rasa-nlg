# rasa-nlg

- Make sure you have set up git and github repo for the project and have heroku cli installed for your specific os
- Create google sheet api. Ref [Analytics Vidya](https://www.analyticsvidhya.com/blog/2020/07/read-and-update-google-spreadsheets-with-python/)
- Save the API json in your project folder and make sure to add it to **.gitignore**

**Steps:**
- `heroku login`
- `heroku create rasa-nlg`
- set env variable `GSHEET_KEY` in your heroku app and the value will be the entire dictionary presnt in your json file
- `git push heroku main`
- Check logs for build

**Automate deployment:**
- You can go to deploy tab in your heroku app on broweser
- Connect to github (Deployment Method)
- Serach for repo, corresponding branch and enable automatic deployment.
- So next time you push to repo app will be automatically deployed.

**Automatic Ping:**
- We all know heroku apps sleep after 30 min of inactivity hence we can ping it to prevent from sleeping
- Go to [https://kaffeine.herokuapp.com/](https://kaffeine.herokuapp.com/)
- Put name of your your app, and you are done!!
- e.g http://`rasa-nlg`.herokuapp.com


Finally you can put this as your endpoint in your rasa bot.
e.g:

`nlg:`

    url: https://rasa-nlg.herokuapp.com/nlg