package util

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

func buildBody() {

}

// BuildMessage will build the entire message
func BuildMessage(rows []JobPostingData) (Post, error) {
	var p Post
	return p, nil
}

// PostToSlack will post this message to the pub/sub to be sent to slack!
func PostToSlack(post Post) error {
	return nil
}
