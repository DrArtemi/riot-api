<script>
	import '../app.css';
	import { ApolloClient, InMemoryCache } from '@apollo/client/core';
	import { setClient } from 'svelte-apollo';
	import Search from '../components/search/Search.svelte';
	import { query } from 'svelte-apollo';
	import { SEARCH_ALL } from '../components/queries';

	const client = new ApolloClient({
		uri: 'http://localhost:3000/graphql',
		cache: new InMemoryCache()
	});
	setClient(client);

	let searchInput = '';
	const searchProps = { leagues: [], teams: [], players: [] };
	const search = query(SEARCH_ALL, { variables: { search: searchInput } });

	search.subscribe(({ data, error }) => {
		if (data) {
			const { searchLeagues: leagues, searchTeams: teams, searchPlayers: players } = data;

			searchProps.leagues = leagues;
			searchProps.teams = teams;
			searchProps.players = players;
		}
		if (error) {
			console.error(error);
		}
	});

	$: search.refetch({ search: searchInput });
</script>

<div class="absolute left-4 w-11/12 top-8 mx-auto border-l-2 border-l-amber-400">
	<Search bind:searchInput {...searchProps} />
</div>

<div class="flex h-full">
	<slot />
</div>

<style>
	@import url('https://fonts.googleapis.com/css?family=Roboto&display=swap');
	:global(body) {
		font-family: 'Roboto', Arial, Helvetica, sans-serif;
	}
</style>
