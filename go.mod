module Users/Robert/Go/src/github.com/robeartoe/JobSlackbot

go 1.13

require github.com/gin-gonic/gin v1.6.2

require (
	cloud.google.com/go v0.56.0 // indirect
	github.com/fasthttp/websocket v1.4.2 // indirect
	github.com/gofiber/fiber v1.8.431
	github.com/gofiber/template v1.1.0 // indirect
	github.com/google/uuid v1.1.1 // indirect
	github.com/gorilla/websocket v1.4.2 // indirect
	github.com/klauspost/compress v1.10.3 // indirect
	github.com/klauspost/cpuid v1.2.3 // indirect
	github.com/modern-go/concurrent v0.0.0-20180306012644-bacd9c7ef1dd // indirect
	github.com/modern-go/reflect2 v1.0.1 // indirect
	github.com/pkg/errors v0.9.1 // indirect
	github.com/robeartoe/JobSlackbot/bigquery v0.1.0
	github.com/robeartoe/JobSlackbot/crawler v0.1.0
	github.com/robeartoe/JobSlackbot/slackpost v0.1.0
	github.com/savsgio/gotils v0.0.0-20200319105752-a9cc718f6a3f // indirect
	github.com/valyala/fasttemplate v1.1.0 // indirect
	golang.org/x/tools v0.0.0-20200331202046-9d5940d49312 // indirect
	gopkg.in/go-playground/assert.v1 v1.2.1 // indirect
	gopkg.in/go-playground/validator.v9 v9.31.0 // indirect
)

replace github.com/robeartoe/JobSlackbot/slackpost v0.1.0 => ./slackpost

replace github.com/robeartoe/JobSlackbot/crawler v0.1.0 => ./crawler

replace github.com/robeartoe/JobSlackbot/bigquery v0.1.0 => ./bigquery
