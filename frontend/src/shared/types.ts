export type SongType = {
	name: string
	artist: string
	album: string
	duration: string
	matchingPositions?: number[]
}

export type SearchResult = {
	name: string
	artist: string
	album: string
	duration: string
	similarity: Similarity
}

type Similarity = {
	matchCount: number
	matchingPositions: number[]
}
