## Introduction and Dataset
For this project I decided to try to implement some methods in order to solve the Spotify Million Playlist Challenge. 

The challenge was hosted on *AIcrowd* in 2018, and since then there have been more than 1000 submission from many different teams.

The challenge consists in taking a dataset of 1 Million playlists, with 63 million tracks, of which 2 million unique ones and more than 300K artists, and build a recommender system.

Since I couldn't work with the full dataset because of hardware limitations, I sampled the 10% of it and worked with 100K playlists. The number of unique songs became around 680K with more than 100K artists.

The aim of the project was to build different recommender systems using `pyspark`, and trying to keep the data as distributed as possibile, and see how the performances kept up with the most advances methods used by the winners of the challenge.

## Visualize the Data
Before diving into the models, we can visualize the data a little bit. Here we can see the top most common songs, from this we can immediately say that hip-hop seems to be the most frequent genre.

If we analyze how many times a song appear In a playlist, we notice that most of the songs are unpopular, meaning that 662K songs out of 680K (more than 97%) appear in less than 100 playlists.

We can zoom on the frequency of the songs that appear in less than 100 playlist, and we'll notice that actually most of the songs appear just in a few playlists. This would surely be a problem for simple recommendation algorithms, since those songs won't probably never be recommended.

We can also plot a pie chart describing the most popular artist, and we can again see how much is hip hop popular.

From the histogram that describes the distribution of words used in the playlist titles, we can see that there are a lot of country playlists.

## Developed Recommender Systems (1:15 min)
Let's now see which one are the developed systems.
- I decided to start with a User-Based Collaborative Filtering system, where playlists are considered as users to which recommend new songs.
- Then I tried with an Item-Based collaborative filtering, where songs are items.
- Finally, I implemented a solution from one of the top solutions of the 2nd place team of the challenge, which uses a Denoising Autoencoder to solve the recommendation problem.

Before diving into the details of each method, let's see how the data was prepared. The dataset is split into 1000 different json files, each one with this structure:

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
        ],

    }
```

First of all I removed the file info in the header, since it was useless. 

Then we can see that for each playlist we have many details, such as the `pid`, the number of albums and tracks, the duration and the different tracks. For each tracks we have the song, album and artist uri, other than their name, along with some other information like the position in the playlist and the duration.

Using pyspark I could load all the different json files into a single DataFrame.

### User Based Collaborative Filtering
Let's now see in detail how the User-based collaborative filtering is capable of generating recommendations:

First of all, I mapped each track to a position, as we can see on this table.

The mapping is useful to encode the playlist into a binary vector, because I will put a $1$ in position $i$ if the song that has mapped the position $i$ is present in the playlist.

So let's say a playlist has this binary vector
$p = [0,0,0,0,0,1,0,1,0,1]$.
This means that it contains the songs that has the the indexed $5, 7, 9$ mapped.

As said before there are an average of $66$ songs per playlist, and a total of 600k unique tracks, the high dimensional vector will be very sparse (sparseness of 99,9903). This is a common problem for User-Based CF, but is good for memory efficiency since it's possible to encode it into a pyspark `SparseVector`.

Now, given a SparseVector as the encoding for the input playlists, that is the playlist to continuate, the pipeline is the following:
1. I compare the playlist with each other playlist, computing the pair-wise similarity using te Jaccard Similarity between their vectors. This will output a value between 0 and 1, the higher the better. I used Jaccard Similarity because I don't care about the actual values of the vector, but just the indices at which the values are.
3. I take the top-$k$ most similar playlists, where $k$ is an hyperparameter.
4. I aggregate the $k$ playlist vectors, weighting them by their respective similarity value.
5.  I then normalize the values dividing them by the sum of the $k$ similarity values.
   
   So let's say that, for k = 3, we obtain these 3 similar playlists, the aggregations results in this other playlist, which can be normalized by dividing it by the sum of similarities.
   $$p_1 = [0,1,1,0,0,1,0] \quad s_1 = 0.3
   p_2 = [0,0,1,0,1,0,0] \quad s_2 = 0.5
   p_3 = [1,0,1,0,1,0,0] \quad s_3 = 0.45$$
6. From the resulting vector, I set to 0 the position that have a $1$ in the input vector, in order to avoid recommending songs that are already in the playlist.
7.  The top-n indices with the highest values in the vector will be the positions of the n recommendations. I can just take the spotify uri that is mapped to that position in order to have all the details about the recommendation.

The entire process takes about 30 seconds for a single playlist.

### Item Based Collaborative Filtering
Regarding Item-Based collaborative filtering, the data is prepared following the same principle, but this time I have to encode the single tracks and not the playlists.

1. First of all I map each playlist to a position, just like it was done before with tracks.
2. The encoding follows the same principle of the one done by the playlist. A song is encoded in a $d$-dimensional vector, where $d$ is the number of unique playlists (100k) in the dataset. In the position $i$ there is a $1$ if the song is present in the playlist encoded with the position $i$.
   We can see that with this kind of representation, we have a smaller representation (100k of the item vector w.r.t 600k of the user vector).
	Since in average a song appears in 10 playlist, we have an even higher sparsity.
	
3. Given a playlist to continuate, represented as a DataFrame containing its song vectors, the recommendation pipeline is the following:
	1. Compute the $k$-nearest-neighbours for each track in the playlist. This will result in a collection of $T$ dataframes, where $|T|$ is the number of songs in the playlist. A dataframe relevant to the track $t$ has a list of $k$ songs, each one with the distance from $t$ in a separate column;
	2. Aggregate each Dataframe $\in T$ in order to have a single dataframe.
	   Since we are sure that the size of $T$ is not big ($T$ occupies a few kbs), I first convert the dataframes into python dictionaries. The aggregation works in this way: for each song in the collection, I put as key the position of that song, and for values a list of all the distances where the song appear. So we will obtain some dictionary like the one shown here.
	3. Then we can transform the dictionary back into a pyspark dataframe, averaging the distances inside each list and taking the opposite in order to transform them into similarities.
	4. Before performing the recommendation, we remove from the dataset the songs that already appear inside of the input playlist, in order to not recommend them.
	5. We recommend the $n$ tracks by ordering the dataframe in ascending order by distance, and taking the top-$n$ tracks with the lowest distance.

In average this whole process takes 30 to 60 seconds.

Since there are in average 66 songs in each playlist, and we have to find the $k$ neighbours for each one of them, the precise neighbour search is too expensive. 
For this I decided to use an approximate search using a Locally Sensitive Hashing algorithm, implemented by pyspark's `MinHashLSH`.
Regarding the number of hash tables, the higher the number, the more precise but less fast; the lower, the less precise but the faster the algorithm is. I tried with both 10 and 20 as values, we will see the results later.

In order to reduce the algorithm inference time, we can pre-compute the list of k-neighbours for each song in advance. This is surely a great idea, but I didn't do it since it took something like a week.

### Denoising Auto-Encoder
Regarding the Neural Network Approach, I took the second place solution of the official spotify challenge, created by  a team called Hello World, which built a recommender system using an ensamble made out of a Denoising Autoencoder, that tries to reconstruct the playlist, and a Character Level CNN in order to recommend songs from the playlist title. For simplicity, I only tried to replicate the Autoencoder part.

The autoencoder works in this way:
It takes in input the concatenation of both the songs and artists vector encodings. The song vector is built exactly as for the other models, and the artist vector follows the same principle, meaning there is a $1$ in the position $i$ if the artist $i$ appears inside of the playlist, $0$ otherwise.

It's trained to reconstruct the input playlist. The intuition is that songs with high values in the reconstructed vectors are relevant for the input playlist.

In order to let the model generalize the reconstruction, we generate some noise in the input vector. The first method for noise generation, that is done during training, is called Hide & Seek. It consists in masking one of the two vectors in the concatenation randomly at each iteration. 
In this way the model has to reconstruct the concatenation of songs and artists only from one of the elements, and so has to learn the relationship between songs and artists to achieve a better reconstruction.

In order to let the model generalize even more, dropout it's applied, with a probability $p$ of staying randomly chosen from 0.5 to 0.8. This acts also as regularization, and so no further regularization, like L1 or L2 is needed. 

To maintain the distribution of the data I used Petastorm, which is an open source library made at Uber that allows to create a DataLoader for PyTorch or Tensorflow from a pyspark database, while maintaining the data distributed. The model is the fed with mini-batches of data.

Regarding the loss, the authors of the paper use Binary Cross Entropy with a weighting scheme different from observed values (ones in the vector) and missing values (zeros in the vector).
$$\mathcal{L}(\mathbf{p}, \hat{\mathbf{p}})=-\frac{1}{n} \sum_{\mathbf{p} \in \mathbf{P}} p_i \log \hat{p}_i+\alpha\left(1-p_i\right) \log \left(1-\hat{p}_i\right)$$
$\alpha$ is the weighting factor, and it's put to 0.5, in order to weight missing values less.

At inference time, the whole concatenation of songs and artists it's predicted, but only the song part it's considered. The recommendation is made out of the top-n songs with the highest values, that are not already present in the original playlist.

%%The training is divided in two phases. In the first phase, the model has tied weights, meaning the weights of the encoder and the decoder are shared. This allows for a faster training. The model is trained for 50 epochs, and then the parameters are used as initialization for the Autoencoder without tied weights, where it's trained for 100 epochs. The best parameters are saved when the best precision is achieved on the validation set, which is evaluated for each epoch.%%

I left the same hyperparameters used by the authors of the paper, but adjusted the learning rate to be 10x smaller, since I have a smaller dataset to work with.

%%The training took about 12 hours using CUDA GPUs on colab pro. I opted for colab pro otherwise the training on CPU would require too much time.%%

## Train-Test Split
Regarding the train-test split, I had to use two different strategies depending on the models.

If the model doesn't need a training part, then the dataset is split at track level, otherwise it's split at row level. Let's see what this mean.

Regarding the models without the training, the train-test split happens at the tracks level. Meaning that we divide the original dataframe in two dataframes, each one with the same playlists, but with different songs. 25% of the songs are sampled and put into the playlist in the test-set, while the remaining 75% of the songs are put in the train-set. In this way we can use the playlists in the train-set to generate the list of recommendations, while the songs in the test-set will be the ground truth.

For what concerns the model with training, we need three different dataframes, for Training, Validation and Testing, without common playlist among them.

So let's say this is the original dataframe, the split now happens at row level, which will produce three different dataframes.

Then, since I have to compute evaluation metrics on the validation and test set, I also have to split them but at track level.

## Evaluation Metrics
The models are evaluated with two different metrics.

Let $G$ be the unordered list of left out tracks, and let $R$ be the list of recommended tracks, ordered by confidence.

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
## Comparing the performances of the different methods
Finally we can see the performances of each model. We can see that the User-Based CF performed well, considering the simplicity of the model.

The item-based, on the other hand, had worse performances. We can also see how with more hash tables the performances are a little bit higher.

And as expected the Neural Network based model is the one that has the best performances.

The models used by the winners of the challenge has a R-Precision of 0.22 and a NDCG of 0.38. Considering the fact that they are complex models and  1 million playlists, I'm very satisfied on how the models used in this project performed with just a tenth of the data.

## Conclusions
In conclusion, we can see that simple model performs good on recommender systems tasks.

In the project the data is kept distributed most of the times, expect for plots, where the data was converted into a Pandas dataframe. 

The use of libraries like Petastorm allowed to keep the distribution, even if the training happens on the master node. Distributed training could be done using other libraries, but this was avoided in order to not overcomplicate the project.
