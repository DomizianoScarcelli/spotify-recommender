export type SongType = {
	id: string
	name: string
	artist: string
	album: string
	duration: string
	song_uri: string
	album_uri: string
	song_artist_concat: string
	matchingPositions?: number[]
}

export type PaginatedSongs = {
	songs: SongType[]
	next_page: number
}

export type SearchResult = {
	id: string
	name: string
	artist: string
	album: string
	duration: string
	song_uri: string
	album_uri: string
	song_artist_concat: string
	matchingPositions?: number[]
	similarity: Similarity
}

type Similarity = {
	matchCount: number
	matchingPositions: number[]
}

export type RecommendationResponse = {
	track_uri: string
	similarity: number
}
