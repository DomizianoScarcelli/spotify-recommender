import React, { useEffect, useState } from "react"
import Searchbar from "./components/Searchbar"
import SongList from "./components/SongList"
import { SongType } from "./shared/types"
import { getAllSongs } from "./utils/apiCalls"

const App = () => {
	const [songs, setSongs] = useState<SongType[]>([])
	const [playlistSongs, setPlaylistSongs] = useState<SongType[]>([])
	const handleSongRetrieval = async () => {
		const result = await getAllSongs()
		const mapped = result.map((song) => {
			return { ...song, matchingCharacters: [] }
		})
		setSongs(mapped)
	}

	useEffect(() => {
		handleSongRetrieval()
	}, [])

	return (
		<div className="bg-spotifyBlack h-screen text-spotifyWhite">
			{/* Main container */}
			<h1 className="font-bold text-spotifyGreen px-6 pt-6 text-3xl">Spotify Playlist Continuation</h1>
			{/* Main screen two cols */}
			<div className="flex h-[calc(100%-3.75rem)] p-5 gap-5">
				<div className="bg-spotifyDarkGray rounded-xl min-w-[280px] w-full max-w-[450px] py-5 px-8 overflow-y-scroll">
					<Searchbar songSetter={setSongs} onClear={handleSongRetrieval} />
					<SongList header={false} small={true} songs={songs} playlistState={{ playlistSongs, setPlaylistSongs }} />
				</div>
				<div className="bg-spotifyDarkGray rounded-xl flex-1 min-w-[500px] py-5 px-8 overflow-y-scroll">
					<p className="text-spotifyLightGray text-2xl">Your Playlist</p>
					<SongList header={true} small={false} songs={playlistSongs} playlistState={{ playlistSongs, setPlaylistSongs }} />
					{/* Line that separates the generated songs */}
					<div className="flex mt-6 items-center justify-center">
						<div className="bg-spotifyGreen h-0.5 mr-8 w-full"></div>
						<div className="text-spotifyGreen text-2xl">Generated songs</div>
						<div className="bg-spotifyGreen h-0.5 ml-8 w-full"></div>
					</div>
				</div>
			</div>
		</div>
	)
}

export default App
