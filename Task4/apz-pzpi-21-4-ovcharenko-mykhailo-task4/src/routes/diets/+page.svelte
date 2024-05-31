<script lang="ts">
	import Header from "$lib/components/Header.svelte"
	import { Button, Card } from "flowbite-svelte"
	import {
		GET,
		ITEMS_PER_PAGE,
		extractToken,
		type Diet,
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
	let diets: Diet[] = []
	function update() {
		GET(`/diet/all/@${page}:${ITEMS_PER_PAGE}`).then((response) => {
			if (response.code != 200) {
				console.log(response.body)
				alert("Error fetching data!")
				return
			}
			maxPages = Math.round(response.body.overflow / ITEMS_PER_PAGE) + 1
			if (maxPages <= page) {
				page = maxPages - 1
			}
			diets = response.body.results
		})
	}
	update()
</script>

<Header {data} />
<main class="dark:text-white flex-col justify-stretch w-fit m-auto gap-5">
	<h1 class="mb-5 text-2xl font-bold dark:text-white">
		{$translate("diet")}
	</h1>
	{#each diets as diet}
		<Card>
			<img src={diet.photo_url} alt={diet.photo_url} />
			<h5>{diet.name}</h5>
			{diet.description}
			<h5>Average intake:</h5>
			<span>{$translate("fat", { v: diet.average_intake.fat })}</span>
			<span>{$translate("carbs", { v: diet.average_intake.carbs })}</span>
			<span
				>{$translate("protein", {
					v: diet.average_intake.protein,
				})}</span
			>
			<span
				>{$translate("calories", {
					v: diet.average_intake.calories,
				})}</span
			>
			<span
				>{$translate("amino_acids", {
					v: JSON.stringify(diet.average_intake.amino_acids),
				})}</span
			>
			<span
				>{$translate("minerals", {
					v: JSON.stringify(diet.average_intake.minerals),
				})}</span
			>
			<span
				>{$translate("vitamins", {
					v: JSON.stringify(diet.average_intake.vitamins),
				})}</span
			>
			<Button outline={true} href="/diets/@{diet.diet_id}"
				>{$translate("more")}</Button
			>
		</Card>
	{/each}
	{#if user?.role.id > 0}
		<Button style="width: 100%;" href="/diets/new"
			>{$translate("new")}</Button
		>
	{/if}
</main>
