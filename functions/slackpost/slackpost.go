package slackpost

import (
	"encoding/json"
	"fmt"
	"github.com/nlopes/slack"
	"html"
	"net/http"
)

// interface 

// HTTPServer is an HTTP Cloud Function with a request parameter.
func HTTPServer(w http.ResponseWriter, r *http.Request) {
	PostMessage()
	var d struct {
		Name string `json:"name"`
	}
	if err := json.NewDecoder(r.Body).Decode(&d); err != nil {
		fmt.Fprint(w, "Hello, World!")
		return
	}
	if d.Name == "" {
		fmt.Fprint(w, "Hello, World!")
		return
	}
	fmt.Fprintf(w, "Hello, %s!", html.EscapeString(d.Name))
}

// PostMessage on Slack.
// Given a Message Object.
// func PostMessage(message map[string]string) {
func PostMessage() {
	fmt.Println("testing!")
	// fmt.Println(message)
	api := slack.New("xoxp-77390523108-77402999255-875064760306-4838d42a4a15700673df8352d57de4e1")
	// You can view the Attachment 
	// attachment := slack.Attachment{
	// 	Pretext: "some pretext",
	// 	Text:    "some text",
	// 	// Uncomment the following part to send a field too
	// 	/*
	// 		Fields: []slack.AttachmentField{
	// 			slack.AttachmentField{
	// 				Title: "a",
	// 				Value: "no",
	// 			},
	// 		},
	// 	*/
	// }

	channelID, timestamp, err := api.PostMessage("jobs", slack.MsgOptionText("Some text", false), slack.MsgOptionIconEmoji("+1F602"))
	if err != nil {
		fmt.Printf("%s\n", err)
		return
	}
	fmt.Printf("Message successfully sent to channel %s at %s", channelID, timestamp)
}
