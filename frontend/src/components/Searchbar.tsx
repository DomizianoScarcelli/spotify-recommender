import React, { useRef } from "react"
import { SearchIcon } from "../shared/icons"
import { searchSongs } from "../utils/apiCalls"

type Props = {
	songSetter: any
}
const Searchbar = ({ songSetter }: Props) => {
	const inputRef = useRef(null)
	const handleSearchSongs = async () => {
		const query = inputRef.current
		if (!query) return []
		const result = await searchSongs(query)
		console.log(`Searched for ${JSON.stringify(result)}`)
		songSetter(result)
		return result
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
