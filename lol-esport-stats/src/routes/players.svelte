<script>
    import { page } from '$app/stores';
    import { query } from 'svelte-apollo';
    import { PLAYER_MATCHES, TOURNAMENTS_BY_SLUGS } from '../components/queries';
    import SideBar from '../components/SideBar.svelte';
    import MatchList from '../components/MatchList.svelte';
    import MatchFilters from '../components/MatchFilters.svelte';

    const name = $page.query.get('name');
    const riot_id = $page.query.get('riot_id');
    let tournament_slugs = [];
    let tournaments_stages = {};
    let tournaments_filters = [];
    let stages_filters = [];

    const matches = query(PLAYER_MATCHES, {
        variables: { "player": riot_id }
    });
    $: matches.refetch({ "player": riot_id });
    matches.subscribe(result => {
        if (result.data) {
            tournament_slugs = [];
            for (const match of result.data.playerMatches)
                if (!tournament_slugs.includes(match.stage.tournament.slug))
                    tournament_slugs.push(match.stage.tournament.slug);
        }
    });
    const tournaments = query(TOURNAMENTS_BY_SLUGS, {
        variables: { "slugs": tournament_slugs }
    });
    $: tournaments.refetch({ "slugs": tournament_slugs });
    tournaments.subscribe(result => {
        if (result.data) {
            for (const tournament of result.data.tournamentsBySlugs) {
                tournaments_filters.push(tournament.slug);
                tournaments_stages[tournament.slug] = [];
                for (const stage of tournament.stages) {
                    stages_filters.push(stage.id);
                    tournaments_stages[tournament.slug].push(stage.id);
                }
            }
            tournaments_filters = [...tournaments_filters]; // C'est quand même fou de devoir faire ça fuck le js
            stages_filters = [...stages_filters]; // C'est quand même fou de devoir faire ça fuck le js
        }
    });
    const tabs = ["matches", "statistics"];
    let activeTab = 0;
</script>

<div class="pt-24 pb-2 px-4 h-full w-full flex flex-col">
    <div class="flex-initial w-full bg-slate-800/30 border-l-2 border-l-amber-400">
        <MatchFilters
            tournaments={tournaments}
            tournaments_stages={tournaments_stages}
            bind:tournaments_filters={tournaments_filters}
            bind:stages_filters={stages_filters}
        />
    </div>
    <div class="flex flex-row flex-1 min-h-0 mt-2 border-l-2 border-l-amber-400">
        <div class="w-64 bg-slate-800/30 flex-initial">
            <SideBar title={name} tabs={tabs} bind:activeTab={activeTab} />
        </div>
        <div class="w-full h-full ml-2 p-8 bg-slate-800/30 flex flex-col flex-1">
            {#if tabs[activeTab] == "matches"}
            <h2 class="text-slate-300 text-3xl mb-8 flex-initial">Match list</h2>
            <div class="text-slate-200 overflow-auto flex-1">
                {#if $matches.data}
                <MatchList
                    tournaments_filters={tournaments_filters}
                    stages_filters={stages_filters}
                    matches={$matches.data.playerMatches}
                />
                {:else}
                <p>No match found</p>
                {/if}
            </div>
            {:else if tabs[activeTab] == "statistics"}
            <p class="text-red-600">STATS</p>
            {/if}
        </div>
    </div>
</div>
