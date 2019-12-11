package main

import (
	"golang.org/x/net/context"
	"net/http"
	"github.com/gin-gonic/gin"
	"cloud.google.com/go/bigquery"
)

func main() {
	ctx := context.Background()
	client, err := bigquery.NewClient(ctx, "slackbot-260723")
	if err != nil {
		// TODO: Handle error.
	}

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
