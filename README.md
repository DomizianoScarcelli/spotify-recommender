The Spotify Million Playlist challenge consists in taking a dataset of 1 Million playlists, in order to build a recommender system that will continuate the playlist with coherent tracks.
The original Dataset is created by users on Spotify between January 2010 and October 2017, and contains more than 2 million unique tracks by nearly 300k artists.

Due to hardware limitations I couldn't work with the full dataset, so I sampled the 10% of it, and worked with 100k playlists. The total number of unique songs becomes around 600k, with 100k artists.
The aim of this project was to build different recommenders systems using pyspark in order to "be distributed", and see how the performances kept up with the most advanced techniques by the winners of the challenge.

## Developed Recommender Systems

The models that I developed are three:

-   User-Based Collaborative Filtering, considering the playlist as an user to which make the recommendation
-   Item-Based Collaborative Filtering, considering the songs as items.
-   Denoising AutoEncoder: I took the solution of one of the top solutions of the challenge, and adapt it in order to use the data in a distributed manner.

Before diving into the details of each method, let's see how the data was prepared. The dataset is split in different json files, each one with this structure:

```json
{
	"name": "musical",
	"collaborative": "false",
	"pid": 5,
	"modified_at": 1493424000,
	"num_albums": 7,
	"num_tracks": 12,
	"num_followers": 1,
	"num_edits": 2,
	"duration_ms": 2657366,
	"num_artists": 6,
	"tracks": [
		{
			"pos": 0,
			"artist_name": "Degiheugi",
			"track_uri": "spotify:track:7vqa3sDmtEaVJ2gcvxtRID",
			"artist_uri": "spotify:artist:3V2paBXEoZIAhfZRJmo2jL",
			"track_name": "Finalement",
			"album_uri": "spotify:album:2KrRMJ9z7Xjoz1Az4O6UML",
			"duration_ms": 166264,
			"album_name": "Dancing Chords and Fireflies"
		}
	]
}
```

First of all I removed the file metadata in the header, since it was useless. Then we can see that for each playlist we have many details, such as the `pid`, the number of albums and tracks, the duration and the different tracks. For each tracks we have the song, album and artist uri, other than their name, along with some other information like the position in the playlist and the duration.

![[Screenshot 2023-06-22 at 7.36.28 PM.png]]

### User Based Collaborative Filtering

Let's start with the first method, the User-Based Collaborative Filtering.
First I mapped each track to a position, that will become useful in order to encode each playlist with binary vector encoding, in which a $1$ in position $i$ means that the song that has mapped the position $i$ is present in the playlist.
$p = [0,0,0,0,0,1,0,1,0,1]$.
Since there are an average of $66$ songs per playlist, and a total of 600k unique tracks, the 600k dimensional vector will be very sparse. This is good for memory efficiency since it's possible to encode it into a pyspark `SparseVector`.

Now, given a SparseVector as the encoding for the input playlists, that is the playlist to continuate, the pipeline is the following:

1. I compare the playlist with each other playlist, computing the pair-wise similarity using te Jaccard Similarity between their vectors. This will output a value between 0 and 1, the higher the better.
2. I take the top-$k$ most similar playlists, where $k$ is an hyperparameter.
3. I aggregate the $k$ playlist vectors, weighting them by their respective similarity value.
    $$
    p_1 = [0,1,1,0,0,1,0] \quad s_1 = 0.3
    p_2 = [0,0,1,0,1,0,0] \quad s_2 = 0.5
    p_3 = [1,0,1,0,1,0,0] \quad s_3 = 0.45
    $$
4. From the resulting vector, I set to 0 the position that have a $1$ in the input vector, in order to avoid recommending songs that are already in the playlist.
5. The top-n indices with the highest values in the vector will be the positions of the n recommendations. I can just take the spotify uri that is mapped to that position in order to have all the details about the recommendation.

### Item Based Collaborative Filtering

User based collaborative filtering has some problems, like the fact that it ages very quickly. Let's see how the item-based CF is implemented:

1. This time I have to encode tracks, that are the items, instead of users. The encoding follows the same principle of the one done by the playlist. An item is encoded in a $d$-dimensional vector, where $d$ is the number of unique playlists (100k) in the dataset. In the position $i$ there is a $1$ if the song is present in the playlist encoded with the position $i$.
   We can see that with this kind of representation, we have a smaller representation (100k of the item vector w.r.t 600k of the user vector).

2. Given a playlist to continuate, we compute the $k$-nearest-neighborus for each track that is present in the playlist. Since in average there are about $66$ songs in each playlist, we have to perform this computation about $66$ times. From here we can do two things:

    1. Perform this 66 average computation each time a playlist has to be continuated
    2. Pre-compute all the k-nearest-neighbours for all the possible 600k songs.
       Even if the second options makes the most sense, because it make the algorithm a lot faster, I sticked with the first one because the complete computation took too long (about 5-7 days). The nearest neighbours search results in this dataframe:
       `track_uri, embedding, hashes, distcol`.

3. Given the set of $n$ dataframes, each one representing the $k$ nearest neighbours of one of the playlist tracks, we want to aggregate them in order to average them into a single dataframe, weighting it by their similarity. At this level, we are sure that we are not working with a small amount of data, for this reason we will convert each dataframe produced by the nearest-neighbour search into a python dictionary:

```python
{track_uri: distance}
```

We will merge the $n$ dataframes in order to obtain an aggregated python dictionary, where the keys are all the unique songs in all the dataframes, and the relative value is the list of distances that they have in the different dataframe where they appear (this can be a single value if the song appears only in a single dataframe, or more than one otherwise.)
The aggregated dataframe will be something like this:

```json
{
	"spotify:track:001BVhvaZTf2icV88rU3DA": [0.0, 0.0],
	"spotify:track:1iO2inxYIzmPnMuDFfU1Rl": [0.8571428571428572, 0.8571428571428572],
	"spotify:track:3Ff2kaO1uxXjd9HkHfMw4h": [0.8571428571428572, 0.8571428571428572],
	"spotify:track:2EhgEpfn3U0lmpryqDujwt": [0.8571428571428572, 0.8571428571428572],
	"spotify:track:3lkFKOOQRp1AqWk2PPAW6B": [0.8571428571428572, 0.8571428571428572],
	"spotify:track:4OEHuq3q8kjkPS1jKI96JP": [0.8571428571428572, 0.8571428571428572],
	"spotify:track:6kucDoXP5pBdFA7GxwgFP2": [0.8571428571428572, 0.8571428571428572],
	"spotify:track:3DeMqzJj9477nCcyTXl3Ye": [0.8571428571428572, 0.8571428571428572],
	"spotify:track:558Km9MuklF6yKJDVVjIli": [0.8571428571428572, 0.8571428571428572],
	"spotify:track:50r5hQgwJ61tCwEL1maGsG": [0.8571428571428572, 0.8571428571428572]
}
```

4. Now we transform this python dictionary back to a pandas dataframe, averaging the values inside of each list. The final dataframe will look like this: ![[Screenshot 2023-06-25 at 6.08.15 PM.png]]
5. Before performing the recommendation, we remove from the dataset the songs that already appear inside of the input playlist, in order to not recommend them.
6. We recommend the $n$ tracks by ordering the dataframe in ascending order by distance, and taking the top-$n$ tracks with the lowest distance.

In average this whole process takes 1 minute, that is a little bit of time, but this may be reduces by pre-computing the list of k-neighbours for each song in advance.

### Denoising Auto-Encoder

The second place solution of the official spotify challenge was taken by a team called Hello World, which built a recommender system using an ensamble made out of a Denoising Autoencoder, that tries to reconstruct the playlist, and a Character Level CNN in order to recommend songs from the playlist title. For simplicity, I only tried to replicate the Autoencoder part.

The autoencoder works in this way:
![[Screenshot 2023-06-26 at 11.42.44 AM.png]]
It takes in input the vector encoding of the songs in the playlist, and the artists. The song vector is built exactly as for the other models, and the artist vector follows the same principle, meaning there is a $1$ in the position $i$ if the artist $i$ appears inside of the playlist, $0$ otherwise.
The models is then trained with a technique called Hide & Seek, meaning each iteration, one of the two vector is randomly removed, meaning all its elements are put to 0, and so the model has to reconstruct the concatenation of songs and artists only from one of the elements. In order to let the model generalize even more, dropout it's applied, with a probability $p$ of staying randomly chosen from 0.5 to 0.8. This acts also as regularization, and so no further regularization, like L1 or L2 is needed. Regarding the loss, the authors of the paper use Binary Cross Entropy with a weighting scheme different from observed values (ones in the vector) and missing values (zeros in the vector).
$$\mathcal{L}(\mathbf{p}, \hat{\mathbf{p}})=-\frac{1}{n} \sum_{\mathbf{p} \in \mathbf{P}} p_i \log \hat{p}_i+\alpha\left(1-p_i\right) \log \left(1-\hat{p}_i\right)$$
$\alpha$ is the weighting factor, and it's put to 0.5, in order to weight missing values less.
At inference time, the whole concatenation of songs and artists it's predicted, but only the song part it's considered. The recommendation is made out of the top-n songs with the highest values, that are not already present in the original playlist.

What I did was to rewrite the Denoising Autoencoder in Pytorch, and construct the DataLoaders for the different training, validation and test set with Petastorm, that is a library made at Uber that allows to build the DataLoaders for common Deep Learning Frameworks giving a Pyspark Dataframe. This is very useful since the data is kept distributed, and the model is fed with single mini-batches of data.

The training is divided in two phases. In the first phase, the model has tied weights, meaning the weights of the encoder and the decoder are shared. This allows for a faster training. The model is trained for 50 epochs, and then the parameters are used as initialization for the Autoencoder without tied weights, where it's trained for another 50 epochs. The best parameters are saved when the best precision is achieved on the validation set, which is evaluated for each epoch.

I left the same hyperparameters used by the authors of the paper, but adjusted the learning rate to be 10x smaller, since I have a smaller dataset to work with.

The training took about 10 hours using CUDA GPUs on colab pro. I opted for colab pro otherwise the training on CPU would require too much time.

# Performance Evaluation

## Evaluation Metrics

AI Crowd provides a challenge dataset which purpose is to evaluate the model. This dataset is made out of playlist with some missing tracks. The model should take in input the seed tracks (which are the tracks that are in the playlist) and output as many tracks as the missing ones. Let $G$ be the unordered list of left out tracks, and let $R$ be the list of recommended tracks, ordered by confidence.
The metrics of evaluation are two:

1. R-Precision: it measures the number of relevant tracks that are actually recommended by computing the ratio of how many recommended tracks are equal to the missing tracks, divided by the total number of missing tracks. Formally:
    $$
    \text{Rprec} = \frac{G \cap R_{1:|G|}}{|G|}
    $$
2. Normalized Discounted Cumulative Gain: it measures how down much up in the list are the tracks that are relevant and recommended. The value is higher, the more relevant recommended tracks are in the first positions. We have first to compute the Discounted Cumulative Gain as:
   $$D C G=r e l_1+\sum_{i=2}^{|R|} \frac{r e l_i}{\log _2 i}$$
   and then dividing it by the Ideal Discounted Cumulative Gain, that is the maximum $DCG$ achievable:
   $$I D C G=1+\sum_{i=2}^{|G \cap R|} \frac{1}{\log _2 i}$$
   so the final metric would be:
   $$NDCG = \frac{DCG}{IDCG}$$

## Train-Test Split

The User based and Item Based CF don't need training, meanwhile the Neural Network approach does. Because of that, we have to use two different train-test split strategies.

### Collaborative Filtering Train-Test Split

Regarding the models without the training, the train-test split happens at the tracks level. Meaning that we divid the original dataframe in two dataframes, each one with the same playlists, but with different songs. 25% of the songs are sampled and put into the playlist in the test-set, while the remaining 75% of the songs are put in the train-set. In this way we can use the playlists in the train-set to generate the list of recommendations, while the songs in the test-set will be the ground truth.

### Neural Network Train-Test Split

Here the situation is more complex. First because the model has a training phase, so it need of a training set with playlists that do not appear in the test set. Then we also need a validation set in order to do optimize the hyperparameters, and do early-stopping, in order to save the model in the state which optimize the evaluation metrics computed on the validation set.
Then, for both the Validation and Test set, we also have to split each dataframe into two dataframes at the track level, as described before, in order to have a set of ground-truth tracks to compute the evaluation on.

The Train Set contains the 98.5% of the playlists, while the remaining 1% is used for testing, and the 0.5% for validation. These seems like very little slices, but they are ok since the model needs plenty of data to be more precise, and in the official challenge the test set has 10k playlists (which is the 0.1% of the 1 million train dataset). Since we have a total of 100k playlist, we will have 98.5K playlist for training, 500 for validation and 1k for testing.

## Comparing the performances of the different methods

Regarding the User-Based CF, the model was evaluated on 1000 random sampled playlists, and the performances are the following:
R-Precision: 0.1, NDCG: 0.3

For what concerns the Item-Based CF, the model was evaluated on the same 1000 playlists, and the performances are:
R-precision: ?, NDCG: ?

And lastly, the Autoencoder model was evaluated with the same 1000 playlists, and the performances are:
R-Precision: ?, NDCG: ?.

We can see that the performances are not bad, considering the simplicity of the models and the less data. Comparing them to the winners of the challenge, which used more complex models, the performances, evaluated on 10k playlists in the provided challenge dataset are:
R-Precision: 0.22, NDCG: 0.38.

## Conclusions

In conclusion, we can see that simple model performs good on recommender systems tasks. As expected, the first model is the one that performs worst, followed by the item-based, which performs a little bit better. As happens most of the time, the model that performs better is the Neural Network based, even if the data is smaller, and without the ensamble part. In the project the data is kept distributed most of the times, expect for plots, where the data was converted into a Pandas dataframe. The use of libraries like Petastorm allowed to keep the distribution, even if the training happens on the master node. Distributed training could be done using other libraries, but this was avoided in order to not overcomplicate the project.

I also built a little web app that demonstrates the use of the application by a final user. In the webapp the user can build a playlist using the songs that are in the dataset, and then make the system continuate it. For simpliciy, the webapp uses only the User-Based Collaborative Filtering technique.

DEMO OF THE APP
