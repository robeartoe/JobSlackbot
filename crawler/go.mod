module github.com/robeartoe/JobSlackbot/crawler

go 1.13

require (
	github.com/golang/protobuf v1.3.5 // indirect
	github.com/robeartoe/JobSlackbot/crawler/shared/github v0.1.0
	github.com/robeartoe/JobSlackbot/crawler/shared/indeed v0.1.0
	github.com/robeartoe/JobSlackbot/crawler/shared/interfaces v0.1.0
	golang.org/x/tools v0.0.0-20200313205530-4303120df7d8 // indirect
	google.golang.org/genproto v0.0.0-20200313141609-30c55424f95d // indirect

)

replace github.com/robeartoe/JobSlackbot/crawler/shared/github v0.1.0 => ./shared/github

replace github.com/robeartoe/JobSlackbot/crawler/shared/indeed v0.1.0 => ./shared/indeed

replace github.com/robeartoe/JobSlackbot/crawler/shared/pubsub v0.1.0 => ./shared/pubsub

replace github.com/robeartoe/JobSlackbot/crawler/shared/interfaces v0.1.0 => ./shared/interfaces
