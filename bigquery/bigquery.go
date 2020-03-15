package bigquery

import (
	"encoding/json"
	"net/http"
)

// Post defines slack Message JSON data to be passed into PostMessage
type Post struct {
	Text  string `json:"text"`
	Emoji string `json:"emoji"`
}

// HTTPServer is an HTTP Cloud Function with a request parameter.
func HTTPServer(w http.ResponseWriter, r *http.Request) {
	var d Post

	err := json.NewDecoder(r.Body).Decode(&d)
	if err != nil {
		w.WriteHeader(http.StatusBadRequest)
		w.Write([]byte("400 - Invalid Parameters!"))
		return
	}

	postToBigquery()

	// msg, err := PostMessage(d)
	// if err != nil {
	// 	http.Error(w, err.Error(), http.StatusInternalServerError)
	// }
	// w.WriteHeader(http.StatusOK)
	// w.Header().Set("Content-Type", "application/json; charset=utf-8")
	// json.NewEncoder(w).Encode(msg)
}

func postToBigquery() {
	println("hello!")
}
