// @ts-ignore
export function load({ params, cookies }) {
	const token = cookies.get("token")

	return {
		token: token,
		food_id: params.food_id,
	}
}
