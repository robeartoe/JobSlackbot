package main

import (
	"context"
	"fmt"
	"log"
	"time"

	"cloud.google.com/go/bigquery"
	"github.com/gofiber/fiber"
	"github.com/robeartoe/JobSlackbot/schedulers/crawlers/util"
)

func main() {
	app := fiber.New()

	app.Get("/", func(c *fiber.Ctx) {
		today := time.Now()
		ctx := context.Background()

		client, err := bigquery.NewClient(ctx, "slackbot-260723")
		if err != nil {
			log.Fatalf("bigquery.NewClient: %v", err)
			panic(err)
		}

		query, err := util.Query(ctx, client, today)
		if err != nil {
			log.Fatalf("Query Function: %v", err)
			panic(err)
		}
		fmt.Println(query)
		defer client.Close()

		c.Send("Hello World!")
	})

	app.Listen(3000)
}
