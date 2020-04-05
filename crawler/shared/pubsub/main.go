package pubsub

import (
	"context"
	"encoding/json"

	pubsub "cloud.google.com/go/pubsub"
	library "github.com/robeartoe/JobSlackbot/crawler/shared/interfaces"
)

// Publish results from various APIs to Google's Pub/Sub listing job queue.
func Publish(data []library.JobPostingData, c chan []library.PubSubData) {
	var err error
	var pubSubs []library.PubSubData

	ctx := context.Background()
	client, err := pubsub.NewClient(ctx, "slackbot-260723")
	if err != nil {
		pubSubs = append(pubSubs, library.PubSubData{Error: err})
		c <- pubSubs
	}
	t := client.Topic("listing")

	for _, msg := range data {
		data, err := json.Marshal(msg)
		if err != nil {
			pubSubs = append(pubSubs, library.PubSubData{Error: err})
			continue
		}

		id, err := t.Publish(ctx, &pubsub.Message{
			Data: data,
		}).Get(ctx)
		if err != nil {
			pubSubs = append(pubSubs, library.PubSubData{Error: err})
			continue
		}
		pubSubs = append(pubSubs, library.PubSubData{Id: id})
	}

	c <- pubSubs
	defer t.Stop()
	defer close(c)
}
