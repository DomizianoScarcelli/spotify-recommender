export const convertMillisecondsToMinutesAndSeconds = (milliseconds: number): string => {
	const totalSeconds = Math.floor(milliseconds / 1000)
	const minutes = Math.floor(totalSeconds / 60)
	const seconds = totalSeconds % 60
	const formattedMinutes = String(minutes).padStart(2, "0")
	const formattedSeconds = String(seconds).padStart(2, "0")
	return `${formattedMinutes}:${formattedSeconds}`
}
