<script>
    import "../app.css";
    import { ApolloClient, InMemoryCache } from '@apollo/client/core';
    import { setClient } from "svelte-apollo";
    import Search from '../components/search/Search.svelte';
    import { query } from 'svelte-apollo';
    import { SEARCH_LEAGUES, SEARCH_TEAMS, SEARCH_PLAYERS } from '../components/queries';

    const client = new ApolloClient({
        uri: "http://localhost:3000/graphql",
        cache: new InMemoryCache()
    });
    setClient(client);

    let search_input = "";
    // Search leagues
    const leagues = query(SEARCH_LEAGUES, {
        variables: { "search": search_input }
    });
    $: leagues.refetch({ "search": search_input });
    // Search teams
    const teams = query(SEARCH_TEAMS, {
        variables: { "search": search_input }
    });
    $: teams.refetch({ "search": search_input });
    // Search players
    const players = query(SEARCH_PLAYERS, {
        variables: { "search": search_input }
    });
    $: players.refetch({ "search": search_input });

</script>

<div class="absolute left-8 w-11/12 top-8 mx-auto border-l-2 border-l-amber-400">
    <Search
        bind:search_input={search_input}
        leagues={leagues}
        teams={teams}
        players={players}
    />
</div>

<slot />

<style>
    @import url('https://fonts.googleapis.com/css?family=Roboto&display=swap');
    :global(body) {
        font-family: 'Roboto', Arial, Helvetica, sans-serif;
    }
</style>