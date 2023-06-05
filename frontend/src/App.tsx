import React from "react"
import Searchbar from "./components/Searchbar"
import Song from "./components/Song"
import SongList from "./components/SongList"
interface Song {
	id: number
	title: string
	artist: string
}

interface Props {
	songs: Song[]
}

const App = () => {
	const songs: Song[] = [
		{ id: 1, title: "Song 1", artist: "Artist 1" },
		{ id: 2, title: "Song 2", artist: "Artist 2" },
		{ id: 3, title: "Song 3", artist: "Artist 3" },
	]

	return (
		<div className="bg-black h-screen text-spotifyWhite w-screen">
			{/* Main container */}
			<div className="h-full p-6">
				<h1 className="font-bold text-spotifyGreen text-3xl">Spotify Playlist Continuation</h1>

				{/* Main screen two cols */}
				<div className="flex mt-5 gap-5">
					<div className="bg-spotifyDarkGray rounded-xl py-5 px-8 w-80">
						<Searchbar />
					</div>
					<div className="bg-spotifyDarkGray rounded-xl flex-1 py-5 px-8 ">
						<p className="text-spotifyLightGray text-2xl">Your Playlist</p>
						<SongList />
					</div>
				</div>
			</div>
			<div className="flex"></div>
		</div>
	)
}

export default App
