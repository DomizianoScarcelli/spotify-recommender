import { PaginatedSongs, RecommendationResponse, SearchResult, SongType } from "../shared/types"
import { BASE_URL } from "../shared/urls"
import axios from "axios"
import { convertMillisecondsToMinutesAndSeconds } from "./timeUtils"

export const getAllSongs = async (): Promise<SongType[]> => {
	const URL = `${BASE_URL}/all-songs`
	const paginatedSongs: PaginatedSongs = (await axios.get(URL)).data
	return paginatedSongs.songs.map((song) => {
		return { ...song, duration: convertMillisecondsToMinutesAndSeconds(parseInt(song.duration)) }
	})
}

export const searchSongs = async (query: string): Promise<SearchResult[]> => {
	const URL = `${BASE_URL}/search-song?query=${query}`
	const songs: SearchResult[] = (await axios.get(URL)).data
	return songs.map((song) => {
		return { ...song, duration: convertMillisecondsToMinutesAndSeconds(parseInt(song.duration)) }
	})
}

export const continuatePlaylist = async (songs: SongType[]): Promise<RecommendationResponse[]> => {
	const URL = `${BASE_URL}/continuate-playlist`
	const parsedSongs = songs.map(({ song_uri, album_uri }) => {
		return {
			song_uri,
			album_uri,
		}
	})
	const response: RecommendationResponse[] = (await axios.post(URL, parsedSongs)).data
	return response
}

export const getSongsFromUri = async (songInfo: RecommendationResponse[]): Promise<SongType[]> => {
	const result: { song: SongType }[] = []
	const URL = `${BASE_URL}/get-song-by-uri`
	console.log("song info: ", songInfo)
	for (const { track_uri } of songInfo) {
		const song = (await axios.get(`${URL}?uri=${track_uri}`)).data
		result.push(song)
	}
	return result.map((item) => item.song)
}

export const getAlbumArt = async (albumUri: string): Promise<string> => {
	const URL = `${BASE_URL}/album-art?album_uri=${albumUri}`
	const b64Image = (await axios.get(URL)).data
	// return `data:image/png;base64${b64Image}`
	return b64Image
}
