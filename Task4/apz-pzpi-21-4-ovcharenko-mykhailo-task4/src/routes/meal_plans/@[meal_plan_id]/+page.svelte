<script lang="ts">
	import Header from "$lib/components/Header.svelte"
	import { Button } from "flowbite-svelte"
	import {
		GET,
		type User,
		extractToken,
		DELETE,
		type Diet,
		type MealPlan,
	} from "$lib"
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

	let mealPlan: MealPlan | null = null
	GET(`/mealplan/query/@${data.meal_plan_id}`).then((response) => {
		if (response.code != 200) {
			alert(JSON.stringify(response.body))
			return
		}

		mealPlan = response.body
	})
</script>

<Header {data} />
<main class="dark:text-white">
	<img src={mealPlan?.diet.photo_url} alt={mealPlan?.diet.photo_url} />
	<h5 class="text-2xl font-bold tracking-tight dark:text-white">
		{mealPlan?.diet.name}
	</h5>
	{#if user?.role.id > 0}
		<Button
			on:click={() => {
				DELETE(`/mealplan/delete/@${mealPlan?.meal_plan_id}`, {
					Authorization: data.token,
				})
				window.location.href = window.location.origin + "/meal_plans"
			}}>{$translate("delete")}</Button
		>
	{/if}
</main>
