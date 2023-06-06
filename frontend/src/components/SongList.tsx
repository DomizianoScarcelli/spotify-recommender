import React from "react"
import { SongType } from "../shared/types"

type SongListProps = {
	header: boolean
	small: boolean
	songs?: SongType[]
}

const SongList = ({ header, small, songs }: SongListProps) => {
	return (
		<>
			{header ? <Header /> : null}
			<li className="flex flex-col pt-3 whitespace-nowrap">
				{songs?.map((song, index) => (
					<Song small={small} songDetails={song} index={index + 1} />
				))}
			</li>
		</>
	)
}

type SongProps = {
	small: boolean
	index: number
	songDetails: SongType
}
const Song = ({ small, index, songDetails }: SongProps) => {
	const { name, artist, album, duration } = songDetails
	return (
		<div className={`flex rounded-lg hover:bg-spotifyGray p-4 ${small ? "justify-between" : "items-center"}`}>
			{small ? <></> : <p className="text-spotifyLightGray text-sm w-1/12">{index}</p>}
			<div className="flex w-4/12 gap-3">
				<img src="https://picsum.photos/50" className="rounded h-50 w-50" />
				<div className="flex flex-col justify-between">
					<p className="font-medium text-m text-spotifyWhite">{name}</p>
					<p className="font-medium text-sm text-spotifyLightGray">{artist}</p>
				</div>
			</div>
			{small ? (
				<div className="flex flex-col justify-around">
					<p className="text-spotifyLightGray text-sm">{album}</p>
					<p className="text-spotifyLightGray text-sm">{duration}</p>
				</div>
			) : (
				<>
					<p className="text-spotifyLightGray text-sm w-4/12">{album}</p>
					<p className="text-spotifyLightGray text-sm w-2/12">{duration}</p>
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
