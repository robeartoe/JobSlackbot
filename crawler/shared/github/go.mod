module github.com/robeartoe/JobSlackbot/crawler/github

go 1.14

require (
	github.com/robeartoe/JobSlackbot/crawler/shared/interfaces v0.1.0
	github.com/robeartoe/JobSlackbot/crawler/shared/pubsub v0.1.0

)

replace github.com/robeartoe/JobSlackbot/crawler/shared/interfaces v0.1.0 => ../interfaces

replace github.com/robeartoe/JobSlackbot/crawler/shared/pubsub v0.1.0 => ../pubsub
