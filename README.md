# PRE-hodl-bot
Designed to work with hourly cron for random-time daily purchases of a set amount for long-term dollar cost averaging.

## How to run it

You will need an account on the CoinEx exchange.

1. Clone the repo.
1. Copy env_copy to .env
1. fill out the values
2. assumes that you have Telegram setup for notifications 
3. make sure the BUY amount is correct - defaults to $5 (this will soon be part of .env)
1. Create a crontab schedule to run hourly that points to the script (`0 * * * * /[your-full-path-into-project-root]/scripts/run_randomly.sh`)

## How to Contribute

Submit a PR along with test coverage.

## Contributors and supporting organizations

[VaxCalc Labs](https://github.com/VaxCalc-Labs) - we create Informed Consent Technology to democratize vaccine-risk info
