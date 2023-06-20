import { PaginatedSongs, SearchResult, SongType } from "../shared/types"
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
	console.log(URL, songs)
	return songs.map((song) => {
		return { ...song, duration: convertMillisecondsToMinutesAndSeconds(parseInt(song.duration)) }
	})
}

export const continuatePlaylist = async (songs: SongType[]): Promise<any> => {
	const URL = `${BASE_URL}/continuate-playlist`
	const parsedSongs = songs.map(({ song_uri, album_uri }) => {
		return {
			song_uri,
			album_uri,
		}
	})
	const response: any = await axios.post(URL, parsedSongs)
	return response
}
