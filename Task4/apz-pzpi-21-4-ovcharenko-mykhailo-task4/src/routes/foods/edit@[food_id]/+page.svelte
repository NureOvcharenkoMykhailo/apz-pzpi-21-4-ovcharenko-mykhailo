<script lang="ts">
	import Header from "$lib/components/Header.svelte"
	import {
		Listgroup,
		ListgroupItem,
		Input,
		Dropdown,
		DropdownItem,
		Button,
	} from "flowbite-svelte"
	import { AMINO_ACIDS, GET, MINERALS, POST, VITAMINS, type Food } from "$lib"
	import { translate } from "$lib/i18n"

	interface Type {
		name: string
		value: number
	}

	export let data: any
	let vitamins: Type[] = []
	let minerals: Type[] = []
	let amino_acids: Type[] = []
	let errors: string[] = []

	let food: Food = {
		food_id: 0,
		name: "",
		description: "",
		photo_url: "",
		carbs: 0,
		protein: 0,
		fat: 0,
		calories: 0,
		nutrition: {
			nutrition_id: 0,
			vitamins: undefined,
			minerals: undefined,
			amino_acids: undefined,
		},
	}
	GET(`/food/query/@${data.food_id}`).then((response) => {
		if (response.code != 200) {
			console.log(response.body)
			alert("Error fetching data!")
			return
		}
		food = response.body
		vitamins = []
		for (const vitamin in food?.nutrition.vitamins) {
			vitamins = [
				...vitamins,
				{ name: vitamin, value: food.nutrition.vitamins[vitamin] },
			]
		}
		minerals = []
		for (const mineral in food?.nutrition.minerals) {
			minerals = [
				...minerals,
				{ name: mineral, value: food.nutrition.minerals[mineral] },
			]
		}
		amino_acids = []
		for (const amino_acid in food?.nutrition.amino_acids) {
			amino_acids = [
				...amino_acids,
				{
					name: amino_acid,
					value: food.nutrition.amino_acids[amino_acid],
				},
			]
		}
	})
</script>

<Header {data} />
<main class="dark:text-white flex-col justify-stretch w-fit m-auto gap-5">
	<h5 class="mb-4 font-bold">{$translate("food.edit")}</h5>
	<Input
		maxlength="16"
		id="name"
		placeholder={$translate("name")}
		bind:value={food.name}
	/>
	<Input
		id="description"
		placeholder={$translate("description")}
		bind:value={food.description}
	/>
	<Input
		type="url"
		id="photo_url"
		placeholder={$translate("photo_url")}
		bind:value={food.photo_url}
	/>
	<Input
		type="number"
		id="carbs"
		placeholder={$translate("carbs")}
		bind:value={food.carbs}
	/>
	<Input
		type="number"
		id="protein"
		placeholder={$translate("protein")}
		bind:value={food.protein}
	/>
	<Input
		type="number"
		id="fat"
		placeholder={$translate("fat")}
		bind:value={food.fat}
	/>
	<Input
		type="number"
		id="calories"
		placeholder={$translate("calories")}
		bind:value={food.calories}
	/>
	<span>{$translate("vitamins", { v: "" })}</span>
	<Listgroup active class="w-48">
		{#each vitamins as vitamin}
			<ListgroupItem class="text-base font-semibold gap-2">
				<span>{vitamin.name} = {vitamin.value}</span>
				<Button
					on:click={() => {
						vitamins = vitamins.filter(
							(v) => v.name !== vitamin.name
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
			{#each VITAMINS as item}
				<DropdownItem
					id={item}
					on:click={() => {
						const number = Number(prompt("Enter the value:"))
						if (!number && number !== 0) {
							return
						}
						vitamins = [
							...vitamins,
							{
								name: item,
								value: number,
							},
						]
					}}>{item.replace("_", " ")}</DropdownItem
				>
			{/each}
		</Dropdown>
	</Listgroup>
	<span>{$translate("minerals", { v: "" })}</span>
	<Listgroup active class="w-48">
		{#each minerals as mineral}
			<ListgroupItem class="text-base font-semibold gap-2">
				<span>{mineral.name} = {mineral.value}</span>
				<Button
					on:click={() => {
						minerals = minerals.filter(
							(v) => v.name !== mineral.name
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
			{#each MINERALS as item}
				<DropdownItem
					id={item}
					on:click={() => {
						const number = Number(prompt("Enter the value:"))
						if (!number && number !== 0) {
							return
						}
						minerals = [
							...minerals,
							{
								name: item,
								value: number,
							},
						]
					}}>{item.replace("_", " ")}</DropdownItem
				>
			{/each}
		</Dropdown>
	</Listgroup>
	<span>{$translate("amino_acids", { v: "" })}</span>
	<Listgroup active class="w-48">
		{#each amino_acids as acid}
			<ListgroupItem class="text-base font-semibold gap-2">
				<span>{acid.name} = {acid.value}</span>
				<Button
					on:click={() => {
						amino_acids = amino_acids.filter(
							(v) => v.name !== acid.name
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
			{#each AMINO_ACIDS as item}
				<DropdownItem
					id={item}
					on:click={() => {
						const number = Number(prompt("Enter the value:"))
						if (!number && number !== 0) {
							return
						}
						amino_acids = [
							...amino_acids,
							{
								name: item,
								value: number,
							},
						]
					}}>{item.replace("_", " ")}</DropdownItem
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

			let post_data = {
				food_id: food.food_id,
			}
			const post_fields = [
				"name",
				"description",
				"photo_url",
				"carbs",
				"protein",
				"fat",
				"calories",
			]
			post_fields.forEach((name) => {
				// @ts-ignore
				post_data[name] = document.getElementById(name)?.value
			})
			let additional = {}
			vitamins.forEach((item) => {
				// @ts-ignore
				additional[item.name] = item.value
			})
			// @ts-ignore
			post_data["vitamins"] = JSON.stringify(additional)

			additional = {}
			minerals.forEach((item) => {
				// @ts-ignore
				additional[item.name] = item.value
			})
			// @ts-ignore
			post_data["minerals"] = JSON.stringify(additional)

			additional = {}
			amino_acids.forEach((item) => {
				// @ts-ignore
				additional[item.name] = item.value
			})
			// @ts-ignore
			post_data["amino_acids"] = JSON.stringify(additional)

			let response = await POST("/food/edit", post_data, [
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

			window.location.href = window.location.origin + "/foods"
		}}>{$translate("save")}</Button
	>
</main>
