<script>
    import MatchList from '../components/MatchList.svelte';
    import { page } from '$app/stores';
    import { query } from 'svelte-apollo';
    import { TEAM_MATCHES } from '../components/queries';

    const slug = $page.query.get('slug');

    const matches = query(TEAM_MATCHES, {
        variables: { "team": slug }
    });
</script>

<div class="mt-32 px-8">
    <h1 class="text-4xl mb-8 capitalize text-slate-400">{slug}</h1>
    <div class="content text-slate-200 max-h-96 w-1/3 overflow-auto">
    {#if $matches.data}
        <MatchList matches={$matches.data.teamMatches} />
    {:else}
        <p>No match found</p>
    {/if}
    </div>
</div>
