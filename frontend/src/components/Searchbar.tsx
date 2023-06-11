import React, { useRef } from "react"
import { SearchIcon } from "../shared/icons"
import { searchSongs } from "../utils/apiCalls"
import { SongType } from "../shared/types"

type Props = {
	songSetter: any
	onClear: () => void
}

const Searchbar = ({ songSetter, onClear }: Props) => {
	const inputRef = useRef<HTMLInputElement>(null)
	let debounceTimeout: any = null

	const handleSearchSongs = async () => {
		if (debounceTimeout) {
			clearTimeout(debounceTimeout)
		}

		const query = inputRef.current?.value

		if (!query) {
			onClear()
			return
		}

		debounceTimeout = setTimeout(async () => {
			const songs: SongType[] = []
			const result = await searchSongs(query)

			for (const item of result) {
				const { name, artist, album, duration, similarity } = item
				const { matchingPositions } = similarity

				const song = {
					name,
					artist,
					album,
					duration,
					matchingPositions: [...new Set(matchingPositions)],
				}

				songs.push(song)
			}

			songSetter(songs)
		}, 300) // Debounce delay of 300 milliseconds
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
