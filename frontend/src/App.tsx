import React, { useEffect, useState } from "react"
import Searchbar from "./components/Searchbar"
import SongList from "./components/SongList"
import { SongType } from "./shared/types"
import { getAllSongs } from "./utils/apiCalls"
import { SparklerIcon } from "./shared/icons"

const App = () => {
	const [songs, setSongs] = useState<SongType[]>([])
	const [playlistSongs, setPlaylistSongs] = useState<SongType[]>([])
	const [generated, setGenerated] = useState<boolean>(false)
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

	const playlistGeneration = () => {
		setGenerated(true)
		console.log(generated)
		return generated
	}

	return (
		<div className="bg-spotifyBlack h-screen text-spotifyWhite">
			{/* Main container */}
			<div className="flex items-center pt-6 px-6 justify-between">
				<h1 className="font-bold text-spotifyGreen text-3xl">Spotify Playlist Continuation</h1>
				<div className="bg-spotifyGreen text-spotifyBlack text-l p-3 rounded-xl cursor-pointer flex items-center justify-between" onClick={playlistGeneration}>
					<SparklerIcon className="fill-spotifyLightGray mr-2 w-5 h-5" />
					<p>CONTINUATE</p>
				</div>
			</div>
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
					{generated ? (
						<div className="flex mt-6 items-center justify-center">
							<div className="bg-spotifyGreen h-0.5 mr-8 w-full"></div>
							<div className="text-spotifyGreen text-2xl">Generated songs</div>
							<div className="bg-spotifyGreen h-0.5 ml-8 w-full"></div>
						</div>
					) : (
						<></>
					)}
				</div>
			</div>
		</div>
	)
}

export default App
