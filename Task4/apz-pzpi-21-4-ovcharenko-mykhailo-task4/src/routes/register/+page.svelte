<script lang="ts">
	import Header from "$lib/components/Header.svelte"
	import { Card, Label, Input, Button } from "flowbite-svelte"
	import { UserOutline } from "flowbite-svelte-icons"
	import { GET, POST, setCookie } from "$lib"
	import { translate } from "$lib/i18n"

	export let data: any
	let errors: string[] = []

	const validateEmail = (email: string) => {
		return String(email)
			.toLowerCase()
			.match(
				/^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|.(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
			)
	}
</script>

<Header {data} />
<main class="dark:text-white">
	<Card>
		<h1 class="mb-5 text-2xl font-bold dark:text-white">Register</h1>
		<div class="mb-5">
			<Label class="block mb-2">{$translate("username")}</Label>
			<Input
				id="user_id"
				required
				placeholder="@user_id"
				maxlength="16"
			/>
		</div>
		<div class="mb-5">
			<Label class="block mb-2">{$translate("first_name")}</Label>
			<Input id="first_name" required placeholder="" />
		</div>
		<div class="mb-5">
			<Label class="block mb-2">{$translate("last_name")}</Label>
			<Input id="last_name" required placeholder="" />
		</div>
		<div class="mb-5">
			<Label class="block mb-2">{$translate("email")}</Label>
			<Input
				id="email"
				type="email"
				required
				placeholder="me@example.com"
			/>
		</div>
		<div class="mb-5">
			<Label class="block mb-2">{$translate("password")}</Label>
			<Input
				id="password"
				required
				type="password"
				placeholder="••••••"
			/>
		</div>
		<div class="mb-5">
			<Label class="block mb-2">{$translate("birth")}</Label>
			<Input id="date_of_birth" type="date" required placeholder="" />
		</div>
		<a class="mb-5" href="/login">{$translate("yes_account")}</a>
		{#each errors as error}
			<span class="text-red-500 mb-5">{error}</span>
		{/each}
		<Button
			class="w-fit"
			on:click={async () => {
				errors = []

				let post_data = {}
				const post_fields = [
					"user_id",
					"first_name",
					"last_name",
					"email",
					"password",
					"date_of_birth",
				]
				post_fields.forEach((name) => {
					// @ts-ignore
					post_data[name] = document.getElementById(name)?.value
				})

				let response = await POST("/account/register", post_data)
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

				document.cookie = setCookie("token", response.body.token, 60)
				window.location.href = window.location.origin
			}}
		>
			{$translate("register")}
			<UserOutline class="w-6 h-6 ms-2 text-white" />
		</Button>
	</Card>
</main>
