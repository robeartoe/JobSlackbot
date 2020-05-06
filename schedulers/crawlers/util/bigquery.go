package util

import (
	"context"
	"fmt"
	"time"

	"cloud.google.com/go/bigquery"
)

func Query(ctx context.Context, client *bigquery.Client, today time.Time) (*bigquery.RowIterator, error) {
	queryString := fmt.Sprint("SELECT * FROM `slackbot-260723.jobs.listings` WHERE InsertDate=", today.Format(time.UnixDate))
	query := client.Query(queryString)
	return query.Read(ctx)
}

func ReadQuery() {

}
