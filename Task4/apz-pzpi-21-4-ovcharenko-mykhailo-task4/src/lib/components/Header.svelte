<script lang="ts">
	import { extractToken } from "$lib"
	import { translate } from "$lib/i18n"
	import {
		Navbar,
		NavBrand,
		NavHamburger,
		NavUl,
		NavLi,
		Dropdown,
		DropdownItem,
	} from "flowbite-svelte"

	export let data: any
</script>

<Navbar>
	<NavBrand href="/">
		<img src="/favicon.png" class="me-3 h-6 sm:h-9" alt="Logo" />
		<span
			class="self-center whitespace-nowrap text-xl font-semibold dark:text-white"
			>Healfood</span
		>
	</NavBrand>
	<NavHamburger />
	<NavUl>
		<NavLi href="/">{$translate("header.home")}</NavLi>
		<NavLi href="/meal_plans">{$translate("header.meal_plans")}</NavLi>
		<NavLi href="/diets">{$translate("header.diets")}</NavLi>
		<NavLi href="/foods">{$translate("header.foods")}</NavLi>
		{#if data.token}
			<NavLi href="/admin">{$translate("header.admin")}</NavLi>
			<span>
				@{extractToken(data.token).username}
			</span>
			<Dropdown>
				<DropdownItem href="/user/@{extractToken(data.token).username}"
					>{$translate("header.my_profile")}</DropdownItem
				>
				<DropdownItem href="/settings"
					>{$translate("header.settings")}</DropdownItem
				>
				<DropdownItem href="/logout" slot="footer"
					>{$translate("header.sign_out")}</DropdownItem
				>
			</Dropdown>
		{:else}
			<NavLi href="/login">{$translate("header.login")}</NavLi>
		{/if}
	</NavUl>
</Navbar>
