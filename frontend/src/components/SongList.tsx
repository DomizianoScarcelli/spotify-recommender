import React, { MouseEventHandler, useState } from "react"
import { SongType } from "../shared/types"

type SongListProps = {
	header: boolean
	small: boolean
	songs?: SongType[]
	playlistState: { playlistSongs: SongType[]; setPlaylistSongs: any }
}

const SongList = ({ header, small, songs, playlistState }: SongListProps) => {
	const { playlistSongs, setPlaylistSongs } = playlistState

	const handleClick = (song: SongType) => {
		if (small) {
			addSongToPlaylist(song)
		}
	}

	const addSongToPlaylist = (song: SongType) => {
		setPlaylistSongs([...playlistSongs, song])
	}

	return (
		<>
			{header ? <Header /> : null}
			<li className="flex flex-col pt-3 whitespace-nowrap overflow-clip ">
				{songs?.map((song, index) => (
					<Song small={small} songDetails={song} index={index + 1} key={index} onClick={handleClick} />
				))}
			</li>
		</>
	)
}

type SongProps = {
	small: boolean
	index: number
	songDetails: SongType
	onClick: (song: SongType) => void
}
const Song = ({ small, index, songDetails, onClick }: SongProps) => {
	const { name, artist, album, duration, matchingPositions } = songDetails

	// Function to check if a character index is in the matchingCharacters array
	const isMatchingCharacter = (index: number) => {
		if (!matchingPositions || !small) return false
		return matchingPositions.includes(index)
	}

	return (
		<div className={`flex rounded-lg hover:bg-spotifyGray p-4 cursor-pointer ${small ? "justify-between w-full bg-red-500" : "items-center"}`} onClick={(e) => onClick(songDetails)}>
			{small ? <></> : <p className="text-spotifyLightGray text-sm w-1/12">{index}</p>}
			<div className={`flex bg-purple-500 ${small ? "max-w-[180px] overflow-hidden" : "w-4/12"}  gap-3`}>
				<img src="https://picsum.photos/50" className="rounded h-50 w-50" />
				<div className="flex flex-col justify-between">
					<p className="font-medium text-m text-spotifyWhite">
						{name.split("").map((char, index) => (
							<span key={index} className={isMatchingCharacter(index) ? "text-spotifyGreen" : ""}>
								{char}
							</span>
						))}
					</p>
					<p className="font-medium text-sm text-spotifyLightGray">{artist}</p>
				</div>
			</div>
			{small ? (
				<div className="flex flex-col bg-green-300 max-w-[150px] justify-around overflow-hidden">
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
