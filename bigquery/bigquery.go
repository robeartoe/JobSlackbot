package bigquery

import (
	"context"
	"encoding/json"
	"log"
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
	Source     string
	Created    time.Time
	Error      error
	Data       interface{}
}

// UploadData returns back everything, and stringifies the Data
type UploadData struct {
	Company    string
	CompanyURL string
	Location   string
	Title      string
	HowToApply string
	URL        string
	JobType    string
	Source     string
	Created    time.Time
	InsertDate time.Time
	Data       string
}

// PubSubEntry consumes a Pub/Sub message.
func PubSubEntry(ctx context.Context, m PubSubMessage) error {
	var jobPost JobPostingData
	if err := json.Unmarshal(m.Data, &jobPost); err != nil {
		panic(err)
	}

	formattedData := transform(jobPost)

	if err := postToBigquery(formattedData); err != nil {
		panic(err)
	}
	return nil
}

func transform(data JobPostingData) UploadData {
	return UploadData{
		Company:    data.Company,
		CompanyURL: data.CompanyURL,
		Location:   data.Location,
		Title:      data.Title,
		HowToApply: data.HowToApply,
		URL:        data.URL,
		JobType:    data.JobType,
		Source:     data.Source,
		Created:    data.Created,
		InsertDate: time.Now(),
		Data:       stringify(data.Data),
	}
}

func stringify(data interface{}) string {
	var jsonData []byte
	jsonData, err := json.Marshal(data)
	if err != nil {
		log.Println(err)
		panic(err)
	}
	return string(jsonData)
}

func postToBigquery(job UploadData) error {
	// Create BigQuery Client:
	ctx := context.Background()
	client, err := bigquery.NewClient(ctx, "slackbot-260723")
	defer client.Close()
	if err != nil {
		println(err)
		return err
	}

	// Given struct post data to BigQuery:
	defaultDataset := client.Dataset("jobs")
	listings := defaultDataset.Table("listings")
	inserter := listings.Inserter()
	if err := inserter.Put(ctx, job); err != nil {
		println(err)
		return err
	}

	println("Data Uploaded!")
	return nil

}
