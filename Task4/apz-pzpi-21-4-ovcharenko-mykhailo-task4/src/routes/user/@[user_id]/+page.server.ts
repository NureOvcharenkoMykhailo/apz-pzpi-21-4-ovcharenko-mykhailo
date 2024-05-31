// @ts-ignore
export function load({ params, cookies }) {
	const token = cookies.get("token")

	return {
		token: token,
		user_id: params.user_id,
	}
}
