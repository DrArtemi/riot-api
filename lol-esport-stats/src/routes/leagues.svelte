<script>
    import MatchList from '../components/MatchList.svelte';
    import { page } from '$app/stores';
    import { query } from 'svelte-apollo';
    import { LEAGUE_MATCHES, TOURNAMENTS_BY_SLUGS } from '../components/queries';
    import SideBar from '../components/SideBar.svelte';

    const slug = $page.query.get('slug');
    let tournament_slugs = [];
    let tournaments_stages = {};
    let tournaments_filters = [];
    let stages_filters = [];

    const matches = query(LEAGUE_MATCHES, {
        variables: { "league": slug }
    });
    $: matches.refetch({ "league": slug });
    matches.subscribe(result => {
        if (result.data) {
            tournament_slugs = [];
            for (const match of result.data.leagueMatches)
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

    let showFilters = false;
    function toggleFilters(e) {
        showFilters = !showFilters;
    }

    function updateTournamentFilter(e) {
        if (!e.target.checked)
            stages_filters = stages_filters.filter(el => !tournaments_stages[e.target.value].includes(el))
        else
            for (const stage_id of tournaments_stages[e.target.value])
                if (!stages_filters.includes(stage_id))
                    stages_filters.push(stage_id);
            stages_filters = [...stages_filters]; // C'est quand même fou de devoir faire ça fuck le js
    }

    function updateStageFilter(e) {
        if (e.target.checked) {
            for (const tournament in tournaments_stages)
                if (tournaments_stages[tournament].includes(e.target.value) && !tournaments_filters.includes(tournament))
                    tournaments_filters.push(tournament);
            tournaments_filters = [...tournaments_filters]; // C'est quand même fou de devoir faire ça fuck le js
        }
    }
</script>

<div class="pt-32 pb-8 px-8 h-full w-full flex flex-col">
    <div class="flex-initial w-full bg-slate-800/30 border-l-2 border-l-amber-400">
        <h2 on:click={toggleFilters} class="text-slate-300 text-3xl w-full cursor-pointer hover:bg-slate-700 p-4">Filters</h2>
        {#if $tournaments.data}
        <div class="{showFilters ? '' : 'hidden'} px-4 pb-4">
            {#each $tournaments.data.tournamentsBySlugs as tournament}
            <div class="mt-4">
                <label class="custom-box relative cursor-pointer capitalize text-slate-300 pl-6">
                    {tournament.slug.replaceAll('_', ' ')}
                    <input on:change={updateTournamentFilter} class="hidden" bind:group={tournaments_filters} type="checkbox" value={tournament.slug}>
                    <span class="checkmark absolute top-0 left-0 h-4 w-4 bg-slate-700 rounded-sm"></span>
                </label>
                {#if tournament.stages.length > 0}
                <div class="pl-6 mt-2">
                    {#each tournament.stages as stage, i}
                    <label class="custom-box relative cursor-pointer capitalize text-slate-300 pl-6 {i !== 0 ? 'ml-4' : ''}">
                        {stage.name}
                        <input on:change={updateStageFilter} class="hidden" bind:group={stages_filters} type="checkbox" value={stage.id}>
                        <span class="checkmark absolute top-0 left-0 h-4 w-4 bg-slate-700 rounded-sm"></span>
                    </label>
                    {/each}
                </div>
                {/if}
            </div>
            {/each}
        </div>
        {/if}
    </div>
    <div class="h-full flex flex-row flex-auto mt-2 border-l-2 border-l-amber-400">
        <div class="w-64 bg-slate-800/30 flex-initial">
            <SideBar title={slug} tabs={tabs} bind:activeTab={activeTab} />
        </div>
        <div class="w-full h-full ml-2 p-8 bg-slate-800/30 flex flex-col flex-1">
            {#if tabs[activeTab] == "matches"}
            <h2 class="text-slate-300 text-3xl mb-8 flex-initial">Match list</h2>
            <div class="text-slate-200 overflow-auto flex-1">
                {#if $matches.data}
                <MatchList
                    tournaments_filters={tournaments_filters}
                    stages_filters={stages_filters}
                    matches={$matches.data.leagueMatches}
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

<style>
    .custom-box .checkmark:after {
        content: "";
        position: absolute;
        display: none;
    }

    .custom-box input:checked + .checkmark:after {
        display: block;
    }

    .custom-box .checkmark:after {
        left: 6px;
        top: 3px;
        width: 5px;
        height: 10px;
        border: solid white;
        border-width: 0 3px 3px 0;
        -webkit-transform: rotate(45deg);
        -ms-transform: rotate(45deg);
        transform: rotate(45deg);
    }
</style>