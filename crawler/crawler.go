package crawler

import (
	"encoding/json"
	"fmt"
	"net/http"

	github "github.com/robeartoe/JobSlackbot/crawler/internal/github"
	indeed "github.com/robeartoe/JobSlackbot/crawler/internal/indeed"
	library "github.com/robeartoe/JobSlackbot/crawler/internal/interfaces"
)

// SearchData defines job search data to be passed into the crawl function.

// HTTPServer is an HTTP Cloud Function with a request parameter.
func HTTPServer(w http.ResponseWriter, r *http.Request) {
	var d library.SearchData

	err := json.NewDecoder(r.Body).Decode(&d)
	if err != nil {
		w.WriteHeader(http.StatusBadRequest)
		w.Write([]byte("400 - Invalid Parameters!"))
		return
	}

	results, error := crawl(d)
	if error != nil {
		http.Error(w, error.Error(), http.StatusInternalServerError)
	}
	w.WriteHeader(http.StatusOK)
	w.Header().Set("Content-Type", "application/json; charset=utf-8")
	json.NewEncoder(w).Encode(results)
}

func crawl(searchData library.SearchData) (string, error) {
	result := "testresult"
	var err error

	switch searchData.Source {
	case "indeed":
		indeed.Crawl()
		return result, err
	case "github":
		result, err := github.Crawl(searchData)
		return result, err
	default:
		fmt.Println("Hello World!")
		return "result", err
	}
}
