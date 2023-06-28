---
theme: default
transition: "slide-left"
css: windicss
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
        font-size: 14px !important; /* Adjust the font size as per your preference */
        width: 30% !important; /* Adjust the table width as per your preference */
    }
    .col-right {
        padding-top: 3rem;
    }
</style>

# <logos-spotify class="pr-120 w-2xl"/>

## Playlist continuation challenge

---

# Introduction
Recommender System for Playlist Continuation

- Started in 2018
- Hosted on AIcrowd
- More than 1000 submissions

<v-clicks>

## Dataset:
- 1 Million Playlists
- 63 Million total songs
- 2 Million unique songs
- 345K unique artists

</v-clicks>

<v-clicks>

Playlists created by users from 2010 to 2017

</v-clicks>
---


# Reduced Dataset

Sampled 10% of the playlists
<v-clicks>

-   100K Playlists
-   600K Unique Songs
-   100K Artists

From here, build a distributed recommender system that given a playlist, it recommend new relevant songs that continuate it.

</v-clicks>
---

# How was the data structured

<style>
.slidev-code-wrapper::-webkit-scrollbar{
    display: none !important;
  }
</style>

1,000 json files

<v-click>

```json {2-11|12-22|23-32|33-42}{maxHeight:'450px'}
{
"metadata": {"bla bla bla"},
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
            },
        ],

    }
}
```
</v-click>

---
layout: two-cols
css: windicss
---

# Data Visualization

<!-- <iframe src="/top-songs.html">
</iframe> -->

| pos   | confidence    |
|-------|---------------|
| 505626| 0.86660594    |
| 338046| 0.8451381     |
| 256245| 0.8245531     |
| 669595| 0.81081593    |
| 174330| 0.78816617    |
| 592258| 0.7713628     |
| 589100| 0.7507684     |
| 170221| 0.73229903    |
|  87563| 0.7185418     |
| 585110| 0.71125495    |

::right::

Test



---

# Developed Systems
<v-clicks>
  
- User-Based Collaborative Filtering;
- Item-Based Collaborative Filtering;
- Neural Network Approach: 
	- Implemented by using a Denoising Autoencoder developed by 	the 2nd place winners of the challenge.
  
</v-clicks>
---

# User-Based Collaborative Filtering - Data Preparation
How the playlists are encoded

1. Map each song in the playlist to a position.

2. Create the encoding vector:
- $1$ in the $i$-th position, if the song at position $i$ is in the playlist;
- $0$ otherwise.

$$
p = [0,0,0,0,0,1,0,1,0,1]
$$

Average of 66 songs in a playlist, the vectors 600K dimensional and so they are very sparse (x % spraseness).

Memory efficiency via pyspark's `SparseVector`, which stores only the indices and the values.

---
transition: slide-up
---

## Generate the Recommendations
The pipeline for the recommendation, given the `SparseVector` of a playlist that has to be continuated, is the following:

<v-clicks>

1. Compare the playlist with each other playlist, computing the pair-wise similarity using te Jaccard Similarity between their vectors. This will output the similarity value $\in [0,1]$
2. Take the top-$k$ vectors with the highest similarity value;
3. Aggregate the $k$ vectors, averaging them by their similarity value.
4. Normalize the values dividing by the sum of the $k$ similarity values.

$$
   p_1 = [0,1,1,0,0,1,0] \quad s_1 = 0.3 \\
   p_2 = [0,0,1,0,1,0,0] \quad s_2 = 0.5 \\
   p_3 = [1,0,1,0,1,0,0] \quad s_3 = 0.45 \\
$$

$$
p_{\text{agg}} = [0.45, 0.3, 1.25, 0, 0.95, 0.3, 0] \\

p_{\text{normalized}} = [0.36, 0.24, 1.0, 0.0, 0.76, 0.24, 0.0]
$$

</v-clicks>

---

$$
p_{\text{normalized}} = [0.36, 0.24, 1.0, 0.0, 0.76, 0.24, 0.0]
$$

4. From the normalized aggregated vector, remove the songs that already appears in the input playlist;
5. The top-$n$ indices with the highest values will be the recommended songs;
6. Take the `song_uri` of the songs that are mapped into those indices to get the details.

---

# Item-Based Collaborative Filtering - Data Preparation
Differently from User-Based CF, here the tracks are encoded instead of playlists.

Same principle:

1. Map each playlist into a position.

2. Create the encoding vector for each track:
- $1$ in the $i$-th position, if the playlist at position $i$ contains the song;
- $0$ otherwise.

$$
s = [0,0,0,0,0,1,0,1,0,1]
$$

The song $s$ appears in the playlists $5, 7, 9$.

The vector is still very sparse, but its dimensions are 100K instead of 600K (x % spraseness).

---
transition: slide-up
---

## Generate the Recommendations

Given a playlist to continuate, represented as a `DataFrame` containing its songs vectors, the recommendation pipeline is the following:

1. Compute the $k$-nearest-neighbours for each track in the playlist. This will result in a collection of $T$ dataframes, where $|T|$ is the number of songs in the playlist. A dataframe relevant to the track $t$ has a list of $k$ songs, each one with the distance from $t$ in a `distCol` column;
2. Aggregate each Dataframe $\in T$ in order to have a single dataframe.
Since we are sure that the size of $T$ is not big, I first convert the dataframes into python dictionaries
```python
{track_uri: distance}
```

---
transition: slide-up
---
    
    The aggregation produce this python dictionary:
    
```json
{'spotify:track:001BVhvaZTf2icV88rU3DA': [0.0, 0.0], 
'spotify:track:1iO2inxYIzmPnMuDFfU1Rl': [0.8571428571428572, 0.8571428571428572], 
'spotify:track:3Ff2kaO1uxXjd9HkHfMw4h': [0.8571428571428572, 0.8571428571428572], 
'spotify:track:2EhgEpfn3U0lmpryqDujwt': [0.8571428571428572, 0.8571428571428572], 
'spotify:track:3lkFKOOQRp1AqWk2PPAW6B': [0.8571428571428572, 0.8571428571428572]}
```

3. Convert the dictionary into a pyspark `DataFrame`, averaging the values inside of each list
<img src="/images/ibcf-aggregated.png">

---

4. Remove from the `DataFrame` the songs that already are in the playlist
5. Order the `DataFrame` by ascending distances, and take the top-$n$ tracks as recommendations.

---

## K-Neighbours?

---
css: windicss
transition: slide-up
---

# Neural Network Approach - Introduction
Solution taken by the "Hello World" team, which classified in 2nd place in the challenge.

- Denoising Autoencoder that takes Tracks and Artits
- Character level CNN that takes playlist's Title.
- Ensable to make a prediction.

For simplicity, I consider just the Denoising Autoencoder model.

---
transition: slide-up
---

## The Autoencoder
<div class="flex justify-center">
    <img src="/images/autoencoder.png">
</div>

Input: Concatenation between songs and artists in the playlist, encoded in the following way: 

- **Songs encoding**: the same as User-Based CF;
- **Artists encoding**: $1$ if artist in playlist, $0$ otherwise.

It reconstruct the input playlist. The intuition is that songs with high values in the reconstructed vectors are relevant for the input playlist.

---

## Noise Generation

Noise to let the model generalize.

Training with Hide & Seek technique:
- Each iteration the song vector or the artist vector are masked.
- The model can learn intra-relationship between artists and tracks.
  
Dropout with probability that a node is maintained $p \in \mathcal{N} \sim (0.5, 0.8)$ as regularization, and to let the model learn inter-relationship between tracks and between artists.

---
transition: slide-up
---

## Training

_Petastorm_ to generate DataLoader from pyspark `DataFrame`. 

At training time, the model is fed with mini-batches of $100$ playlists.

The loss function is the Binary Cross Entropy loss:
$$
\mathcal{L}(\mathbf{p}, \hat{\mathbf{p}})=-\frac{1}{n} \sum_{\mathbf{p} \in \mathbf{P}} p_i \log \hat{p}_i+\alpha\left(1-p_i\right) \log \left(1-\hat{p}_i\right)
$$

where $p_i$ is the input concatenated vector, and $\hat{p}_i$ is the reconstructed vector.

$\alpha = 0.5$ is the hyperparameter weighting factor. Balances the importance between observed values ($1$s) and missing values $0$s in the input vector.

Same hyperparameters used by the authors of the paper, but smaller learning rate, since I have a smaller dataset to work with.


---

## Validation
In order to do _Early Stopping_, and save the model parameters that achieve the best metrics, at the end epoch the model is evaluated on a validation set.

This is done for both the pretraining (tied weights) and training.
---

# Performance Evaluation
How is the test set built


---
css: windicss
---

# Web Application Demo

<div class="flex justify-center">
    <video width="800" height="400" controls autoplay>
        <source src='/videos/output.mp4' type="video/mp4">
    </video>
</div>

