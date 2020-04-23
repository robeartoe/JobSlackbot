module Users/Robert/Go/src/github.com/robeartoe/JobSlackbot

go 1.13

require github.com/gin-gonic/gin v1.6.2

require (
	github.com/gofiber/fiber v1.8.431
	github.com/golang/protobuf v1.3.5 // indirect
	github.com/gorilla/websocket v1.4.2 // indirect
	github.com/klauspost/compress v1.10.3 // indirect
	github.com/kr/pretty v0.1.0 // indirect
	github.com/modern-go/concurrent v0.0.0-20180306012644-bacd9c7ef1dd // indirect
	github.com/modern-go/reflect2 v1.0.1 // indirect
	github.com/pkg/errors v0.9.1 // indirect
	github.com/robeartoe/JobSlackbot/slackpost v0.1.0
	golang.org/x/sys v0.0.0-20200331124033-c3d80250170d // indirect
	gopkg.in/check.v1 v1.0.0-20180628173108-788fd7840127 // indirect
)

replace github.com/robeartoe/JobSlackbot/slackpost v0.1.0 => ./slackpost

replace github.com/robeartoe/JobSlackbot/bigquery v0.1.0 => ./bigquery
