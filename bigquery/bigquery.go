package bigquery

import (
	"bytes"
	"context"
	"encoding/base64"
	"encoding/gob"
	"fmt"
	"time"

	"cloud.google.com/go/bigquery"
)

// PubSubMessage is the payload of a Pub/Sub event.
type PubSubMessage struct {
	Data []byte `json:"data"`
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

// PubSubEntry consumes a Pub/Sub message.
func PubSubEntry(ctx context.Context, m PubSubMessage) error {
	// data := string(m.Data)
	decodedData, err := decodedData(string(m.Data))
	if err != nil {
		return err
	}

	fmt.Println(decodedData)
	if err := postToBigquery(decodedData); err != nil {
		return err
	}
	return nil
}

func decodedData(data string) (JobPostingData, error) {
	decodedData := JobPostingData{}
	by, err := base64.StdEncoding.DecodeString(data)
	if err != nil {
		fmt.Println(`failed base64 Decode`, err)
		return JobPostingData{}, err
	}
	b := bytes.Buffer{}
	b.Write(by)
	d := gob.NewDecoder(&b)
	// Convert the data to the Standardized Job Post Struct:
	err = d.Decode(&decodedData)
	if err != nil {
		fmt.Println(`failed gob Decode`, err)
		return JobPostingData{}, err
	}
	return JobPostingData{}, nil
}

func postToBigquery(job JobPostingData) error {
	// Create BigQuery Client:
	ctx := context.Background()
	client, err := bigquery.NewClient(ctx, "slackbot-260723")
	if err != nil {
		return err
	}

	// Given struct post data to BigQuery:
	defaultDataset := client.Dataset("jobs")
	listings := defaultDataset.Table("listings")
	u := listings.Uploader()
	if err := u.Put(ctx, job); err != nil {
		return err
	}

	println("Data Uploaded!")
	return nil

}
