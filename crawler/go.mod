module github.com/robeartoe/JobSlackbot/crawler

go 1.14

require (
	cloud.google.com/go/pubsub v1.3.1 // indirect
	github.com/robeartoe/JobSlackbot/crawler/shared/github v0.1.0
	github.com/robeartoe/JobSlackbot/crawler/shared/indeed v0.1.0
	github.com/robeartoe/JobSlackbot/crawler/shared/interfaces v0.1.0
	github.com/robeartoe/JobSlackbot/crawler/shared/pubsub v0.1.0 // indirect

)

replace github.com/robeartoe/JobSlackbot/crawler/shared/github v0.1.0 => ./shared/github

replace github.com/robeartoe/JobSlackbot/crawler/shared/indeed v0.1.0 => ./shared/indeed

replace github.com/robeartoe/JobSlackbot/crawler/shared/interfaces v0.1.0 => ./shared/interfaces

replace github.com/robeartoe/JobSlackbot/crawler/shared/pubsub v0.1.0 => ./shared/pubsub
