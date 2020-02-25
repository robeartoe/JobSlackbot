package main

import (
	"log"
	"net/http"

	"cloud.google.com/go/bigquery"
	"github.com/gin-gonic/gin"
	"golang.org/x/net/context"
)

func main() {
	// Initialize BigQuery:
	ctx := context.Background()
	client, err := bigquery.NewClient(ctx, "slackbot-260723")
	if err != nil {
		log.Fatal(err)
	}
	// Initialize Gin:
	r := gin.Default()
	r.GET("/", func(c *gin.Context) {
		c.JSON(200, gin.H{
			"message": "test",
		})
	})
	r.GET("/crawl", func(c *gin.Context) {

		c.JSON(200, gin.H{
			"message": "pong",
		})
	})
	http.Handle("/", r)
	r.Run() // listen and serve on 0.0.0.0:8080 (for windows "localhost:8080")
}
