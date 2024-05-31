<script lang="ts">
	import Header from "$lib/components/Header.svelte"
	import {
		Listgroup,
		ListgroupItem,
		Button,
		Dropdown,
		DropdownItem,
	} from "flowbite-svelte"
	import { GET, POST, type Diet, type Food } from "$lib"
	import { translate } from "$lib/i18n"

	interface Type {
		name: string
		value: number
	}

	export let data: any
	let errors: string[] = []

	let diets: Diet[] = []
	GET(`/diet/all/@0:1024`).then((response) => {
		if (response.code != 200) {
			console.log(response.body)
			alert("Error fetching data!")
			return
		}
		diets = response.body.results
	})

	let foods: Food[] = []
	GET(`/food/all/@0:1024`).then((response) => {
		if (response.code != 200) {
			console.log(response.body)
			alert("Error fetching data!")
			return
		}
		foods = response.body.results
	})

	let selectedFoods: Type[] = []
</script>

<Header {data} />
<main class="dark:text-white flex-col justify-stretch w-fit m-auto gap-5">
	<h5 class="mb-4 font-bold">{$translate("meal_plan.new")}</h5>
	<select class="text-black" id="time">
		<option value="0">{$translate("breakfast")}</option>
		<option value="1">{$translate("lunch")}</option>
		<option value="2">{$translate("snack")}</option>
		<option value="3">{$translate("dinner")}</option>
	</select>
	<select class="text-black" id="diet_id">
		{#each diets as diet}
			<option value={diet.diet_id}>{diet.name}</option>
		{/each}
	</select>
	<span>Foods:</span>
	<Listgroup active class="w-48">
		{#each selectedFoods as food}
			<ListgroupItem class="text-base font-semibold gap-2">
				<span>{food.name}</span>
				<Button
					on:click={() => {
						selectedFoods = selectedFoods.filter(
							(v) => v.name !== food.name
						)
					}}
					>-
				</Button>
			</ListgroupItem>
		{/each}
		<ListgroupItem class="text-base font-semibold gap-2"
			>{$translate("new")}</ListgroupItem
		>
		<Dropdown>
			{#each foods as item}
				<DropdownItem
					id={item}
					on:click={() => {
						selectedFoods = [
							...selectedFoods,
							{
								name: item.name,
								value: item.food_id,
							},
						]
					}}>{item.name}</DropdownItem
				>
			{/each}
		</Dropdown>
	</Listgroup>
	{#each errors as error}
		<span class="text-red-500 mb-5">{error}</span>
	{/each}
	<Button
		on:click={async () => {
			errors = []

			let post_data = {}
			const post_fields = ["time", "diet_id"]
			post_fields.forEach((name) => {
				// @ts-ignore
				post_data[name] = document.getElementById(name)?.value
			})
			let result = ""
			for (const item of selectedFoods) {
				result += item.value
			}
			// @ts-ignore
			post_data["foods"] = result

			let response = await POST("/mealplan/create", post_data, [
				`Authorization->${data.token}`,
			])
			if (response.code != 200) {
				if (typeof response.body.error == "string") {
					errors = [...errors, response.body.error]
					return
				}
				for (const key in response.body.error) {
					if (response.body.error.hasOwnProperty(key)) {
						const value = response.body.error[key]
						errors.push(
							// @ts-ignore
							`${value} ("${document.getElementById(key)?.value}")`
						)
						errors = [...errors]
					}
				}
				return
			}

			window.location.href = window.location.origin + "/meal_plans"
		}}>{$translate("save")}</Button
	>
</main>
