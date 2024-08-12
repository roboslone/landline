# landline
A simple service that runs voice recognition on given files and uploads results to Notion database.  
It's using [Whisper](https://github.com/openai/whisper) for voice recognition.

## Building
Replace `<tag>` with actual tag, e.g. `0.0.2`.
```
docker build -f deploy/Dockerfile . -t roboslone/landline:<tag>
docker push roboslone/landline:<tag>
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
