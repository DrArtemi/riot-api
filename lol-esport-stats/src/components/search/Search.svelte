<script>
	import SearchSuggest from './SearchSuggest.svelte';

	export let searchInput;
	export let leagues;
	export let teams;
	export let players;
</script>

<input
	class="w-full bg-slate-900 hover:bg-slate-700 rounded-r-md bg-inherit outline-none border-none px-4 py-1 text-xl text-slate-200"
	type="text"
	bind:value={searchInput}
	placeholder="League, team, player..."
/>
{#if searchInput}
	<div class="bg-slate-800 rounded-br-md">
		<SearchSuggest
			search_data={[
				{ category: 'Leagues', data: leagues },
				{ category: 'Teams', data: teams },
				{ category: 'Players', data: players }
			]}
		/>
	</div>
{/if}

<style>
</style>
