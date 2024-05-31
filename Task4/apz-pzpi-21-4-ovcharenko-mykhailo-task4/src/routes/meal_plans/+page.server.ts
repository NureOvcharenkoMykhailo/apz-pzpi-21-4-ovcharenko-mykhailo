// @ts-ignore
export function load({ params, cookies }) {
	const token = cookies.get("token")

	return {
		token: token,
	}
}
