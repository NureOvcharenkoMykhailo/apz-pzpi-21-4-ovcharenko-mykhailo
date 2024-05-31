<script lang="ts">
	import Header from "$lib/components/Header.svelte"
	import { Card, Label, Input, Button, Select } from "flowbite-svelte"
	import { GET, POST, extractToken, project, type User } from "$lib"
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
<main class="dark:text-white">
	<h1>{$translate("admin.backups")}:</h1>
	<div>
		<select id="backup" class="text-black">
			<option value="users" selected>{$translate("admin.users")}</option>
			<option value="profiles">{$translate("admin.profiles")}</option>
			<option value="diets">{$translate("header.diets")}</option>
			<option value="meal_plans">{$translate("header.meal_plans")}</option
			>
			<option value="submissions"
				>{$translate("admin.submissions")}</option
			>
			<option value="foods">{$translate("header.foods")}</option>
			<option value="nutritions">{$translate("admin.nutritions")}</option>
		</select>
		<Button
			on:click={() => {
				// @ts-ignore
				const val = document.getElementById("backup").value
				GET(
					`/system/backup/@${val}`,
					"GET",
					{
						Authorization: data.token,
					},
					false
				).then((response) => {
					if (response.code != 200) {
						console.log(response.body)
						alert("Error fetching data!")
						return
					}
					const popup = window.open()
					if (popup) {
						popup.document.write(
							response.body.split("\n").join("<br/>")
						)
						popup.document.title = `${val}.csv`
					}
				})
			}}>{$translate("create")}</Button
		>
	</div>
	<h1>{$translate("admin.rollback")}:</h1>
	<div>
		<select id="rollback" class="text-black">
			<option value="users" selected>{$translate("admin.users")}</option>
			<option value="profiles">{$translate("admin.profiles")}</option>
			<option value="diets">{$translate("header.diets")}</option>
			<option value="meal_plans">{$translate("header.meal_plans")}</option
			>
			<option value="submissions"
				>{$translate("admin.submissions")}</option
			>
			<option value="foods">{$translate("header.foods")}</option>
			<option value="nutritions">{$translate("admin.nutritions")}</option>
		</select>
		<Button
			on:click={() => {
				// @ts-ignore
				const val = document.getElementById("rollback").value
				POST(
					`/system/rollback`,
					{
						resource: val,
						// @ts-ignore
						data: document.getElementById("rollback_data").value,
					},
					[`Authorization->${data.token}`],
					false
				).then((response) => {
					if (response.code != 200) {
						console.log(response.body)
						alert("Error fetching data!")
						return
					}
					window.location.href = window.location.origin
				})
			}}>{$translate("submit")}</Button
		>
	</div>
	<textarea
		id="rollback_data"
		placeholder="file.csv"
		class="text-black w-full"
	></textarea>
</main>
