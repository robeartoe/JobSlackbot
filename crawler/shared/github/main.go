package github

import (
	"encoding/json"
	"fmt"
	"net/http"
	"net/url"
	"sync"
	"time"

	library "github.com/robeartoe/JobSlackbot/crawler/shared/interfaces"
	"github.com/robeartoe/JobSlackbot/crawler/shared/pubsub"
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
func Crawl(searchData library.SearchData) error {
	// Idea is to use channels, to separate all of these job & location queries into their own separate things. Then merge the results into one array.
	// After the array is returned, it is sent to another function to be transformed.

	// Get all combinations and create an array of searchTerm[]
	combinations := getPermutations(searchData)

	var builtData []library.JobPostingData

	// Setup Channel to fetch all results:
	c := make(chan githubResult, len(combinations))
	var wg sync.WaitGroup
	for _, combination := range combinations {
		wg.Add(1)
		go fetchJobs(combination, c, &wg)
	}
	wg.Wait()
	close(c)
	for result := range c {
		if result.Error != nil {
			fmt.Println("Failed Fetch!")
			return result.Error
		}
		// If no error, build the data:
		builtData = append(builtData, buildJobPostings(result)...)
	}

	cPubSub := make(chan []library.PubSubData)
	var err error
	go pubsub.Publish(builtData, cPubSub)
	pubSubs := <-cPubSub
	for _, result := range pubSubs {
		if result.Error != nil {
			err = result.Error
			break
		}
	}
	return err
}

// https://www.oreilly.com/library/view/concurrency-in-go/9781491941294/ch04.html#callout_concurrency_patterns_in_go_CO7-1
// Fetch request and json
func fetchJobs(job searchTerm, c chan githubResult, wg *sync.WaitGroup) {
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
	defer wg.Done()
}

// buildJobPostings builds a standardized job posting array that will be sent to the pubsub queue.
func buildJobPostings(data githubResult) []library.JobPostingData {
	var fullData []library.JobPostingData
	for i := 0; i < len(data.Posts); i++ {
		created, err := time.Parse(`"`+time.UnixDate+`"`, data.Posts[i].Created)
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
			Source:     "github",
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
