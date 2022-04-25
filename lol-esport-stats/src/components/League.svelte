<script>
    import { page } from '$app/stores'
    import MatchList from '../components/MatchList.svelte';
    import { query } from 'svelte-apollo';
    import { LEAGUE_MATCHES } from '../components/queries';

    export let slug;

    const matches = query(LEAGUE_MATCHES, {
        variables: { "league": slug }
    });
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