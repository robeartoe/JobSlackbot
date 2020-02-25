package main

import (
	"fmt"
	slackpost "github.com/robeartoe/JobSlackbot/functions/slackpost"
	"log"
	"net/http"
)

// /Users/Robert/Go/src/github.com/robeartoe/JobSlackbot/functions/slackpost/function.go

func main() {
	slackpost.PostMessage()
}
// func main() {
// 	http.HandleFunc("/", slackpost.HTTPServer)
// 	fmt.Println("Listening on localhost:8080")
// 	log.Fatal(http.ListenAndServe(":8080", nil))
// }

