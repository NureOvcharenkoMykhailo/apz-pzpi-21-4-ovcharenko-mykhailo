import { derived, writable } from "svelte/store"
import translations from "./translations"
import { globalLocale } from "$lib"

export const locales = Object.keys(translations)

function get_translations(locale: string, key: string, vars: any) {
	// Let's throw some errors if we're trying to use keys/locales that don't exist.
	// We could improve this by using Typescript and/or fallback values.
	if (!key) return "~~"
	if (!locale) return "~~"

	// Grab the translation from the translations object.
	// @ts-ignore
	let text = translations[locale][key]

	if (!text) return `~${key}~`

	// Replace any passed in variables in the translation string.
	Object.keys(vars).map((k) => {
		const regex = new RegExp(`{{${k}}}`, "g")
		text = text.replace(regex, vars[k])
		console.log(text)
	})

	return text
}

export const translate = derived(
	globalLocale,
	($locale) =>
		(key: string, vars = {}) =>
			get_translations($locale, key, vars)
)
