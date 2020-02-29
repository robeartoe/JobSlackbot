gcloud functions deploy lib --entry-point HTTPServer --runtime go113 --trigger-http --allow-unauthenticated --env-vars-file .env.yaml
