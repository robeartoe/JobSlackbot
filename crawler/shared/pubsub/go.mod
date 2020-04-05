module github.com/robeartoe/JobSlackbot/crawler/pubsub

go 1.14

require (
	cloud.google.com/go/pubsub v1.3.1
	github.com/robeartoe/JobSlackbot/crawler/shared/interfaces v0.1.0
)

replace github.com/robeartoe/JobSlackbot/crawler/shared/interfaces v0.1.0 => ../interfaces
