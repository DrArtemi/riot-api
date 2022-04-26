<script>
    import SearchSuggest from './SearchSuggest.svelte';
    
    export let search_input = "";
    export let leagues;
    export let teams;
</script>

<input class="search-input "type="text" bind:value={search_input} placeholder="Player, Team, Tournament..." />
{#if search_input}
    <div class="search-suggest">
        <SearchSuggest
            search_data={[
                { category: "Leagues", data: $leagues.data ? $leagues.data.searchLeagues : [] },
                { category: "Teams", data: $teams.data ? $teams.data.searchTeams : [] }
            ]}
        />
    </div>
{/if}

<style>
    .search-input {
        width: 100%;
        outline: none;
        border: none;
        padding: .5rem .25rem;
        font-size: 1rem;
    }

    .search-suggest {
        padding-top: 1rem;
        border-top: 1px solid #eceff1;
    }
</style>