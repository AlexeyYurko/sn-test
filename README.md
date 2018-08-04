# DONE

 - basic models
 - basic features (user signup/login, post creation)
 - REST API

# TODO

## Requirement

 - post like
 - post unlike
 - token authentication (JWT is prefered)

## Optional

### get additional data and email check

 - use clearbit.com/enrichment for getting additional data for the user
   on signup
 - use emailhunter.co for verifying email existence on signup

### create automated bot

Object of this bot demonstrate functionalities of the system according to defined rules. This bot should read rules from a config file (in any format chosen by the candidate), but should have following fields (all integers, candidate can rename as they see fit):

 - number_of_user
 - max_posts_per_user
 - max_likes_per_user

Bot should read the configuration and create this activity:

 - signup users (number provided in config)
 - each user creates random number of posts with any content (up to max_posts_per_user)
 - after creating the signup and posting activity, posts should be liked randomly, posts can be liked multiple times
