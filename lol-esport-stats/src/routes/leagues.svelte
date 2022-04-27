<script>
    import MatchList from '../components/MatchList.svelte';
    import { page } from '$app/stores';
    import { query } from 'svelte-apollo';
    import { LEAGUE_MATCHES } from '../components/queries';

    const slug = $page.query.get('slug');

    const matches = query(LEAGUE_MATCHES, {
        variables: { "league": slug }
    });
</script>

<div class="mt-32 px-8">
    <h1 class="text-4xl mb-8 capitalize text-slate-400">{slug}</h1>
    <div class="content text-slate-200 max-h-96 w-1/3 overflow-auto">
    {#if $matches.data}
        <MatchList matches={$matches.data.leagueMatches} />
    {:else}
        <p>No match found</p>
    {/if}
    </div>
</div>
