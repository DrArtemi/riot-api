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

    let searchInput = "";

    // Search leagues
    const leagues = query(SEARCH_LEAGUES, {
        variables: { "search": searchInput }
    });
    $: leagues.refetch({ "search": searchInput });
    // Search teams
    const teams = query(SEARCH_TEAMS, {
        variables: { "search": searchInput }
    });
    $: teams.refetch({ "search": searchInput });
    // Search players
    const players = query(SEARCH_PLAYERS, {
        variables: { "search": searchInput }
    });
    $: players.refetch({ "search": searchInput });
</script>

<div class="absolute left-8 w-11/12 top-8 mx-auto border-l-2 border-l-amber-400">
    <Search
        bind:searchInput={searchInput}
        leagues={leagues}
        teams={teams}
        players={players}
    />
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