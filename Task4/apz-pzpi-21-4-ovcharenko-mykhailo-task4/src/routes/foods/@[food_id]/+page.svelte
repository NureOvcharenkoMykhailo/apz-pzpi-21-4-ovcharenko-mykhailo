<script lang="ts">
	import Header from "$lib/components/Header.svelte"
	import { Button } from "flowbite-svelte"
	import { GET, type User, extractToken, type Food, DELETE } from "$lib"
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

	let food: Food | null = null
	GET(`/food/query/@${data.food_id}`).then((response) => {
		if (response.code != 200) {
			alert(JSON.stringify(response.body))
			return
		}

		food = response.body
	})
</script>

<Header {data} />
<main class="dark:text-white">
	<img src={food?.photo_url} alt={food?.photo_url} />
	<h5 class="text-2xl font-bold tracking-tight dark:text-white">
		{food?.name}
	</h5>
	{food?.description}
	{#if user?.role.id > 0}
		<Button
			on:click={() => {
				DELETE(`/food/delete/@${food?.food_id}`, {
					Authorization: data.token,
				})
				window.location.href = window.location.origin + "/foods"
			}}>{$translate("delete")}</Button
		>
		<Button href="/foods/edit@{food?.food_id}">{$translate("edit")}</Button>
	{/if}
</main>
