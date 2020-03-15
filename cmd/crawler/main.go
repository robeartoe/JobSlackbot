package main

import (
	"fmt"
	"log"
	"net/http"

	"github.com/robeartoe/JobSlackbot/crawler"
)

func main() {
	http.HandleFunc("/", crawler.HTTPServer)
	fmt.Println("Listening on localhost:8080")
	log.Fatal(http.ListenAndServe("localhost:8080", nil))
}
