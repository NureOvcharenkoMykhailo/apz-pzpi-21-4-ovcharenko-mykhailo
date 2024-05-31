<script lang="ts">
	import Header from "$lib/components/Header.svelte"
	import { Card, Label, Input, Button, Select } from "flowbite-svelte"
	import { UserOutline } from "flowbite-svelte-icons"
	import { POST, setCookie, project, globalAPI, globalLocale } from "$lib"
	import { translate } from "$lib/i18n"

	export let data: any
	let errors: string[] = []

	let selected: string = project.LOCALE
	let locales = [
		{ value: "en", name: "English (US)" },
		{ value: "ua", name: "Українська" },
	]
</script>

<Header {data} />
<main class="dark:text-white">
	<Card>
		<h1 class="mb-5 text-2xl font-bold dark:text-white">
			{$translate("settings")}
		</h1>
		<div class="mb-5">
			<Label class="block mb-2">{$translate("api")}</Label>
			<Input id="api" required value={project.API} />
		</div>
		<div class="mb-5">
			<Label class="block mb-2">{$translate("locale")}</Label>
			<Select id="locale" items={locales} bind:value={selected} />
		</div>
		<Button
			class="w-fit"
			on:click={async () => {
				// @ts-ignore
				globalAPI.set(document.getElementById("api")?.value)
				// @ts-ignore
				globalLocale.set(document.getElementById("locale")?.value)
			}}
		>
			{$translate("save")}
		</Button>
	</Card>
</main>
