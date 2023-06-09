import React, { useRef } from "react"
import { SearchIcon } from "../shared/icons"
import { searchSongs } from "../utils/apiCalls"
import { SongType } from "../shared/types"

type Props = {
	songSetter: any
}
const Searchbar = ({ songSetter }: Props) => {
	const inputRef = useRef<HTMLInputElement>(null)
	const handleSearchSongs = async () => {
		const songs: SongType[] = []
		if (inputRef.current == null) return
		if (inputRef.current.value == "") {
			// songSetter([])
			//TODO: Return to initial state
			return
		}
		const query = inputRef.current.value
		console.log("QUERY", query)
		if (!query) return []
		const result = await searchSongs(query)
		for (const item of result) {
			const { name, artist, album, duration, similarity } = item
			const { matchingPositions } = similarity
			console.log("matching positions for", name, [...new Set(matchingPositions)])
			const song = { name, artist, album, duration, matchingPositions: [...new Set(matchingPositions)] }
			songs.push(song)
		}
		songSetter(songs)
	}
	return (
		<div className="bg-spotifyGray flex rounded-3xl p-4 items-center">
			<SearchIcon className="fill-spotifyLightGray mr-2 w-5" />
			<input
				className="bg-transparent outline-none placeholder-spotifyLightGray flex-1 text-spotifyLightGray"
				placeholder="Search for a song"
				onInputCapture={handleSearchSongs}
				ref={inputRef}
			/>
		</div>
	)
}

export default Searchbar
