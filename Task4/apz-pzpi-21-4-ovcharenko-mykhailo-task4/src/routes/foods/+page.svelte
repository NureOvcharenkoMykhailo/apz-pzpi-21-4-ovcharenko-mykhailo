<script lang="ts">
	import Header from "$lib/components/Header.svelte"
	import { Button, Card } from "flowbite-svelte"
	import {
		GET,
		ITEMS_PER_PAGE,
		extractToken,
		type Food,
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
	let foods: Food[] = []
	function update() {
		GET(`/food/all/@${page}:${ITEMS_PER_PAGE}`).then((response) => {
			if (response.code != 200) {
				console.log(response.body)
				alert("Error fetching data!")
				return
			}
			maxPages = Math.round(response.body.overflow / ITEMS_PER_PAGE) + 1
			if (maxPages <= page) {
				page = maxPages - 1
			}
			foods = response.body.results
		})
	}
	update()
</script>

<Header {data} />
<main class="dark:text-white flex-col justify-stretch w-fit m-auto gap-5">
	<h1 class="mb-5 text-2xl font-bold dark:text-white">
		{$translate("food")}
	</h1>
	{#each foods as food}
		<Card>
			<img src={food.photo_url} alt={food.photo_url} />
			<h1 class="mb-5 text-2xl font-bold dark:text-white">{food.name}</h1>
			<span>{food.description}</span>
			<div>
				<strong>{$translate("fat", { v: food.fat })}</strong>
				<strong>{$translate("carbs", { v: food.carbs })}</strong>
				<strong>{$translate("protein", { v: food.protein })}</strong>
			</div>
			<Button outline={true} href="/foods/@{food.food_id}"
				>{$translate("more")}</Button
			>
		</Card>
	{/each}
	{#if user?.role.id > 0}
		<Button style="width: 100%;" href="/foods/new"
			>{$translate("new")}</Button
		>
	{/if}
</main>
