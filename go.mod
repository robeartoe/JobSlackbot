module Users/Robert/Go/src/github.com/robeartoe/JobSlackbot

go 1.13

require github.com/gin-gonic/gin v1.5.0

require (
	github.com/gofiber/fiber v1.8.31
	github.com/klauspost/compress v1.10.2 // indirect
	github.com/klauspost/cpuid v1.2.3 // indirect
	github.com/modern-go/concurrent v0.0.0-20180306012644-bacd9c7ef1dd // indirect
	github.com/modern-go/reflect2 v1.0.1 // indirect
	github.com/robeartoe/JobSlackbot/bigquery v0.1.0
	github.com/robeartoe/JobSlackbot/crawler v0.1.0
	github.com/robeartoe/JobSlackbot/slackpost v0.1.0
)

replace github.com/robeartoe/JobSlackbot/slackpost v0.1.0 => ./slackpost

replace github.com/robeartoe/JobSlackbot/crawler v0.1.0 => ./crawler

replace github.com/robeartoe/JobSlackbot/bigquery v0.1.0 => ./bigquery
