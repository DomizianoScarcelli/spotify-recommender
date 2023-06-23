import { useEffect, useState } from "react"
import { getAlbumArt } from "../utils/apiCalls"

type Props = {
	albumUri: string
}
const AlbumArt = ({ albumUri }: Props) => {
	const [albumArt, setAlbumart] = useState<string>("")
	useEffect(() => {
		const retrieveAlbumArt = async () => {
			const image = await getAlbumArt(albumUri)
			setAlbumart(image)
		}
		retrieveAlbumArt()
	}, [albumUri])

	useEffect(() => {
		if (albumArt != "") console.log("ALBUM ART DEBUG: ", albumArt)
	}, [albumArt])
	return <img className="rounded h-50 w-50" src={`data:image/png;base64,${albumArt}`} alt="Base64 Image" />
}

export default AlbumArt
