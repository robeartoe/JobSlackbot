package slackpost

import (
	"encoding/json"
	"fmt"
	"net/http"
	"os"

	"github.com/nlopes/slack"
)

// Post defines slack Message JSON data to be passed into PostMessage
type Post struct {
	Text       string `json:"text"`
	Emoji      string `json:"emoji"`
	Attachment Attachment
}

// Attachment defines Slack Attachment detailing info about Job Post
type Attachment struct {
	Title     string `json:"title,omitempty"`
	TitleLink string `json:"TitleLink,omitempty"`
	Pretext   string `json:"pretext,omitempty"`
	Text      string `json:"text,omitempty"`
}

// HTTPServer is an HTTP Cloud Function with a request parameter.
func HTTPServer(w http.ResponseWriter, r *http.Request) {
	var d Post

	err := json.NewDecoder(r.Body).Decode(&d)
	if err != nil {
		w.WriteHeader(http.StatusBadRequest)
		w.Write([]byte("400 - Invalid Parameters!"))
		return
	}

	// if d.Text == "" {
	// 	fmt.Fprintf(w, "NO TEXT, %+v!", d)
	// 	log.Println(d, r.Body)
	// 	return
	// }
	// log.Println(d, r.Body)

	PostMessage(d)
}

// PostMessage on Slack.
// Given a Message Object.
func PostMessage(post Post) {
	api := slack.New(os.Getenv("token"))

	fmt.Printf("%+v\n", post)

	emoji := post.Emoji
	if len(emoji) == 0 {
		emoji = ":incoming_envelope:"
	}

	// You can view the Attachment
	attachment := slack.Attachment{
		Title:     post.Attachment.Title,
		TitleLink: post.Attachment.TitleLink,
		Pretext:   post.Attachment.Pretext,
		Text:      post.Attachment.Text,
		// 	// Uncomment the following part to send a field too
		// 	/*
		// 		Fields: []slack.AttachmentField{
		// 			slack.AttachmentField{
		// 				Title: "a",
		// 				Value: "no",
		// 			},
		// 		},
		// 	*/
	}

	channelID, timestamp, err := api.PostMessage("jobs", slack.MsgOptionText(post.Text, false), slack.MsgOptionUsername("Slackbot"), slack.MsgOptionIconEmoji(emoji), slack.MsgOptionAttachments(attachment))
	if err != nil {
		fmt.Printf("%s\n", err)
		return
	}
	fmt.Printf("Message successfully sent to channel %s at %s", channelID, timestamp)
}
