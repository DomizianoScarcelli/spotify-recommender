import React from "react"
import Searchbar from "./components/Searchbar"
import SongList from "./components/SongList"
import { SongType } from "./shared/types"
interface Song {
	id: number
	title: string
	artist: string
}

interface Props {
	songs: Song[]
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
		<div className="bg-black h-screen text-spotifyWhite w-screen">
			{/* Main container */}
			<div className="h-full p-6">
				<h1 className="font-bold text-spotifyGreen text-3xl">Spotify Playlist Continuation</h1>

				{/* Main screen two cols */}
				<div className="flex mt-5 gap-5">
					<div className="bg-spotifyDarkGray rounded-xl w-fit py-5 px-8">
						<Searchbar />
						<SongList header={false} small={true} songs={songs} />
					</div>
					<div className="bg-spotifyDarkGray rounded-xl flex-1 py-5 px-8 ">
						<p className="text-spotifyLightGray text-2xl">Your Playlist</p>
						<SongList header={true} small={false} songs={songs} />
					</div>
				</div>
			</div>
			<div className="flex"></div>
		</div>
	)
}

export default App
