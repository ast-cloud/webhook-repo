# webhook-repo
Flask web app to receive github webhook post requests for pull_request and push events from a repository ast-cloud/action-repo, and save details to a remote mongodb database.
UI pulls details from database every 15 seconds and displays it.
Deployed at - https://githubactions248.herokuapp.com/
