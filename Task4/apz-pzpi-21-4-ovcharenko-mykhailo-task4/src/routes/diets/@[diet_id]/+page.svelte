<script lang="ts">
	import Header from "$lib/components/Header.svelte"
	import { Button } from "flowbite-svelte"
	import { GET, type User, extractToken, DELETE, type Diet } from "$lib"
	import { translate } from "$lib/i18n"

	export let data: any

	let user: User
	GET(`/account/query/@${extractToken(data.token).username}`).then(
		(response) => {
			if (response.code != 200) {
				console.log(response.body)
				alert("Error fetching data!")
				return
			}
			user = response.body
		}
	)

	let diet: Diet | null = null
	GET(`/diet/query/@${data.diet_id}`).then((response) => {
		if (response.code != 200) {
			alert(JSON.stringify(response.body))
			return
		}

		diet = response.body
	})
</script>

<Header {data} />
<main class="dark:text-white">
	<img src={diet?.photo_url} alt={diet?.photo_url} />
	<h5 class="text-2xl font-bold tracking-tight dark:text-white">
		{diet?.name}
	</h5>
	{diet?.description}
	{#if user?.role.id > 0}
		<Button
			on:click={() => {
				DELETE(`/diet/delete/@${diet?.diet_id}`, {
					Authorization: data.token,
				})
				window.location.href = window.location.origin + "/diets"
			}}>{$translate("delete")}</Button
		>
		<Button href="/diets/edit@{diet?.diet_id}">{$translate("edit")}</Button>
	{/if}
</main>
