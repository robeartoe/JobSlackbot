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

// SentPost response data to return after sending Slack post.
type SentPost struct {
	ChannelID string `json:"ChannelID"`
	Timestamp string `json:"timestamp"`
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

	msg, err := PostMessage(d)
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
	}
	w.WriteHeader(http.StatusOK)
	w.Header().Set("Content-Type", "application/json; charset=utf-8")
	json.NewEncoder(w).Encode(msg)
}

// PostMessage on Slack.
// Given a Message Object.
func PostMessage(post Post) (SentPost, error) {
	api := slack.New(os.Getenv("token"))

	emoji := post.Emoji
	if len(emoji) == 0 {
		emoji = ":incoming_envelope:"
	}

	attachment := slack.Attachment{
		Title:     post.Attachment.Title,
		TitleLink: post.Attachment.TitleLink,
		Pretext:   post.Attachment.Pretext,
		Text:      post.Attachment.Text,
	}

	channelID, timestamp, err := api.PostMessage("jobs", slack.MsgOptionText(post.Text, false), slack.MsgOptionUsername("Slackbot"), slack.MsgOptionIconEmoji(emoji), slack.MsgOptionAttachments(attachment))
	if err != nil {
		fmt.Printf("%s\n", err)
		return SentPost{}, err
	}

	returnValue := SentPost{
		ChannelID: channelID,
		Timestamp: timestamp,
	}
	fmt.Printf("Message successfully sent to channel %s at %s", channelID, timestamp)
	return returnValue, nil
}
