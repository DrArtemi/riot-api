<script>
    import MatchList from '../components/MatchList.svelte';

    export let slug;
    export let matches;
</script>

<h1 class="title">{slug} matches</h1>
<div class="content">
{#if $matches.data}
    <MatchList matches={$matches.data.leagueMatches} />
{:else}
    <p>No match found</p>
{/if}
</div>

<style>
    .title {
        color: #263238;
        margin-bottom: 1rem;
    }

    .title::first-letter {
        text-transform: capitalize;
    }
</style>