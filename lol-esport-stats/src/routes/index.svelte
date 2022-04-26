<script>
    import Search from '../components/search/Search.svelte'
    import League from '../components/League.svelte';
    import { page } from '$app/stores'
    import { query } from 'svelte-apollo';
    import { SEARCH_LEAGUES, SEARCH_TEAMS, LEAGUE_MATCHES } from '../components/queries';

    const category = $page.query.get('category');
    const slug = $page.query.get('slug');

    let matches;

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

    $: if (category) {
        if (category == "leagues") {
            matches = query(LEAGUE_MATCHES, {
                variables: { "league": slug }
            });
        }
    }    
</script>

<div class="search-bar">
    <Search
        bind:search_input={search_input}
        leagues={leagues}
        teams={teams}
    />
</div>

{#if category}
<div class="content">
{#if matches}
    <League slug={slug} matches={matches}/>
{/if}
</div>
{/if}

<style>
    .search-bar {
        margin-left: auto;
        margin-right: auto;
        margin-top: 2rem;
        width: 80%;
        padding: .5rem 2rem;
        border-radius: 5px;
        box-shadow: 0rem 0rem .25rem #b0bec5;
    }

    .content {
        margin-left: auto;
        margin-right: auto;
        margin-top: 2rem;
        width: 80%;
        padding: .5rem 2rem;
        border-radius: 5px;
        box-shadow: 0rem 0rem .25rem #b0bec5;
    }
</style>