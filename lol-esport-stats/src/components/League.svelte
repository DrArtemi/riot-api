<script>
    import MatchList from '../components/MatchList.svelte';

    export let matches;
</script>

<div class="content text-slate-200 max-h-96 w-1/3 overflow-auto">
{#if $matches.data}
    <MatchList matches={$matches.data.leagueMatches} />
{:else}
    <p>No match found</p>
{/if}
</div>
