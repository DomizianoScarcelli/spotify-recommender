import React from "react"

type SongListProps = {
	header: boolean
	small: boolean
}

const SongList = ({ header, small }: SongListProps) => {
	return (
		<>
			{header ? <Header /> : null}
			<li className="flex flex-col pt-5 gap-5">
				<Song small={small} />
				<Song small={small} />
				<Song small={small} />
			</li>
		</>
	)
}

type SongProps = {
	small: boolean
}
const Song = ({ small }: SongProps) => {
	return (
		<div className={`flex ${small ? "justify-between" : "items-center"}`}>
			{small ? <></> : <p className="text-spotifyLightGray text-sm w-1/12">1</p>}
			<div className="flex w-4/12 gap-3">
				<img src="https://picsum.photos/50" className="rounded h-50 w-50" />
				<div className="flex flex-col justify-between">
					<p className="font-medium text-m text-spotifyWhite">Jaden</p>
					<p className="font-medium text-sm text-spotifyLightGray">SYRE</p>
				</div>
			</div>
			{small ? (
				<div className="flex flex-col justify-around">
					<p className="text-spotifyLightGray text-sm">SYRE</p>
					<p className="text-spotifyLightGray text-sm">2:33</p>
				</div>
			) : (
				<>
					<p className="text-spotifyLightGray text-sm w-4/12">SYRE</p>
					<p className="text-spotifyLightGray text-sm w-2/12">2:33</p>
				</>
			)}
		</div>
	)
}

const Header = () => {
	return (
		<>
			<div className="flex text-spotifyLightGray w-full pt-3">
				<p className="w-1/12">#</p>
				<p className="w-4/12">Title</p>
				<p className="w-4/12">Album</p>
				<p className="w-2/12">Duration</p>
			</div>
			<hr className="border-spotifyGray my-1" />
		</>
	)
}

export default SongList
