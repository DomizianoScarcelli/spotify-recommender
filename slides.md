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
            },
        ],

    }
}
```
</v-click>

---

# Data Visualization


---

# Developed Systems
<v-clicks>
  
- User-Based Collaborative Filtering;
- Item-Based Collaborative Filtering;
- Neural Network Approach: 
	- Implemented by using a Denoising Autoencoder developed by 	the 2nd place winners of the challenge.
  
</v-clicks>
---
transition: slide-up
---

# User-Based Collaborative Filtering - Data Preparation
How the playlists are encoded

1. Map each song in the playlist to a position.

| track_uri | pos |
|-----------|-----|
| track_1   | 0   |
| track_10  | 1   |
| track_11  | 2   |

---

2. Create the encoding vector:

<v-clicks>

- $1$ in the $i$-th position, if the song at position $i$ is in the playlist;
- $0$ otherwise.

$$
p = [0,0,0,0,0,1,0,1,0,1]
$$

This means that the playlit $p$ has the songs with positions $[5, 7, 9]$

Average of 66 songs in a playlist, the vectors 600K dimensional and so they are very sparse (x % spraseness).

Memory efficiency via pyspark's `SparseVector`, which stores only the indices and the values.

</v-clicks>
---
transition: slide-up
---

## Generate the Recommendations
The pipeline for the recommendation, given the `SparseVector` of a playlist that has to be continuated, is the following:

<v-clicks>

1. Compare the playlist with each other playlist, computing the pair-wise similarity using te Jaccard Similarity between their vectors. This will output the similarity value $\in [0,1]$

| track_uri | vector         | input_vector     | similarity |
|-----------|----------------|------------------|------------|
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

</v-click>


---
transition: slide-up
---

# Item-Based Collaborative Filtering - Data Preparation
Differently from User-Based CF, here the tracks are encoded instead of playlists.

Same principle:

1. Map each playlist into a position.

| pid | pos |
|-----------|-----|
| pid_1   | 0   |
| pid_2  | 1   |
| pid_3  | 2   |

---

2. Create the encoding vector for each track:

<v-clicks>

- $1$ in the $i$-th position, if the playlist at position $i$ contains the song;
- $0$ otherwise.

$$
s = [0,0,0,0,0,1,0,1,0,1]
$$

The song $s$ appears in the playlists $5, 7, 9$.

The vector is still very sparse, but its dimensions are 100K instead of 600K (x % spraseness).

</v-clicks>
---
transition: slide-up
---

## Generate the Recommendations

Given a playlist to continuate, represented as a `DataFrame` containing its songs vectors, the recommendation pipeline is the following:

<v-click>

1. Compute the $k$-nearest-neighbours for each track in the playlist. This will result in a collection of $T$ dataframes, where $|T|$ is the number of songs in the playlist. A dataframe relevant to the track $t$ has a list of $k$ songs, each one with the distance from $t$ in a `distCol` column;

</v-click>

<v-click>

2. Aggregate each Dataframe $\in T$ in order to have a single dataframe.
Since we are sure that the size of $T$ is not big, I first convert the dataframes into python dictionaries
```python
{
    pos: distance
}
```

</v-click>
---
transition: slide-up
---
    
    The aggregation produce a python dictionary like this:
    
```json
{
    34: [0.2], 
    24: [0.25, 0.45], 
    102: [0.31, 0.40, 0.36], 
    314: [0.1], 
}
```

3. Convert the dictionary into a pyspark `DataFrame`, averaging the values inside of each list

| pos   | confidence    |
|-------|---------------|
| 34| 0.8  |
| 24| 0.65     |
| 102| 0.644    |
| 314| 0.9    |



---

4. Remove from the `DataFrame` the songs that already are in the playlist

<v-clicks>

5. Order the `DataFrame` by ascending distances, and take the top-$n$ tracks as recommendations.

if $n = 3$, recommendations:

| pos   | confidence    |
|-------|---------------|
| 314| 0.9    |
| 34| 0.8  |
| 24| 0.65     |

</v-clicks>
---

## K-Neighbours with LSH

<v-clicks>

- Precise $k$-neighbours search is too expensive
- *Locally Sensitive Hashing* with pyspark's `MinHasLSH` class.
- Number of hash tables $= 10$
  - Higher: more precise, less fast
  - Lower: less precise, faster

We can pre-compute the entire set of $k$-nearest neighbour to be even faster

This takes a long time, but has to be done just once
</v-clicks>

---
css: windicss
transition: slide-up
---

# Neural Network Approach - Introduction
Solution taken by the "Hello World" team, which classified in 2nd place in the challenge.

<v-clicks>

- Denoising Autoencoder that takes Tracks and Artits
- Character level CNN that takes playlist's Title.
- Ensable to make a prediction.

For simplicity, I consider just the Denoising Autoencoder model.

</v-clicks>
---
transition: slide-up
---

## The Autoencoder
<div class="flex justify-center">
    <img src="/images/autoencoder.png">
</div>

<v-clicks>

Input: Concatenation between songs and artists in the playlist, encoded in the following way: 

- **Songs encoding**: the same as User-Based CF;
- **Artists encoding**: $1$ if artist in playlist, $0$ otherwise.

It reconstruct the input playlist. The intuition is that songs with high values in the reconstructed vectors are relevant for the input playlist.

</v-clicks>
---

## Noise Generation

Noise to let the model generalize.

<v-clicks>

Training with Hide & Seek technique:

$\text{input} = [\underbrace{0,0,1,0,1,1,}_\text{playlist}\underbrace{0,1,0}_\text{artists}]$

Each iteration the song vector or the artist vector are masked.

</v-clicks>

<v-click>

Mask playlist: $\text{input}  [\underbrace{\color{red}0,0,0,0,0,0}_\text{playlist}\underbrace{,\color{green}0,1,0}_\text{artists}]$

</v-click>

<v-click>

Mask artists: $\text{input} = [\underbrace{\color{green}0,0,1,0,1,1}_\text{playlist}\underbrace{,\color{red}0,0,0}_\text{artists}]$

</v-click>

<v-clicks>

The model can learn intra-relationship between artists and tracks.
  
Dropout with probability $p$ that a node is kept in the network sampled between $(0.5, 0.8)$  as regularization, and to let the model learn inter-relationship between tracks and between artists.

</v-clicks>


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

$\alpha = 0.5$ is the hyperparameter weighting factor. Balances the importance between observed values ($1$s) and missing values $0$s in the input vector.

Same hyperparameters used by the authors of the paper, but smaller learning rate, since I have a smaller dataset to work with.

</v-clicks>

---

## Validation
In order to do _Early Stopping_, and save the model parameters that achieve the best metrics, at the end epoch the model is evaluated on a validation set.

This is done for both the pretraining (tied weights) and training.

---
transition-slide-up
---

# Performance Evaluation
How is the test set built

<v-clicks>

- Different splits for models with and without training
- If there is no training, split at track level
- It there is training, split at row level, and then at track level

</v-clicks>

---
css: windicss
---

## User-based and Item-based CF

<v-clicks>

Split at track level (75%, 25%)

Original `DataFrame`

| pid | vector                  |
|-----|-------------------------|
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

---
transition: slide-up
---

## Neural Network Based

Create 3 `DataFrames`:  Train, Validation, Test

Original `DataFrame`

| pid | vector                      |
|-----|-----------------------------|
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

---

# Evaluation Metrics
Evaluation metrics used for Performance Evaluation
<v-clicks>

$G$ is the ground truth (tracks in Test set) and $R$ is the set of recommended tracks

- R-precision: ratio between correct and incorrect recommended songs
$$
\text{Rprec} = \frac{G \cap R_{1:|G|}}{|G|}
$$

- Normalized Discounted Gain: how much the correct recommended songs are up in the list
$$
NDCG = \frac{DCG}{IDCG} \\
$$
- where
$$
DCG=rel_1+\sum_{i=2}^{|R|} \frac{r e l_i}{\log _2 i} \quad \text{and} \quad IDC G=1+\sum_{i=2}^{|G \cap R|} \frac{1}{\log _2 i}
$$

</v-clicks>

---

# Performance Comparison

Evaluation on 1,000 playlists

<v-clicks>

- User-Based CF
  - $Rprec = 0.13$, $NDCG = 0.28$
- Item-Based CF:
  - $Rprec = 0.13$, $NDCG = 0.28$
- Denoising Autoencoder:
  - $Rprec = 0.13$, $NDCG = 0.28$

Winners of the challenge:
- $Rprec = 0.220$, $NDCG = 0.3858$
	
</v-clicks>

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


