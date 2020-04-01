package github

import (
	"bufio"
	"bytes"
	"encoding/json"
	"fmt"
	"net/http"
	"net/url"
	"time"

	library "github.com/robeartoe/JobSlackbot/crawler/internal/interfaces"
	"github.com/robeartoe/JobSlackbot/crawler/internal/pubsub"
)

func new(search string, location string) searchTerm {
	return searchTerm{
		search:   search,
		location: location,
		// fullTime: fullTime,
	}
}

type searchTerm struct {
	search   string
	location string
	// fullTime bool
}

type githubResult struct {
	Error error
	Posts []post
}

type post struct {
	Company    string `json:"company,omitempty"`
	CompanyURL string `json:"company_url,omitempty"`
	Location   string `json:"location,omitempty"`
	Title      string `json:"title,omitempty"`
	HowToApply string `json:"how_to_apply,omitempty"`
	URL        string `json:"url,omitempty"`
	JobType    string `json:"type,omitempty"`
	Created    string `json:"created_at,omitempty"`
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
		go fetchJobs(combinations[i], c)
	}

	for result := range c {
		if result.Error != nil {
			fmt.Println("Failed Fetch!")
		}
		// If no error, build the data:
		builtData = append(builtData, buildJobPostings(result)...)
	}

	// Setup Channel to post to Pub/Sub:
	cPubSub := make(chan library.PubSubData)
	for j := 0; j < len(builtData); j++ {
		var b bytes.Buffer
		buf := bufio.NewWriter(&b)
		go pubsub.Publish(buf, builtData[j], cPubSub)
	}

	for result := range cPubSub {
		if result.Error != nil {
			return "", result.Error
		}
		fmt.Print(result.Id)
	}
	return "Success!", nil
}

// https://www.oreilly.com/library/view/concurrency-in-go/9781491941294/ch04.html#callout_concurrency_patterns_in_go_CO7-1
// Fetch request and json
func fetchJobs(job searchTerm, c chan githubResult) {
	defer close(c)

	var result []post
	baseURL, err := url.Parse("https://jobs.github.com/positions.json")
	if err != nil {
		c <- githubResult{Error: err}
	}
	params := url.Values{}
	params.Add("search", job.search)
	params.Add("location", job.location)
	baseURL.RawQuery = params.Encode()

	formattedValue := baseURL.String()
	resp, err := http.Get(formattedValue)
	if err != nil {
		c <- githubResult{Error: err}
	}

	errBody := json.NewDecoder(resp.Body).Decode(&result)
	if errBody != nil {
		c <- githubResult{Error: errBody}
	}

	c <- githubResult{Posts: result}
	defer resp.Body.Close()
}

// buildJobPostings builds a standardized job posting array that will be sent to the pubsub queue.
func buildJobPostings(data githubResult) []library.JobPostingData {
	var fullData []library.JobPostingData
	for i := 0; i < len(data.Posts); i++ {
		created, err := time.Parse(`"`+time.RFC3339+`"`, data.Posts[i].Created)
		if err != nil {

		}
		fullData = append(fullData, library.JobPostingData{
			Company:    data.Posts[i].Company,
			CompanyURL: data.Posts[i].CompanyURL,
			Location:   data.Posts[i].Location,
			Title:      data.Posts[i].Title,
			HowToApply: data.Posts[i].HowToApply,
			URL:        data.Posts[i].URL,
			JobType:    data.Posts[i].JobType,
			Created:    created,
			Data:       data.Posts[i],
		})
	}
	return fullData
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
