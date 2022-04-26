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

<div class="absolute left-8 w-11/12 top-8 mx-auto border-l-2 border-l-amber-400">
    <Search
        bind:search_input={search_input}
        leagues={leagues}
        teams={teams}
    />
</div>

{#if category && slug}
<div class="mt-32 px-8">
    <h1 class="text-4xl mb-8 capitalize text-slate-400">{slug}</h1>
    {#if matches}
        <League matches={matches}/>
    {/if}
</div>
{/if}
