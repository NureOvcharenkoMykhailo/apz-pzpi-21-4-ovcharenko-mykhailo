import { writable } from "svelte/store"

export const globalAPI = writable("http://127.0.0.1:8000")
export const globalLocale = writable("en")

export const ITEMS_PER_PAGE = 16

export interface Global {
	API: string
	LOCALE: string
}

export const project: Global = {
	API: "http://127.0.0.1:8000",
	LOCALE: "en",
}

globalAPI.subscribe((value) => {
	project.API = value
})

globalLocale.subscribe((value) => {
	project.LOCALE = value
})

export function setCookie(cname: string, cvalue: string, exdays: number) {
	const d = new Date()
	d.setTime(d.getTime() + exdays * 24 * 60 * 60 * 1000)
	let expires = "expires=" + d.toUTCString()
	return cname + "=" + cvalue + ";" + expires + ";path=/"
}

export function deleteCookie(cname: string) {
	return cname + "=;expires=Thu, 01 Jan 1970 00:00:01 GMT;"
}

interface token {
	username: string
	password: string
}

export function extractToken(token: string): token {
	if (token == undefined) {
		return {
			username: "Unknown",
			password: "none",
		}
	}
	return {
		username: token.split(":")[0].split("@")[1],
		password: token.split(":")[1],
	}
}

interface response {
	code: number
	body: any
}

export async function GET(
	endpoint: string,
	method: string = "GET",
	headers: any = {},
	use_json: boolean = true
): Promise<response> {
	try {
		const response = await fetch(
			`${project.API}/api/${project.LOCALE}${endpoint}`,
			{
				method: method,
				headers: headers,
			}
		)
		if (!response.ok) {
			throw new Error(`Failed to fetch: ${await response.json()}`)
		}
		if (use_json) {
			return {
				code: response.status,
				body: await response.json(),
			}
		} else {
			return {
				code: response.status,
				body: await response.text(),
			}
		}
	} catch (err: any) {
		console.log(err.message)
	}

	return { code: 0, body: null }
}

export async function DELETE(
	endpoint: string,
	headers: any
): Promise<response> {
	return GET(endpoint, "DELETE", headers)
}

export async function POST(
	endpoint: string,
	data: any,
	headers: string[] = [],
	is_json: boolean = true
): Promise<response> {
	try {
		let head = {
			"Content-Type": "application/json",
		}
		headers.forEach((header) => {
			// @ts-ignore
			head[header.split("->")[0]] = header.split("->")[1]
		})

		const response = await fetch(
			`${project.API}/api/${project.LOCALE}${endpoint}`,
			{
				method: "POST",
				headers: head,
				body: JSON.stringify(data),
			}
		)
		if (!response.ok) {
			return {
				code: response.status,
				body: await response.json(),
			}
		}
		if (is_json) {
			return {
				code: response.status,
				body: await response.json(),
			}
		} else {
			return {
				code: response.status,
				body: await response.text(),
			}
		}
	} catch (err: any) {
		console.log(err.message)
	}

	return { code: 0, body: null }
}

export interface User {
	user_id: string
	email: string
	first_name: string
	last_name: string
	weight?: number
	body_fat?: number
	heart_rate?: number
	blood_pressure?: number
	oxygen_level?: number
	role: {
		id: number
		name: string
	}
	date_of_birth: string
	created_at: string
	updated_at: string
	last_seen_at: string
}

export interface Food {
	food_id: number
	name: string
	description: string
	photo_url: string
	carbs: number
	protein: number
	fat: number
	calories: number
	nutrition: {
		nutrition_id: number
		vitamins: any
		minerals: any
		amino_acids: any
	}
}

export interface Diet {
	diet_id: number
	name: string
	description: string
	photo_url: string
	average_intake: {
		carbs: number
		protein: number
		fat: number
		calories: number
		vitamins: number
		minerals: number
		amino_acids: number
	}
}

export interface MealPlan {
	meal_plan_id: number
	time: number
	diet: Diet
}

export const VITAMINS = [
	"vitamin_a",
	"vitamin_b6",
	"vitamin_b12",
	"vitamin_c",
	"vitamin_d",
	"vitamin_e",
	"vitamin_k1",
	"betaine",
	"choline",
	"folate",
	"thiamin",
	"riboflavin",
	"pantothenic_acid",
	"niacin",
]

export const MINERALS = [
	"calcium",
	"copper",
	"fluoride",
	"iron",
	"magnesium",
	"manganese",
	"phosphorus",
	"potassium",
	"selenium",
	"sodium",
	"zinc",
]

export const AMINO_ACIDS = [
	"alanine",
	"arginine",
	"aspartic_acid",
	"cystine",
	"glutamic_acid",
	"glycine",
	"histidine",
	"isoleucine",
	"leucine",
	"lysine",
	"methionine",
	"phenylalanine",
	"proline",
	"serine",
	"threonine",
	"tyrosine",
	"valine",
]
