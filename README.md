# flicker_api(Flask|PostgreSQL)
Sample Flask app to fetch the images from Flicker using Flicker API

## 1. Initiate the image fetch API request
Request: https://{{server}}/get-images

Response: 
```
{
"status": "Waiting to process",
"id": "c3a0fc64-684f-4733-96ff-e4f80496340e"
} 
```
## 2. Get the status of the above API request
Request: https://{{server}}/get-image-status?uid=c3a0fc64-684f-4733-96ff-e4f80496340e

Response: 
### if process completed

```
{
"status": "Completed",
"id": "c3a0fc64-684f-4733-96ff-e4f80496340e"
} 
```

### if process not completed

```
{
"status": "Completed",
"result": [
            {
            "image_url": "https://farm66.staticflickr.com/65535/49979695478_b7b9711aa6.jpg"
            },
            {
            "image_url": "https://farm66.staticflickr.com/65535/50600578397_c73781ff3f.jpg"
            },
            ...
            ...
         ]
} 
```
