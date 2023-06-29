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
			if (image === "") {
				const STOCK_PHOTO = "https://picsum.photos/65"
				setAlbumart(STOCK_PHOTO)
			} else {
				setAlbumart(`data:image/png;base64,${image}`)
			}
		}
		retrieveAlbumArt()
	}, [albumUri])

	useEffect(() => {
		if (albumArt != "") console.log("ALBUM ART DEBUG: ", albumArt)
	}, [albumArt])
	return <img className="rounded h-50 w-50" src={albumArt} alt="Base64 Image" />
}

export default AlbumArt
