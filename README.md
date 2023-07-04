# Spotify Automatic Playlist Continuation

Final project for the Big Data Course A.Y. 2022/2023 at University of Rome la Sapienza.

The project consists in implementing 3 different techniques to solve the Spotify Million Dataset Playlist Challenge, hosted on [AICrowd](https://www.aicrowd.com/challenges/spotify-million-playlist-dataset-challenge).

The methods are implemented using Pyspark in order for the data to work on a distributed system.

There is also a re-implementation of the [MMCF: Multimodal Collaborative Filtering for Automatic Playlist Continuation](https://github.com/hojinYang/spotify_recSys_challenge_2018) by the "Hello World" team that classified in 2nd place in the challenge. The re-implementation consists in converting the Neural Network from Tensorflow v1 to PyTorch, and using [Petastorm](https://github.com/uber/petastorm) to create a PyTorch DataLoader from a pyspark DataFrame in order to keep the data distributed.

The fold structure is the folliwing:

-   `core`: contains the notebooks and other files that consistutes the core algorithms that implement the recommender systems;
-   `slides`: contains the source code for the [presentation] made using [Slidev](https://github.com/slidevjs/slidev).
-   `webapp`: contains the code for a demo app built with Vite + React + FastAPI that showcase the usage of the system;

## Demo of the webapp
