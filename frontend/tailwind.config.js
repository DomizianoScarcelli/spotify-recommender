/** @type {import('tailwindcss').Config} */
export default {
	content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
	theme: {
		extend: {
			colors: {
				spotifyGreen: "#1DB954",
				spotifyBlack: "#191414",
				spotifyWhite: "#FFFFFF",
				spotifyGray: "#B3B3B3",
			},
		},
	},
	plugins: [],
}
