// @ts-ignore
export function load({ cookies }) {
	const token = cookies.get("token")

	return {
		token: token,
	}
}
