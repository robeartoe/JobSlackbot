package main

import (
	"context"
	"log"
	"time"

	"cloud.google.com/go/bigquery"
	"github.com/gofiber/fiber"
	"github.com/robeartoe/JobSlackbot/schedulers/slackposts/util"
)

func main() {
	app := fiber.New()

	app.Get("/", func(c *fiber.Ctx) {
		today := time.Now()
		ctx := context.Background()
		// Get Client:
		client, err := bigquery.NewClient(ctx, "slackbot-260723")
		if err != nil {
			log.Fatalf("bigquery.NewClient: %v", err)
			panic(err)
		}

		// Get Query:
		rows, err := util.Query(ctx, client, today)
		if err != nil {
			log.Fatalf("Query Function: %v", err)
			panic(err)
		}

		// Format/Aggregate Query:
		post, err := util.BuildMessage(rows)
		if err != nil {
			log.Fatalf("Build Message: %v", err)
			panic(err)
		}

		// Send Post:
		err = util.PostToSlack(post)
		if err != nil {
			log.Fatalf("Post Message: %v", err)
			panic(err)
		}

		c.Send("Sent Messages!")
		defer client.Close()
	})

	app.Listen(8080)
}
