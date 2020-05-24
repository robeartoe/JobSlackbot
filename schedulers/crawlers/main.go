package main

import (
	"bytes"
	"encoding/json"
	"net/http"

	"github.com/gofiber/fiber"
)

type SearchData struct {
	Source        string   `json:"source,omitempty"`
	JobQuery      []string `json:"job_query"`
	LocationQuery []string `json:"location_query"`
}

func main() {
	app := fiber.New()

	app.Get("/", func(c *fiber.Ctx) {
		body := SearchData{
			Source:        "github",
			JobQuery:      []string{"software engineer"},
			LocationQuery: []string{"los angeles"},
		}
		requestBody, err := json.Marshal(body)
		if err != nil {
			panic(err)
		}
		req, err := http.NewRequest("POST", "https://us-central1-slackbot-260723.cloudfunctions.net/crawler", bytes.NewBuffer(requestBody))
		req.Header.Set("Content-Type", "application/json")
		client := &http.Client{}
		resp, err := client.Do(req)
		if err != nil {
			panic(err)
		}
		defer resp.Body.Close()
		if resp.StatusCode != 200 {
			panic(err)
		}
		c.Send("Started Crawlers!")
	})

	app.Listen(8080)
}
