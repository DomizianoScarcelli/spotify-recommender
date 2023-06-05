import React from "react"

const SongList = () => {
	return (
		<>
			<div className="flex text-spotifyLightGray w-full pt-3 justify-around">
				<p>#</p>
				<p>Title</p>
				<p>Album</p>
				<p>Duration</p>
			</div>
			<hr className="border-spotifyGray my-1" />
			<li className="flex flex-col pt-5 gap-5">
				<Song />
				<Song />
				<Song />
			</li>
		</>
	)
}

const Song = () => {
	return (
		<div className="flex gap-3">
			<img src="https://picsum.photos/50" className="rounded h-50 w-50" />
			<div className="flex flex-col justify-between">
				<p className="font-medium text-m text-spotifyWhite">Jaden</p>
				<p className="font-medium text-sm text-spotifyLightGray">SYRE</p>
			</div>
		</div>
	)
}

export default SongList
