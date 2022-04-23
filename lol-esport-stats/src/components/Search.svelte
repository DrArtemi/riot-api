<script>
    import { query } from 'svelte-apollo';
    import { SEARCH_LEAGUES } from './queries';
    
    let search_input = "";
    const leagues = query(SEARCH_LEAGUES, {
        variables: { "search": search_input }
    });
    $: leagues.refetch({ "search": search_input });
</script>

<div>
    <input type="text" bind:value={search_input} placeholder="Player, Team, Tournament..." />
    {#if $leagues.loading}
        Loading...
    {:else if $leagues.error}
        {$leagues.error}
    {:else}
        <ul>
            {#each $leagues.data.searchLeagues as league (league.id)}
                <li>{league.name}</li>
            {:else}
                <li>No league found</li>
            {/each}
        </ul>
    {/if}
</div>

<style></style>