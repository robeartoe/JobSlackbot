module github.com/robeartoe/JobSlackbot/schedulers/slackposts

go 1.14

replace github.com/robeartoe/JobSlackbot/schedulers/slackposts/util => ./util

require (
	cloud.google.com/go/bigquery v1.6.0
	github.com/gofiber/fiber v1.9.3
	github.com/robeartoe/JobSlackbot/schedulers/crawlers/util v0.0.0-20200506033054-8c1497353d6f
	github.com/robeartoe/JobSlackbot/schedulers/slackposts/util v0.0.0-00010101000000-000000000000

)
