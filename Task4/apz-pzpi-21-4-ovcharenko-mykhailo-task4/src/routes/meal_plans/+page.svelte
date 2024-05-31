<script lang="ts">
	import Header from "$lib/components/Header.svelte"
	import { Button, Card } from "flowbite-svelte"
	import {
		GET,
		ITEMS_PER_PAGE,
		extractToken,
		type Diet,
		type MealPlan,
		type User,
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

	let page = 0
	let maxPages = 1
	let meal_plans: MealPlan[] = []
	function update() {
		GET(`/mealplan/all/@${page}:${ITEMS_PER_PAGE}`).then((response) => {
			if (response.code != 200) {
				console.log(response.body)
				alert("Error fetching data!")
				return
			}
			maxPages = Math.round(response.body.overflow / ITEMS_PER_PAGE) + 1
			if (maxPages <= page) {
				page = maxPages - 1
			}
			meal_plans = response.body.results
		})
	}
	update()
</script>

<Header {data} />
<main class="dark:text-white flex-col justify-stretch w-fit m-auto gap-5">
	<h1 class="mb-5 text-2xl font-bold dark:text-white">
		{$translate("meal_plan")}
	</h1>
	{#each meal_plans as meal_plan}
		<Card>
			<img
				src={meal_plan.diet.photo_url}
				alt={meal_plan.diet.photo_url}
			/>
			{meal_plan.diet.name}
			<Button outline={true} href="/meal_plans/@{meal_plan.meal_plan_id}"
				>{$translate("more")}</Button
			>
		</Card>
	{/each}
	{#if user?.role.id > 0}
		<Button style="width: 100%;" href="/meal_plans/new"
			>{$translate("new")}</Button
		>
	{/if}
</main>
