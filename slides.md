---
theme: default
transition: slide-left
css: windicss
layout: cover
title: <logos-spotify class="pr-120 w-2xl"/>
---

<style>
    @font-face {
    font-family: Gotham;
    src: url(./fonts/Spotify-Font/GothamMedium.ttf);
    }
    *{
        font-family: "Gotham";
    }
    h1{
        color: #1ED760;
    }
    .slidev-layout table {
        padding: 1rem, 0, 1rem, 0 !important;
        font-size: 14px !important;
        width: 30% !important; 
    }

    .col-right {
        padding-top: 3rem;
    }
</style>

# <logos-spotify class="pr-120 w-2xl"/>

<h1 class="text-gray-100">Million Playlist Challenge</h1>
<p>by Domiziano Scarcelli - 1872664</p>

<!-- 
For this project I decided to try to implement some methods in order to solve the Spotify Million Playlist Challenge.  
-->


---

# Introduction

Recommender System for Playlist Continuation

-   Challenge started in 2018
-   Hosted on AIcrowd
-   More than 1000 submissions

<v-click>

## Dataset:

</v-click>

<v-clicks>

- 1 Million Playlists
- 63 Million total songs
- 2 Million unique songs
- 345K unique artists

</v-clicks>

<v-clicks>

Playlists created by users from 2010 to 2017

A song recommender is an essential feature to enable an easy discoverability of new songs.

</v-clicks>

<!--
The challenge was hosted on *AIcrowd* in 2018, and since then there have been more than 1000 submission from many different teams.

The challenge consists in taking a dataset of 1 Million playlists, with 63 million tracks, of which 2 million unique ones and more than 300K artists, and build a recommender system.
-->

---

# Reduced Dataset

Sampled 10% of the playlists
<v-clicks>

-   100K Playlists
-   681,805 Unique Songs
-   110,063 Artists

</v-clicks>

<v-clicks>

-   In average:
    -   66 songs per playlist
    -   38 unique artists per playlist

From here, build a distributed recommender system that given a playlist, it recommends new relevant songs that continuate it.

</v-clicks>

<!--
Since I couldn't work with the full dataset because of hardware limitations, I sampled the 10% of it and worked with 100K playlists. The number of unique songs became around 680K with more than 100K artists.

The aim of the project was to build different recommender systems using `pyspark`, and trying to keep the data as distributed as possibile, and see how the performances kept up with the most advances methods used by the winners of the challenge.
-->

---
css: windicss
transition: slide-up
---

# Data Visualization

<div class="flex justify-center">
    <img class="w-full" src="plots/dark/top_10_songs.png"/>
</div>

<!--
Before diving into the models, we can visualize the data a little bit. Here we can see the top most common songs, from this we can immediately say that hip-hop seems to be the most frequent genre.
-->

---
transition: slide-up
layout: center
---

Songs Frequency (Logarithmic scale)

<img class="w-full" src="plots/dark/all_songs_frequency_log.png"/>

<!--
If we analyze how many times a song appear In a playlist, we notice that most of the songs are unpopular, meaning that 662K songs out of 680K (more than 97%) appear in less than 100 playlists.
-->

---
transition: slide-up
layout: center
---

Frequency of songs that appear in less that 100 playlists (Logarithmic Scale)

<div class="flex justify-center">
<img class="w-full" src="plots/dark/major_songs_frequency_log.png"/>
</div>

In average each song appears in only 10 playlists!

<!--
We can zoom on the frequency of the songs that appear in less than 100 playlist, and we'll notice that actually most of the songs appear just in a few playlists. This would surely be a problem for simple recommendation algorithms, since those songs won't probably never be recommended.
-->

---
transition: slide-up
layout: center
---

Most popular artists

<div class="flex justify-center">
<img class="h-90" src="plots/dark/most_popular_artists.png"/>
</div>

<!--
We can also plot a pie chart describing the most popular artist, and we can again see how much is hip hop popular.
-->

---
layout: center
---

Top 15 most used words inside playlist titles

<div class="flex justify-center">
<img class="h-90" src="plots/dark/top_15_words.png"/>
</div>

<!--
From the histogram that describes the distribution of words used in the playlist titles, we can see that there are a lot of country playlists.
-->

---

# Developed Systems

<v-clicks>
  
- User-Based Collaborative Filtering;
- Item-Based Collaborative Filtering;
- Neural Network Approach: 
	- Implemented by using a Denoising Autoencoder developed by the 2nd place solution of the challenge.
  
</v-clicks>

<!--
Let's now see which one are the developed systems.

- I decided to start with a User-Based Collaborative Filtering system, where playlists are considered as users to which recommend new songs.

- Then I tried with an Item-Based collaborative filtering, where songs are items.

- Finally, I implemented a solution from one of the top solutions of the 2nd place team of the challenge, which uses a Denoising Autoencoder to solve the recommendation problem.
-->

---

# How was the data structured

<style>
.slidev-code-wrapper::-webkit-scrollbar{
    display: none !important;
  }
</style>

1,000 json files

<v-click>

```json {0-6|7-17|18-28|29-38|39-49}{maxHeight:'450px'}
{
    "info": {
        "generated_on": "2017-12-03 08:41:42.057563",
        "slice": "0-999",
        "version": "v1"
    },
    "playlist": {
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
            },
            {
                "pos": 1,
                "artist_name": "Degiheugi",
                "track_uri": "spotify:track:23EOmJivOZ88WJPUbIPjh6",
                "artist_uri": "spotify:artist:3V2paBXEoZIAhfZRJmo2jL",
                "track_name": "Betty",
                "album_uri": "spotify:album:3lUSlvjUoHNA8IkNTqURqd",
                "duration_ms": 235534,
                "album_name": "Endless Smile"
            },
            {
                "pos": 2,
                "artist_name": "Degiheugi",
                "track_uri": "spotify:track:1vaffTCJxkyqeJY7zF9a55",
                "artist_uri": "spotify:artist:3V2paBXEoZIAhfZRJmo2jL",
                "track_name": "Some Beat in My Head",
                "album_uri": "spotify:album:2KrRMJ9z7Xjoz1Az4O6UML",
                "duration_ms": 268050,
                "album_name": "Dancing Chords and Fireflies"
            }
        ]
    }
}
```

</v-click>

<!--
When downloaded, the data was split into 1000 different json files, and each file was structured like this.

The first part is an info header, which was removes since it was useless. Then we have a list of playlists, and we can see some information like the pid, the name, and other stuff. Then for each playlist we have a list of tracks, containing some more information like the track and artist name and uri. 

Thanks to pyspark I could load all the 1000 jsons into a single dataframe, and then randomly sample the 10% of it.
-->

---
transition: slide-up
---

# User-Based Collaborative Filtering - Data Preparation

How the playlists are encoded

<v-clicks>

1. Map each song in the playlist to a position.

| track_uri | pos |
| --------- | --- |
| track_1   | 0   |
| track_10  | 1   |
| track_11  | 2   |

</v-clicks>

<!--
The first method that I implemented is the user based collaborative filtering, and it works in this way.

First I map each song in the entire dataset to a position. This will be useful in order to encode the playlist into a vector.
-->

---

2. Create the encoding vector:

<v-clicks>

-   $1$ in the $i$-th position, if the song at position $i$ is in the playlist;
-   $0$ otherwise.

$$
p = [0,0,0,0,0,1,0,1,0,1]
$$

This means that the playlist $p$ has the songs with positions $[5, 7, 9]$

Average of 66 songs in a playlist, the vectors are 681,805 dimensional and so they are very sparse ($99.9903\%$ sparseness).

Memory efficiency via pyspark's `SparseVector`, which stores only the indices and the values.

</v-clicks>

<!--
The encoding in fact is created putting a 1 in the i-th position if the song mapped at position i is in the playlist, and a 0 otherwise. 

So if we have a playlist vector like this, this means that the playlist has the songs with positions 5,7 and 9.

Since there are an average of 66 songs in a playlist, the highly dimensional vector is very sparse, with a sparseness factor of 99,9903 percent. This is good for memory efficiency because we can represent it with a SparseVector object, but could be bad for the model performances.
-->

---
transition: slide-up
---

## Generate the Recommendations

The pipeline for the recommendation, given the `SparseVector` of a playlist that has to be continuated, is the following:

<v-clicks>

1. Compare the playlist with each other playlist, computing the pair-wise similarity using te Jaccard Similarity between their vectors. This will output the similarity value $\in [0,1]$

| track_uri | vector         | input_vector     | similarity |
| --------- | -------------- | ---------------- | ---------- |
| track_1   | indices=1,3,4  | indices=0,2,4,10 | 0.2        |
| track_10  | indices=4,6,10 | indices=0,2,4,10 | 0.5        |
| track_11  | indices=3,5    | indices=0,2,4,10 | 0.0        |

</v-clicks>

<v-click>

2. Take the top-$k$ vectors with the highest similarity value;

</v-click>

<v-click>

3. Aggregate the $k$ vectors, averaging them by their similarity value.

</v-click>

<!--
Once we have the SparseVector of the playlist that we want to continuate, the pipeline for generating the recommendation is the following:

First I compare the input playlist with each other playlist, computing the pairwise similarity using the Jaccard Similarity between the vectors. This will output a similarity value in 0,1. I use Jaccard Similarity because I don't need the information about the values, but just at which indexes the values are. 

This operation will produce a dataframe like this.

I then take the top-k vectors with the highest similarity value, where k is an hyperparameters, and aggregate the k vectors in order to have a single final vector. The aggregation works by averaging the vector weighting them by the relative similarity value, and then normalizing the value dividing them by the sum of similarity values.

-->

---

4. Normalize the values dividing by the sum of the $k$ similarity values.

<v-clicks>

$$
   p_1 = [0,1,1,0,0,1,0] \quad s_1 = 0.3 \\
   p_2 = [0,0,1,0,1,0,0] \quad s_2 = 0.5 \\
   p_3 = [1,0,1,0,1,0,0] \quad s_3 = 0.45 \\
$$

$$
p_{\text{agg}} = [0.45, 0.3, 1.25, 0, 0.95, 0.3, 0] \quad s_\text{sum} = 1.25\\
$$

$$
p_{\text{normalized}} = [\color{green}0.36, \color{white}0.24, \color{green}1.0, \color{white}0.0, \color{green}0.76, \color{white}0.24, 0.0]
$$

</v-clicks>

<v-click>

5. From the normalized aggregated vector, remove the songs that already appears in the input playlist;

</v-click>

<v-click>

6. The top-$n$ indices with the highest values will be the recommended songs;

$$n = 3 \quad \text{recommendations} = \{2: \color{green}1.0, \color{white}4: \color{green}0.76, \color{white}0: \color{green}0.36\}$$

</v-click>

<v-click>

7. Take the `song_uri` of the songs that are mapped into those indices to get the details.

The entire process takes about 30 seconds.
</v-click>

<!--
Let 's say that, for k = 3, we have these three playlist vectors, with their relative similarity value. The aggregation will produce this result, and the normalization this final vector. 
From this normalized aggregated vector, I remove the songs that already appear in the input playlist, and then I take the top-n indices with the highest values as the recommended songs. 

So, if n = 3, we will have this final recommendation result. Of course then I can take the track_uri that corresponds to the positions in order to have all the songs details. This entire process takes about 30 seconds.
-->

---
transition: slide-up
---

# Item-Based Collaborative Filtering - Data Preparation

Differently from User-Based CF, here the tracks are encoded instead of playlists.

Same principle:

1. Map each playlist into a position.

| pid   | pos |
| ----- | --- |
| pid_1 | 0   |
| pid_2 | 1   |
| pid_3 | 2   |

<!--
The item-based collaborative filtering is the opposite approach to user-based, in which the similarity is made between songs, and not between playlists.

The first steps are very similar, so I first have to map each playlist into a position
-->

---

2. Create the encoding vector for each track:

<v-clicks>

-   $1$ in the $i$-th position, if the playlist at position $i$ contains the song;
-   $0$ otherwise.

$$
s = [0,0,0,0,0,1,0,1,0,1]
$$

The song $s$ appears in the playlists $5, 7, 9$.

The vector is still very sparse, but its dimensionality is 110,063 instead of 681,805.

Since a song appears in an average of $10$ playlists, we have a degree of sparseness of $99.9909\%$ (w.r.t. $99.9903\%$ of the user-based cf).

</v-clicks>

<!--
Then I create the encoding vector for a tracks (and not a playlist as before), where there is a 1 in position 1 if the song appears in the playlist with position i mapped, and 0 otherwise. So if a song has this vector, it means that it appears in playlists 5, 7 and 9.

Since a song appears in an average in 10 playlists, we have a degree of sparseness that is a little bit higher than the one for the user-based cf.
-->

---
transition: slide-up
---

## Generate the Recommendations

Given a playlist to continuate, represented as a `DataFrame` containing its songs vectors, the recommendation pipeline is the following:

<v-click>

1. Compute the $k$-nearest-neighbours for each track in the playlist. This will result in a collection of $T$ dataframes, where $|T|$ is the number of songs in the playlist. A dataframe relevant to the track $t$ has a list of $k$ songs, each one with the distance from $t$ in a separated column;

</v-click>

<v-click>

2. Aggregate each Dataframe $\in T$ in order to have a single dataframe.
   Since we are sure that the size of $T$ is not big, I first convert the dataframes into python dictionaries

```python
{
    track_uri: distance
}
```

</v-click>

<!-- Let's see how do we generate a list of recommendation.

First we need the playlist to continuate, that in this case will be represented as a DataFrame containing the vectors of the songs it contains. Then the recommendation pipeline is the following:

- I first compute the k-nearest-neighbours for each track in the playlist. This will result in a collection of T dataframe, where the cardinality of T is the number of songs in the playlist. Each dataframe t in T has the k-neighbours of a singular track, and each neighbour has a distance from that track.
- I then aggreagate each dataframe in T in order to obtain a single dataframe. Now, since we are sure that the size of T is not big, I first convert the dataframes into python dictionaries with this structure. So we have a mapping between the track_uri and its distance from the relative track.
-->
---
transition: slide-up
---

The aggregation produce a python dictionary like this:

```json
{
    "track_uri_1": [0.2],
    "track_uri_2": [0.25, 0.45],
    "track_uri_3": [0.31, 0.4, 0.36],
    "track_uri_4": [0.1]
}
```

3. Convert the dictionary into a pyspark `DataFrame`, averaging the values inside of each list

| track_uri   | distance |
| ----------- | -------- |
| track_uri_1 | 0.2      |
| track_uri_2 | 0.35     |
| track_uri_3 | 0.356    |
| track_uri_4 | 0.1      |

<!-- 

- The aggreagation works in the following way: for each track_uri in all the dataframes in T, i put it as key of the dictionary, and I insert as values a list of all the distances that are mapped with that track. 

- Then I convert back the dictionary into a pyspark dataframe, averaging the values inside of each list.

- As before, i have to remove from this dataframe the songs that already are in the playlist, then I order the dataframe by ascending distances, and take the top-n tracks as recommendations.

This entire process takes about 30 to 60 seconds.
 -->

---

4. Remove from the `DataFrame` the songs that already are in the playlist

<v-clicks>

5. Order the `DataFrame` by ascending distances, and take the top-$n$ tracks as recommendations.

if $n = 3$, recommendations:

| track_uri   | distance |
| ----------- | -------- |
| track_uri_4 | 0.1      |
| track_uri_1 | 0.2      |
| track_uri_2 | 0.35     |

The entire process takes about 30 to 60 seconds.

</v-clicks>

<!--
Before performing the recommendation, we remove from the dataset the songs that already appear inside of the input playlist, in order to not recommend them.

We recommend the $n$ tracks by ordering the dataframe in ascending order by distance, and taking the top-$n$ tracks with the lowest distance.
-->

---

## K-Neighbours with LSH

<v-clicks>

-   Precise $k$-neighbours search is too expensive
-   _Locally Sensitive Hashing_ with pyspark's `MinHashLSH` class.
-   Number of hash tables $= 20$
    -   Higher: more precise, less fast
    -   Lower: less precise, faster

We can pre-compute the entire set of $k$-nearest neighbour to be even faster.

This takes a long time, but has to be done just once.
</v-clicks>

<!--
When computing the k-neighbours search for each song in the playlist, this could be very expensive, the more songs are in the playlist. 

For this I decided to not compute the exact neighbour search, but to use an approximation algoritmh using the Locally Sensitive Hasing with pyspark MinHashLSH class, which uses Jaccard Distance under the hood.

I had to set an hyperparamters that controls the number of hash tables to use. The higher the number, the more precise the algorithm, but the less fast; the lower, the less precise but the faster. I tried with both 10 and 20 hash tables.

In order to be very-fast at inference time, we can pre-compute the entire set of k-nearest neigbhours.
-->

---
css: windicss
transition: slide-up
---

# Neural Network Approach - Introduction

Solution taken by the "Hello World" team, which classified in 2nd place in the challenge.

<v-clicks>

-   Denoising Autoencoder that takes Tracks and Artits
-   Character level CNN that takes playlist's Title.
-   Ensable to make a prediction.

For simplicity, I consider just the Denoising Autoencoder model.

</v-clicks>

<!--
Regarding the final approach, I decided to take the solution written by the 2nd place team in the challenge. They implemented a recommender system that includes a denoising autoencoder that takes in input the tracks and the artists of a playlist, then a character level cnn that takes the playlist's title in input, and the overall model is just an ensamble of the twos.

For simplicity, I just considered the Denoising autoencoder model. 
-->

---
transition: slide-up
---

## The Autoencoder

<div class="flex justify-center">
    <img src="/images/autoencoder.png">
</div>

<v-clicks>

Input: Concatenation between songs and artists in the playlist, encoded in the following way:

-   **Songs encoding**: the same as User-Based CF;
-   **Artists encoding**: $1$ if artist in playlist, $0$ otherwise.

It reconstruct the input playlist. The intuition is that songs with high values in the reconstructed vectors are relevant for the input playlist.

</v-clicks>

<!--
The autoencoder works in the following way. It takes in input the concatenation between the songs and artists vector. The songs vector is encoded in the same way as the user-based cf, the artists vector follows the same principle, so a 1 if the artist i is in the playlist, 0 otherwise.

The model learns to reconstruct the input playlist, and the intuition is that songs with high values in the reconstructed vectors are relevant for the input playlist.
-->

---

## Noise Generation

Noise to let the model generalize.

<v-clicks>

Training with Hide & Seek technique:

$\text{input} = [\underbrace{0,0,1,0,1,1,}_\text{songs}\underbrace{0,1,0}_\text{artists}]$

Each iteration the song vector or the artist vector are masked.

</v-clicks>

<v-click>

Mask playlist: $\text{input}  [\underbrace{\color{red}0,0,0,0,0,0}_\text{songs}\underbrace{,\color{green}0,1,0}_\text{artists}]$

</v-click>

<v-click>

Mask artists: $\text{input} = [\underbrace{\color{green}0,0,1,0,1,1}_\text{songs}\underbrace{,\color{red}0,0,0}_\text{artists}]$

</v-click>

<v-clicks>

The model can learn inter-relationship between artists and tracks.

Dropout with probability $p$ that a node is kept in the network sampled between $(0.5, 0.8)$ as regularization, and to let the model learn intra-relationship between tracks and between artists.

</v-clicks>

<!--
In order to let the model generalize and not reconstruct exactly the same input, we add some noise to the input vector.
To generate this noise, at training time a technique called Hide & Seek is used, in which at each iteration and at random, one of the two vectors in the concatenation is maskes, meaning all its values are put to zero. 

So let's say this is the input, each time we can mask the songs, or mask the artists. In this way the model has to learn inter-relationship between artists and tracks to reconstruct the vector.

Another regularization technique is dropout, with a probability p of a node staying in the network sampled between the interval 0.5, 0.8. This allows the model to learn intra-relationship between tracks and between artists.
-->


---
transition: slide-up
---

## Training

_Petastorm_ to generate DataLoader from pyspark `DataFrame`.

<v-clicks>

At training time, the model is fed with mini-batches of $100$ playlists.

The loss function is the Binary Cross Entropy loss:

$$
\mathcal{L}(\mathbf{p}, \hat{\mathbf{p}})=-\frac{1}{n} \sum_{\mathbf{p} \in \mathbf{P}} p_i \log \hat{p}_i+\alpha\left(1-p_i\right) \log \left(1-\hat{p}_i\right)
$$

where $p_i$ is the input concatenated vector, and $\hat{p}_i$ is the reconstructed vector.

$\alpha = 0.5$ is the hyperparameter weighting factor. Balances the importance between observed values ($1$s) and missing values $0$s in the vector.

Same hyperparameters used by the authors of the paper, but smaller learning rate, since I have a smaller dataset to work with.

The whole training (pretrain + train) took about 12 hours on CUDA GPUs.

</v-clicks>


<!--

Regarding the training part, I used Petastorm, which is an open source libary made at Uber that allows to generate a Pytorch or Tensorflow dataloader form a pyspark dataframe, maintaining the data distributed. The model is then fed with mini-batches of data taken from the data loader.

Regarding the loss, the authors of the paper use Binary Cross Entropy with a weighting scheme different from observed values (ones in the vector) and missing values (zeros in the vector).

$\alpha$ is the weighting factor, and it's put to 0.5, in order to weight missing values less.

At inference time, the whole concatenation of songs and artists it's predicted, but only the song part it's considered. The recommendation is made out of the top-n songs with the highest values, that are not already present in the original playlist.

I left the same hyperparameters used by the authors of the paper, but adjusted the learning rate to be 10x smaller, since I have a smaller dataset to work with.
-->
---

## Validation

In order to do _Early Stopping_, and save the model parameters that achieve the best metrics, at the end epoch the model is evaluated on a validation set.

<v-click>

This is done for both the pretraining (tied weights) and training.

</v-click>

---
transition-slide-up
---

# Performance Evaluation

How is the test set built

<v-clicks>

-   Different splits for models with and without training
-   If there is no training, split at track level
-   It there is training, split at row level, and then at track level

</v-clicks>

<!--

Regarding the train-test split, I had to use two different strategies depending on the models.

If the model doesn't need a training part, then the dataset is split at track level, otherwise it's split at row level. Let's see what this mean.
-->

---
css: windicss
---
## User-based and Item-based CF

<v-clicks>

Split at track level (75%, 25%)

Original `DataFrame`

| pid | vector                  |
| --- | ----------------------- |
| 0   | indices=1,3,4,10,11,23  |
| 1   | indices=4,6,10,12,34,56 |
| 2   | indices=3,5,6,8,9,10    |

<div class="flex py-10">
  <div class="flex-1">

    Training set (75% of the tracks)

    | pid | vector             |
    |-----|--------------------|
    | 0   | indices=1,3,10,23  |
    | 1   | indices=4,10,56    |
    | 2   | indices=3,6,8, 10  |
    |-----|--------------------|

  </div>
  <div class="flex-1">

    Test set (25% of the tracks)

    | pid | vector          |
    |-----|-----------------|
    | 0   | indices=4,11    |
    | 1   | indices=6,12,34 |
    | 2   | indices=5,9     |
    |-----|-----------------|

  </div>
</div>

</v-clicks>


<!-- 

Regarding the models without the training, the train-test split happens at the tracks level. 

Meaning that we divide the original dataframe in two dataframes, each one with the same playlists, but with different songs. 25% of the songs are sampled and put into the playlist in the test-set, while the remaining 75% of the songs are put in the train-set.

In this way we can use the playlists in the train-set to generate the list of recommendations, while the songs in the test-set will be the ground truth. 

-->

---
transition: slide-up
---
## Neural Network Based

Create 3 `DataFrames`: Train, Validation, Test

Original `DataFrame`

| pid | vector                      |
| --- | --------------------------- |
| 0   | indices=1,3,4,10,11,23      |
| 1   | indices=4,6,10,12,34,56     |
| 2   | indices=3,5,6,8,9,10        |
| 3   | indices=1,2,5,8,10,11       |
| 4   | indices=0,1,5,8,11,21,34,53 |

---

<v-clicks>

<div class="flex py-10">
  <div class="flex-1">

    Training Set

    (98.5K playlists)

    | pid | vector                      |
    |-----|-----------------------------|
    | 0   | indices=1,3,4,10,11,23      |
    | 1   | indices=4,6,10,12,34,56     |
    | 2   | indices=3,5,6,8,9,10        |
    |-----|-----------------------------|

  </div>
  <div class="flex-1">

    Validation Set

    (500 playlists)

    | pid | vector                      |
    |-----|-----------------------------|
    | 3   | indices=1,2,5,8,10,11       |
    |-----|-----------------------------|

  </div>

</div>

<div class="flex justify-center">

<div>

    Test Set

    (1,000 playlists)

    | pid | vector                      |
    |-----|-----------------------------|
    | 4   | indices=0,1,5,8,11,21,34,53 |
    |-----|-----------------------------|

  </div>

</div>

Then I split at track level the Evaluation and Test set, in order to compute evaluation metrics

No need to further split the Training set.

</v-clicks>

<!--

For what concerns the model with training, we need three different dataframes, for Training, Validation and Testing, without common playlist among them.

So let's say this is the original dataframe, the split now happens at row level, which will produce three different dataframes.

Then, since I have to compute evaluation metrics on the validation and test set, I also have to split them but at track level. 

-->

---

# Evaluation Metrics

Evaluation metrics used for Performance Evaluation
<v-click>

$G$ is the ground truth (tracks in Test set) and $R$ is the set of recommended tracks

</v-click>

<v-click>

- R-precision: ratio between correct and incorrect recommended songs

    $$
    \text{Rprec} = \frac{G \cap R_{1:|G|}}{|G|}
    $$

</v-click>

<v-click>

- Normalized Discounted Cumulative Gain: how much the correct recommended songs are up in the list. We define $rel_i = 1$ if the track with index $i$ is in the ground truth, otherwise $rel_i = 0$.
    $$
    NDCG = \frac{DCG}{IDCG} \\
    $$
    $$
    DCG=rel_1+\sum_{i=2}^{|R|} \frac{r e l_i}{\log _2 i} \quad \text{and} \quad IDCG=1+\sum_{i=2}^{|G \cap R|} \frac{1}{\log _2 i}
    $$

</v-click>

<!-- The models are evaluated with two different metrics.

Let $G$ be the unordered list of left out tracks, and let $R$ be the list of recommended tracks, ordered by confidence.

The metrics of evaluation are two:

1. R-Precision: it measures the number of relevant tracks that are actually recommended by computing the ratio of how many recommended tracks are equal to the missing tracks, divided by the total number of missing tracks.
2. Normalized Discounted Cumulative Gain: it measures how down much up in the list are the tracks that are relevant and recommended. The value is higher, the more relevant recommended tracks are in the first positions.
-->

---

# Performance Comparison

Evaluation on 1,000 playlists

<v-click>

-   User-Based CF
    -   $Rprec = 0.1023$, $NDCG = 0.256$

</v-click>

<v-click>

-   Item-Based CF:
    -   10 Hash Tables: $Rprec = 0.0847$, $NDCG = 0.242$
    -   20 Hash Tables: $Rprec = 0.0897$, $NDCG = 0.261$

</v-click>

<v-click>

-   Denoising Autoencoder:
    -   $Rprec = 0.1327$, $NDCG = 0.334$

</v-click>

<v-click>

Winners of the challenge:

-   $Rprec = 0.220$, $NDCG = 0.3858$

</v-click>


<!-- 

Finally we can see the performances of each model. We can see that the User-Based CF performed well, considering the simplicity of the model.

The item-based, on the other hand, had worse performances. We can also see how with more hash tables the performances are a little bit higher.

And as expected the Neural Network based model is the one that has the best performances.

The models used by the winners of the challenge has a R-Precision of 0.22 and a NDCG of 0.38. Considering the fact that they are complex models and  1 million playlists, I'm very satisfied on how the models used in this project performed with just a tenth of the data.

I also built a little web app that demonstrates the use of the application by a final user.
-->

---
css: windicss
---
# Web Application Demo

<div class="flex justify-center">
    <video width="800" height="400" controls autoplay>
        <source src='/videos/demo.mp4' type="video/mp4">
    </video>
</div>

---
css: windicss
---

<div class="flex flex-col justify-between items-center h-full w-full">
<div class="flex justify-center items-center flex-1">
<h1>
Thank you for the attention
</h1>
</div>

<div class="flex flex-col justify-start items-start w-full">

<h4>
References
</h4>

<ul>
<li>
<a href="https://www.aicrowd.com/challenges/spotify-million-playlist-dataset-challenge">AIcrowd Spotify Million Playlist Challenge.</a>
</li>
<li>
<a href="url">hello world! [Yang et al.]</a>
</li>
</ul>

</div>

</div>
