module Users/Robert/Go/src/github.com/robeartoe/JobSlackbot

go 1.13

require github.com/gin-gonic/gin v1.6.2

require (
	cloud.google.com/go/bigquery v1.6.0
	github.com/gofiber/fiber v1.9.3
	github.com/golang/protobuf v1.4.1 // indirect
	github.com/gorilla/websocket v1.4.2 // indirect
	github.com/klauspost/compress v1.10.5 // indirect
	github.com/klauspost/cpuid v1.2.1 // indirect
	github.com/kr/pretty v0.1.0 // indirect
	github.com/modern-go/concurrent v0.0.0-20180306012644-bacd9c7ef1dd // indirect
	github.com/modern-go/reflect2 v1.0.1 // indirect
	github.com/pkg/errors v0.9.1 // indirect
	github.com/robeartoe/JobSlackbot/slackpost v0.1.0
	golang.org/x/net v0.0.0-20200505041828-1ed23360d12c // indirect
	golang.org/x/sys v0.0.0-20200501145240-bc7a7d42d5c3 // indirect
	golang.org/x/tools v0.0.0-20200505023115-26f46d2f7ef8 // indirect
	google.golang.org/api v0.23.0 // indirect
	google.golang.org/appengine v1.6.6 // indirect
	google.golang.org/genproto v0.0.0-20200430143042-b979b6f78d84 // indirect
	google.golang.org/grpc v1.29.1 // indirect
	gopkg.in/check.v1 v1.0.0-20180628173108-788fd7840127 // indirect
)

replace github.com/robeartoe/JobSlackbot/slackpost v0.1.0 => ./slackpost

replace github.com/robeartoe/JobSlackbot/bigquery v0.1.0 => ./bigquery
