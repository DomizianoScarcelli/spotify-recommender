import { SongType } from "../shared/types"
import { BASE_URL } from "../shared/urls"
import axios from "axios"

export const getAllSongs = async (): Promise<SongType[]> => {
	const URL = `${BASE_URL}/all-songs`
	const songs: SongType[] = (await axios.get(URL)).data
	return songs
}
