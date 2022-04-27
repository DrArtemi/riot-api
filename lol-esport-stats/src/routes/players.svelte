<script>
    import MatchList from '../components/MatchList.svelte';
    import { page } from '$app/stores';
    import { query } from 'svelte-apollo';
    import { PLAYER_MATCHES } from '../components/queries';

    const name = $page.query.get('name');
    const riot_id = $page.query.get('riot_id');

    const matches = query(PLAYER_MATCHES, {
        variables: { "player": riot_id }
    });
</script>

<div class="mt-32 px-8">
    <h1 class="text-4xl mb-8 capitalize text-slate-400">{name}</h1>
    <div class="content text-slate-200 max-h-96 w-1/3 overflow-auto">
    {#if $matches.data}
        <MatchList matches={$matches.data.playerMatches} />
    {:else}
        <p>No match found</p>
    {/if}
    </div>
</div>
