package main

import (
	"fmt"
	"log"
	"net/http"

	"github.com/robeartoe/JobSlackbot/slackpost"
)

// /Users/Robert/Go/src/github.com/robeartoe/JobSlackbot/functions/slackpost/function.go

func main() {
	http.HandleFunc("/", slackpost.HTTPServer)
	fmt.Println("Listening on localhost:8080")
	log.Fatal(http.ListenAndServe("localhost:8080", nil))
}
