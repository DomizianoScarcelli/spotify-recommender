# Data Preparation

In order for spark to read the playlist dataset, I needed to remove the metadata about each playlist file, meaning the top part:

```json
{
	"info": {
		"generated_on": "2017-12-03 08:41:42.057563",
		"slice": "0-999",
		"version": "v1"
	}
}
```

I zipped the collection of `json` files with the `zipfile` python library in order to not include the hidden `__MACOS` folder that would corrupt the pyspark dataframe when passing the zip file to create the dataframe.

Using the official Spotify API, I also downloaded, for each song, the audio features of that song and put all of them in a different JSON file, in order to load them into a pySpark dataframe.

To do that, I extracted the list of all songs ID from all the playlist JSON files, and I called the Spotify API in batches of 1000 songs (the maximum allowed for each API call) for a total of ${2,000,000 \over 1,000} = 2,000$ API calls.

# Data esploration
