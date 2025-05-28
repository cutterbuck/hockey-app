Hockey Demo App

The initial purpose of this project is to experiment with deploying a DASH application to DigitalOcean's App Platform. The app, in its current form, updates team standings by querying the NHLClient API every night. The longer-term goal is to delve deeper into NHL analytics in attempt to understand the game at a higher level.

The next steps are to add players to each team's roster and track their statistics with a nightly batch update. The statistics included should be wide-ranging. For instance, basics like Goals, Assists, Points, and Time on Ice will be tracked as well as more "advanced" metrics like xGoals and NHL Edge physical data like skater top speed and 20mph+ burst frequency.

This data will be used to ponder larger questions like:
  - What team stats are the most predictable when it comes to team success (winning)?
  - What player stats are the most predictable when it comes to team success?
  - How persistent are the resulting stats from year-to-year? If variance is high, are they actually useful?
  - By determining which analytics actually matter, is there a repeatable way to find undervalued players?
  - Do overlooked stats exist that are predictive of winning?
  - Keeping in mind Einstein's observation that "not everything that counts can be counted, and not everything that can be counted counts", do the results of this statistical analysis make sense from a qualitative basis?
  - If every team did this kind of analysis, would there be no sustainable competitive advantage?

And also used to answer specific questions like:
  - How much does faceoff win percentage correlate with team success in aggregate?
  - How much does strong special teams play (powerplay, shorthanded, 6v5, and 5v6) drive team success?
  - Qualitatively, it seems like faceoff wins are very important during special teams situations. Does faceoff win percentage actually help drive special teams success?

Created by Jake MacNaughton (2025)
