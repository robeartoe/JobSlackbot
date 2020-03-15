package main

import (
	"fmt"
	"log"
	"net/http"

	"github.com/robeartoe/JobSlackbot/bigquery"
)

func main() {
	http.HandleFunc("/", bigquery.HTTPServer)
	fmt.Println("Listening on localhost:8080")
	log.Fatal(http.ListenAndServe("localhost:8080", nil))
}
