import React from "react"
import Searchbar from "./components/Searchbar"
import SongList from "./components/SongList"
import { SongType } from "./shared/types"
interface Song {
	id: number
	title: string
	artist: string
}

const App = () => {
	const songs: SongType[] = [
		{ name: "Song 1", artist: "Artist 1", album: "marione", duration: "2:33" },
		{ name: "Song 1", artist: "Artist 1", album: "marione", duration: "2:33" },
		{ name: "Song 1", artist: "Artist 1", album: "marione", duration: "2:33" },
		{ name: "Song 1", artist: "Artist 1", album: "marione", duration: "2:33" },
		{ name: "Song 1", artist: "Artist 1", album: "marione", duration: "2:33" },
		{ name: "Song 1", artist: "Artist 1", album: "marione", duration: "2:33" },
		{ name: "Song 1", artist: "Artist 1", album: "marione", duration: "2:33" },
	]

	return (
		<div className="bg-spotifyBlack text-spotifyWhite h-screen">
			{/* Main container */}
			<h1 className="font-bold text-spotifyGreen text-3xl px-6 pt-6">Spotify Playlist Continuation</h1>
			{/* Main screen two cols */}
			<div className="flex gap-5 p-5 h-[calc(100%-3.75rem)]">
				<div className="bg-spotifyDarkGray rounded-xl min-w-[280px] max-w-fit w-full py-5 px-8 overflow-y-scroll">
					<Searchbar />
					<SongList header={false} small={true} songs={songs} />
				</div>
				<div className="bg-spotifyDarkGray rounded-xl flex-1 py-5 px-8 overflow-y-scroll min-w-[500px]">
					<p className="text-spotifyLightGray text-2xl">Your Playlist</p>
					<SongList header={true} small={false} songs={songs} />
				</div>
			</div>
		</div>
	)
}

export default App
