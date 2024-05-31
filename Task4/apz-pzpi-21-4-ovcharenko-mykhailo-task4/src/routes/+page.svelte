<script lang="ts">
	import { extractToken, GET, type User } from "$lib"
	import Header from "$lib/components/Header.svelte"
	import { browser } from "$app/environment"
	import { translate } from "$lib/i18n"

	export let data: any

	let user: User
	if (data.token) {
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
	}
</script>

<Header {data} />
{#if user}
	<main class="dark:text-white text-center">
		<h1 class="font-bold mb-5 text-2xl">
			{$translate("welcome", { f: user.first_name, l: user.last_name })}
		</h1>

		<fieldset class="mb-5">
			<legend class="font-bold">{$translate("field.weight")}</legend>
			<span>{user.weight || $translate("unknown")}</span>
		</fieldset>
		<fieldset class="mb-5">
			<legend class="font-bold">{$translate("field.fat")}</legend>
			<span>{user.body_fat || $translate("unknown")}</span>
		</fieldset>
		<fieldset class="mb-5">
			<legend class="font-bold">{$translate("field.heart")}</legend>
			<span>{user.heart_rate || $translate("unknown")}</span>
		</fieldset>
		<fieldset class="mb-5">
			<legend class="font-bold">{$translate("field.oxygen")}</legend>
			<span>{user.oxygen_level || $translate("unknown")}</span>
		</fieldset>
		<fieldset class="mb-5">
			<legend class="font-bold">{$translate("field.blood")}</legend>
			<span>{user.blood_pressure || $translate("unknown")}</span>
		</fieldset>
	</main>
{/if}
