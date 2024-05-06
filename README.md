# Image API Service

## Dependencies

- Docker
- GNU make (comes with most unix systems)

## Local setup

Run the following command:

```bash
make prod
```

Service should now be running on: [http://localhost:8000](http://localhost:8000)

API Docs can be found at: [http://localhost:8000/docs](http://localhost:8000/docs)

## Implementation details

- I'm assuming that it's an internal service (e.g. I'm not adding any security in form of API keys)

Implementation notes on endpoints:

- `/crop` - since we are handling the processing of the image on the host machine, we use a background process to make sure we remove any temporary files we might have created
- `/difference` - I've made the assumption that we're interested in variations of very similar images, and so I'm using `dhash` to calculate the difference.
  According to this [article](https://www.hackerfactor.com/blog/index.php?/archives/529-Kind-of-Like-That.html), a value of 0 is a very similar image, and anything over 10 is probably a different image.
  So I have normalized it with a max of 10, so any value above 1 is likely more than a variation. I used the `dhash` algorithm because they specify that it's less sensitive to a general change in lighting.

- `/hash` - I'm assuming this hash can be used as an identifier, and that the image integrity is preserved.
