package library

import (
	"net/http"
	"time"
)

// SearchData is the initial data sent into be crawled. Given a source and description/location query arrays.
type SearchData struct {
	Source        string   `json:"source,omitempty"`
	JobQuery      []string `json:"job_query"`
	LocationQuery []string `json:"location_query"`
}

// ReponseData fetches URL, either returns Response data or Error data with Job & Location Queries.
type ReponseData struct {
	Response *http.Response
	Error    error
	Search   string
	Location string
}

// PubSubData returns response or error.
type PubSubData struct {
	Id    string
	Error error
}

// JobPostingData is the standardized data that is sent to pub/sub for processing (BQ, and Slack)
type JobPostingData struct {
	Company    string
	CompanyURL string
	Location   string
	Title      string
	HowToApply string
	URL        string
	JobType    string
	Created    time.Time
	Error      error
	Data       interface{}
}
