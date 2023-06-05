import React from "react"

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

export default Song
