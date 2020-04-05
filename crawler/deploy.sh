go mod vendor
gcloud functions deploy crawler --entry-point HTTPServer --runtime go113 --trigger-http --allow-unauthenticated
# Don't forget, run the command go mod vendor to move the sub modules into the vendor folder.