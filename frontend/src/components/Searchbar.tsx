import React from "react"
import { SearchIcon } from "../shared/icons"

const Searchbar = () => {
	return (
		<div className="bg-spotifyGray flex rounded-3xl p-4 items-center">
			<SearchIcon className="fill-spotifyLightGray mr-2 w-5" />
			<input className="bg-transparent outline-none placeholder-spotifyLightGray flex-1 text-spotifyLightGray" placeholder="Search for a song" />
		</div>
	)
}

export default Searchbar
