# landline
A simple service that runs voice recognition on given files and uploads results to Notion database.  
It's using [Whisper](https://github.com/openai/whisper) for voice recognition.

## Building
```
docker build -f deploy/Dockerfile . -t roboslone/landline:0.0.1
docker push roboslone/landline:0.0.1
```

## Running
In this example `landline` will process recordings from iCloud. Sharing is required.  
```
docker run \
  -e LANDLINE_NOTION_TOKEN \
  -e LANDLINE_NOTION_DATABASE_ID \
  -v /Users/roboslone/Library/Group\ Containers/group.com.apple.VoiceMemos.shared/Recordings:/Recordings \
  roboslone/landline:0.0.1
```
