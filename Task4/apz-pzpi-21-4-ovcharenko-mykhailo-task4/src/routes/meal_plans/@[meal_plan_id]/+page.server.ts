// @ts-ignore
export function load({ params, cookies }) {
	const token = cookies.get("token")

	return {
		token: token,
		meal_plan_id: params.meal_plan_id,
	}
}
