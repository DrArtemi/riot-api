<script>
    import { page } from '$app/stores'
    import { query } from 'svelte-apollo';
    import * as moment from 'moment';
    import { LEAGUE_MATCHES } from '../components/queries';

    const league_slug = $page.query.get('slug');

    const matches = query(LEAGUE_MATCHES, {
        variables: { "league": league_slug }
    });
</script>

{#if $matches.data}
    {#each $matches.data.leagueMatches as match (match.id)}
        <p>{match.riot_id} ({moment(match.date).format('DD-MMM-YYYY HH:mm')}): {match.team_1.name} ({match.team_1_win}) vs {match.team_2.name} ({match.team_2_win})</p>
    {/each}
{:else}
    <p>No match found</p>
{/if}
