package pubsub

import (
	"context"
	"encoding/json"
	"io"

	pubsub "cloud.google.com/go/pubsub"
	library "github.com/robeartoe/JobSlackbot/crawler/internal/interfaces"
)

// Publish results from various APIs to Google's Pub/Sub listing job queue.
func Publish(w io.Writer, msg library.JobPostingData, c chan library.PubSubData) {
	defer close(c)
	var err error
	ctx := context.Background()

	client, err := pubsub.NewClient(ctx, "slackbot-260723")
	if err != nil {
		c <- library.PubSubData{Error: err}
	}

	t := client.Topic("listing")
	// defer t.Stop()

	data, err := json.Marshal(msg)
	if err != nil {
		c <- library.PubSubData{Error: err}
	}

	// var results []*pubsub.PublishResult
	if id, err := t.Publish(ctx, &pubsub.Message{
		Data: data,
	}).Get(ctx); err != nil {
		c <- library.PubSubData{Error: err}
	} else {
		c <- library.PubSubData{Id: id}
	}

	// results = append(results, r)
	// for _, r := range results {
	// 	id, err := r.Get(ctx)
	// 	if err != nil {
	// 		c <- library.PubSubData{Error: err}
	// 	}
	// 	c <- library.PubSubData{Id: id}
	// }

}
