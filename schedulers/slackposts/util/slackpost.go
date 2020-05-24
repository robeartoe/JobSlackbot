package util

import (
	"bytes"
	"encoding/json"
	"errors"
	"fmt"
	"net/http"
)

// Post defines slack Message JSON data to be passed into PostMessage
type Post struct {
	Text       string `json:"text"`
	Emoji      string `json:"emoji"`
	Attachment []Attachment
}

// Attachment defines Slack Attachment detailing info about Job Post
type Attachment struct {
	Title     string `json:"title,omitempty"`
	TitleLink string `json:"TitleLink,omitempty"`
	Pretext   string `json:"pretext,omitempty"`
	Text      string `json:"text,omitempty"`
}

func buildAttachments(rows []JobPostingData) []Attachment {
	var attachments []Attachment
	for i := 0; i < len(rows); i++ {
		data := Attachment{
			Title:     fmt.Sprintf("%s - %s - %s", rows[i].Title, rows[i].Location, rows[i].JobType),
			TitleLink: rows[i].URL,
			Text:      rows[i].HowToApply,
		}
		attachments = append(attachments, data)
	}
	return attachments
}

// BuildMessage will build the entire message
func BuildMessage(rows []JobPostingData) (Post, error) {
	p := Post{
		Text:       fmt.Sprintf("%d New Job Listings!", len(rows)),
		Attachment: buildAttachments(rows),
	}
	return p, nil
}

// PostToSlack will post this message to the pub/sub to be sent to slack!
func PostToSlack(post Post) error {
	requestBody, err := json.Marshal(post)
	if err != nil {
		return err
	}
	req, err := http.NewRequest("POST", "https://us-central1-slackbot-260723.cloudfunctions.net/slackpost", bytes.NewBuffer(requestBody))
	req.Header.Set("Content-Type", "application/json")
	client := &http.Client{}
	resp, err := client.Do(req)
	if err != nil {
		return err
	}
	defer resp.Body.Close()
	if resp.StatusCode != 200 {
		return errors.New("Post to Slack failed")
	}
	return nil
}
