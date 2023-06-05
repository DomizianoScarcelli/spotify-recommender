/** @type {import('tailwindcss').Config} */
export default {
	content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
	theme: {
		extend: {
			colors: {
				spotifyBlack: "#191414",
				spotifyDarkGray: "#121212",
				spotifyGray: "#B3B3B3",
				spotifyLightGray: "A7A7A7",
				spotifyWhite: "#FFFFFF",
				spotifyGreen: "#65D46E",
			},
			fontFamily: {
				gotham: ["Gotham", "sans-serif"],
			},
		},
	},
	plugins: [],
}
