<script lang="ts">
	import { GET, type User } from "$lib"
	import Header from "$lib/components/Header.svelte"
	import { translate } from "$lib/i18n"
	import { Card } from "flowbite-svelte"

	export let data: any

	let user: User | null = null
	GET(`/account/query/@${data.user_id}`).then((response) => {
		if (response.code != 200) {
			alert(JSON.stringify(response.body))
			return
		}

		user = response.body
	})
</script>

<Header {data} />
<main class="dark:text-white">
	<Card style="max-width: 32rem;">
		<h5 class="text-2xl font-bold tracking-tight dark:text-white">
			{user?.first_name}
			{user?.last_name}
		</h5>
		<span class="mb-2">@{user?.user_id}</span>
		<div class="flex items-baseline gap-2 dark:text-white">
			<span class="text-1xl font-semibold">{$translate("email")}</span>
			<span class="text-1xl font-normal">{user?.email}</span>
		</div>
		<div class="flex items-baseline gap-2 dark:text-white">
			<span class="text-1xl font-semibold">{$translate("birth")}</span>
			<span class="text-1xl font-normal"
				>{new Date(user?.date_of_birth || "").toLocaleString()}</span
			>
		</div>
	</Card>
</main>
