<script lang="ts">
	import Header from "$lib/components/Header.svelte"
	import { Input, Button } from "flowbite-svelte"
	import { GET, POST, type Diet } from "$lib"
	import { translate } from "$lib/i18n"

	export let data: any
	let errors: string[] = []

	let diet: Diet = {
		diet_id: 0,
		name: "",
		description: "",
		photo_url: "",
		// @ts-ignore
		average_intake: {},
	}
	GET(`/diet/query/@${data.diet_id}`).then((response) => {
		if (response.code != 200) {
			console.log(response.body)
			alert("Error fetching data!")
			return
		}
		diet = response.body
	})
</script>

<Header {data} />
<main class="dark:text-white flex-col justify-stretch w-fit m-auto gap-5">
	<h5 class="mb-4 font-bold">{$translate("diet.edit")}</h5>
	<Input
		maxlength="16"
		id="name"
		placeholder={$translate("name")}
		bind:value={diet.name}
	/>
	<Input
		id="description"
		placeholder={$translate("description")}
		bind:value={diet.description}
	/>
	<Input
		type="url"
		id="photo_url"
		placeholder={$translate("photo_url")}
		bind:value={diet.photo_url}
	/>
	{#each errors as error}
		<span class="text-red-500 mb-5">{error}</span>
	{/each}
	<Button
		on:click={async () => {
			errors = []

			let post_data = {
				diet_id: diet.diet_id,
			}
			const post_fields = ["name", "description", "photo_url"]
			post_fields.forEach((name) => {
				// @ts-ignore
				post_data[name] = document.getElementById(name)?.value
			})
			let response = await POST("/diet/edit", post_data, [
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

			window.location.href = window.location.origin + "/diets"
		}}>{$translate("save")}</Button
	>
</main>
