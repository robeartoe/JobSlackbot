package util

import (
	"context"
	"fmt"
	"time"

	"cloud.google.com/go/bigquery"
	"google.golang.org/api/iterator"
)

// JobPostingData is standard data across entire application
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
	InsertDate time.Time
	Data       string
}

// Query gets BigQuery data from today's date.
func Query(ctx context.Context, client *bigquery.Client, today time.Time) ([]JobPostingData, error) {
	year, month, day := today.Date()

	queryString := fmt.Sprintf("SELECT * FROM `slackbot-260723.jobs.listings` WHERE InsertDate>='%v-%v-%v'", year, int(month), day)
	query := client.Query(queryString)

	rows, err := query.Read(ctx)
	if err != nil {
		return nil, err
	}
	data, err := readQuery(rows)
	if err != nil {
		return nil, err
	}
	return data, nil
}

func readQuery(rows *bigquery.RowIterator) ([]JobPostingData, error) {
	var data []JobPostingData
	for {
		var row JobPostingData
		err := rows.Next(&row)
		if err == iterator.Done {
			break
		}
		if err != nil {
			return nil, err
		}
		data = append(data, row)
	}
	return data, nil
}
