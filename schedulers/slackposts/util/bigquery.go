package util

import (
	"context"
	"fmt"
	"time"

	"cloud.google.com/go/bigquery"
	"google.golang.org/api/iterator"
)

// Query gets BigQuery data from today's date.
func Query(ctx context.Context, client *bigquery.Client, today time.Time) (string, error) {
	year, month, day := today.Date()

	queryString := fmt.Sprintf("SELECT * FROM `slackbot-260723.jobs.listings` WHERE InsertDate>='%v-%v-%v'", year, int(month), day)
	fmt.Println(queryString)
	query := client.Query(queryString)

	rows, err := query.Read(ctx)
	if err != nil {
		return "", err
	}

	return readQuery(rows)
}

func readQuery(rows *bigquery.RowIterator) (string, error) {
	for {
		var values []bigquery.Value
		err := rows.Next(&values)
		if err == iterator.Done {
			fmt.Println("DONE Iterating!")
			break
		}
		if err != nil {
			// TODO: Handle error.
			return "Error", err
		}
		fmt.Println(values)
	}
	return "nil", nil
}
