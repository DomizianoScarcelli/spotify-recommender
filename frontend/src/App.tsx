import React from "react"

interface Song {
	id: number
	title: string
	artist: string
}

interface Props {
	songs: Song[]
}

const Sidebar = ({ songs }: Props) => {
	return (
		<div className="bg-spotifyBlack text-spotifyWhite p-4">
			<input type="text" placeholder="Search songs..." className="rounded-md text-spotifyBlack mb-4 w-full p-2" />
			<ul>
				{songs.map((song) => (
					<li key={song.id} className="mb-2">
						{song.title} - {song.artist}
					</li>
				))}
			</ul>
		</div>
	)
}

const MainScreen = () => {
	const songs: Song[] = [
		{ id: 1, title: "Song 1", artist: "Artist 1" },
		{ id: 2, title: "Song 2", artist: "Artist 2" },
		{ id: 3, title: "Song 3", artist: "Artist 3" },
	]
	return (
		<div className="bg-spotifyBlack h-screen w-screen p-4">
			<h2 className="font-bold mb-4 text-2xl">Recommendations</h2>
			<RecommendationList recommendations={songs} />
		</div>
	)
}

interface RecommendationProps {
	recommendations: Song[]
}

const RecommendationList = ({ recommendations }: RecommendationProps) => {
	return (
		<ul className="space-y-4">
			{recommendations.map((recommendation) => (
				<li key={recommendation.id} className="bg-white rounded-md shadow-md p-4">
					<h3 className="font-bold text-lg">{recommendation.title}</h3>
					<p className="text-gray-500">{recommendation.artist}</p>
				</li>
			))}
		</ul>
	)
}

const App: React.FC = () => {
	const songs: Song[] = [
		{ id: 1, title: "Song 1", artist: "Artist 1" },
		{ id: 2, title: "Song 2", artist: "Artist 2" },
		{ id: 3, title: "Song 3", artist: "Artist 3" },
	]

	return (
		<div className="bg-black h-screen text-spotifyWhite w-screen">
			<nav className="bg-spotifyBlack text-spotifyWhite p-4">
				<h1 className="font-bold text-spotifyGreen text-2xl">Spotify Recommender</h1>
			</nav>
			<div className="flex">
				<Sidebar songs={songs} />
				<MainScreen />
			</div>
		</div>
	)
}

export default App
