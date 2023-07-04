import React, { useEffect, useState } from "react"
import Searchbar from "./components/Searchbar"
import SongList from "./components/SongList"
import { SongType } from "./shared/types"
import { continuatePlaylist, getAllSongs, getSongsFromUri } from "./utils/apiCalls"
import { SparklerIcon } from "./shared/icons"

const App = () => {
	const [songs, setSongs] = useState<SongType[]>([])
	const [playlistSongs, setPlaylistSongs] = useState<SongType[]>([])
	const [generated, setGenerated] = useState<boolean>(false)
	const [inProgress, setInProgress] = useState<boolean>(false)
	const [recommendedSongs, setRecommendedSongs] = useState<SongType[]>([])
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

	useEffect(() => {
		console.log("RECOMMENDATIONS DEBUG: ", recommendedSongs)
	}, [recommendedSongs])

	useEffect(() => {
		console.log("PLAYLIST SONGS DEBUG: ", playlistSongs)
	}, [playlistSongs])

	const playlistGeneration = async () => {
		setInProgress(true)
		const recommendationResponse = await continuatePlaylist(playlistSongs)
		const recommendations = await getSongsFromUri(recommendationResponse)
		setInProgress(false)
		setGenerated(true)
		setRecommendedSongs(recommendations)
	}

	return (
		<div className="bg-spotifyBlack h-screen text-spotifyWhite">
			{/* Main container */}
			<div className="flex px-6 pt-6 items-center justify-between">
				<h1 className="font-bold text-spotifyGreen text-3xl">Spotify Playlist Continuation</h1>
				<div className="bg-spotifyGreen rounded-xl cursor-pointer flex text-spotifyBlack text-l p-3 items-center justify-between" onClick={playlistGeneration}>
					<SparklerIcon className="h-5 fill-spotifyLightGray mr-2 w-5" />
					{generated ? inProgress ? <p>GENERATING...</p> : <p>AGAIN!</p> : inProgress ? <p>GENERATING...</p> : <p>CONTINUATE</p>}
				</div>
			</div>
			{/* Main screen two cols */}
			<div className="flex h-[calc(100%-3.75rem)] p-5 gap-5">
				<div className="bg-spotifyDarkGray rounded-xl min-w-[280px] w-full max-w-[450px] py-5 px-8 overflow-y-scroll">
					<Searchbar songSetter={setSongs} onClear={handleSongRetrieval} />
					<SongList header={false} small={true} songs={songs} playlistState={{ playlistSongs, setPlaylistSongs }} recommended={false} />
				</div>
				<div className="bg-spotifyDarkGray rounded-xl flex-1 min-w-[500px] py-5 px-8 overflow-y-scroll">
					<p className="text-spotifyLightGray text-2xl">Your Playlist</p>
					<SongList header={true} small={false} songs={playlistSongs} playlistState={{ playlistSongs, setPlaylistSongs }} recommended={false} />
					{/* Line that separates the generated songs */}
					{generated ? (
						<>
							<div className="flex mt-6 pb-5 items-center justify-center">
								<div className="bg-spotifyGreen h-0.5 mr-8 w-full"></div>
								<div className="text-spotifyGreen text-xl whitespace-nowrap">Recommended songs</div>
								<div className="bg-spotifyGreen h-0.5 ml-8 w-full"></div>
							</div>
							<SongList
								header={false}
								small={false}
								songs={recommendedSongs}
								playlistState={{ playlistSongs: recommendedSongs, setPlaylistSongs: setRecommendedSongs }}
								recommended={true}
							/>
						</>
					) : (
						<></>
					)}
				</div>
			</div>
		</div>
	)
}

export default App
