package github

import (
	"encoding/json"
	"fmt"
	"net/http"
	"time"

	library "github.com/robeartoe/JobSlackbot/crawler/internal/interfaces"
)

type searchTerm struct {
	search   string
	location string
	// fullTime bool
}

func new(search string, location string) searchTerm {
	return searchTerm{
		search:   search,
		location: location,
		// fullTime: fullTime,
	}
}

type githubResult struct {
	Error      error
	Company    string    `json:"company,omitempty"`
	CompanyURL string    `json:"company_url,omitempty"`
	Location   string    `json:"location,omitempty"`
	Title      string    `json:"title,omitempty"`
	HowToApply string    `json:"how_to_apply,omitempty"`
	URL        string    `json:"url,omitempty"`
	JobType    string    `json:"type,omitempty"`
	Created    time.Time `json:"created_at,omitempty"`
}

// Crawl Github's API given Job & Location Queries
func Crawl(searchData library.SearchData) (string, error) {
	// Idea is to use channels, to separate all of these job & location queries into their own separate things. Then merge the results into one array.
	// After the array is returned, it is sent to another function to be transformed.

	// Get all combinations and create an array of searchTerm[]
	combinations := getPermutations(searchData)

	var builtData []library.JobPostingData

	// Setup Channel to fetch all results:
	c := make(chan githubResult)
	for i := 0; i < len(combinations); i++ {
		go fetchJob(combinations[i], c)
	}

	for result := range c {
		if result.Error != nil {
			fmt.Println("Failed Fetch!")
		}
		// If no error, build the data:
		builtData = append(builtData, buildJobPostings(result))
	}

	// Setup Channel to post to Pub/Sub:
	cPubSub := make(chan library.PubSubData)

	// results, err := fetchJob()
	// if (err != nil) {
	// return "", err
	// }

	return string(body), nil
}

// https://www.oreilly.com/library/view/concurrency-in-go/9781491941294/ch04.html#callout_concurrency_patterns_in_go_CO7-1
// Fetch request and json
func fetchJob(jobs searchTerm, c chan githubResult) {
	defer close(c)

	var result githubResult

	formattedValue := fmt.Sprintf("https://jobs.github.com/positions.json?search=%s&location=%s", jobs.search, jobs.location)
	resp, err := http.Get(formattedValue)
	if err != nil {
		c <- githubResult{Error: err}
	}

	errBody := json.NewDecoder(resp.Body).Decode(&result)
	if errBody != nil {
		c <- githubResult{Error: errBody}
	}

	c <- result
	defer resp.Body.Close()
}

// buildJobPostings builds a standardized job posting array that will be sent to the pubsub queue.
func buildJobPostings(data githubResult) library.JobPostingData {
	return library.JobPostingData{
		Company:    data.Company,
		CompanyURL: data.CompanyURL,
		Location:   data.Location,
		Title:      data.Title,
		HowToApply: data.HowToApply,
		URL:        data.URL,
		JobType:    data.JobType,
		Created:    data.Created,
		Data:       data,
	}
}

// Gets all permutations of all the queries, and locations. Returns array of objects.
func getPermutations(data library.SearchData) []searchTerm {
	var results []searchTerm
	for i := 0; i < len(data.JobQuery); i++ {
		for j := 0; j < len(data.LocationQuery); j++ {
			results = append(results, new(data.JobQuery[i], data.LocationQuery[j]))
		}
	}
	return results
}
