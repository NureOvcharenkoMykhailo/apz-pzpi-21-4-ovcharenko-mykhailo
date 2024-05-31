<script lang="ts">
	import { browser } from "$app/environment"
	import { deleteCookie } from "$lib"

	if (browser) {
		document.cookie = deleteCookie("token")
		window.location.href = window.location.origin
	}
</script>

<div></div>
