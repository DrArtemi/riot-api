<script>
    import * as moment from 'moment';

    export let matches;
    export let tournaments_filters;
    export let stages_filters;
</script>

<table class="text-left border-collapse w-full bg-slate-900">
    <thead>
        <tr>
            <th class="sticky z-10 top-0 p-0 bg-slate-900 text-slate-300"><div class="py-2 pl-4 pr-2 border-b border-amber-400/40">Tournament</div></th>
            <th class="sticky z-10 top-0 p-0 bg-slate-900 text-slate-300"><div class="py-2 pr-2 border-b border-amber-400/40">Stage</div></th>
            <th class="sticky z-10 top-0 p-0 bg-slate-900 text-slate-300"><div class="py-2 pr-2 border-b border-amber-400/40">Date</div></th>
            <th class="sticky z-10 top-0 p-0 bg-slate-900 text-center text-slate-300"><div class="py-2 pr-2 border-b border-amber-400/40">Blue side</div></th>
            <th class="sticky z-10 top-0 p-0 bg-slate-900 text-center text-slate-300"><div class="py-2 pr-2 border-b border-amber-400/40">Red side</div></th>
            <th class="sticky z-10 top-0 p-0 bg-slate-900 text-center text-slate-300"><div class="py-2 pr-2 border-b border-amber-400/40">Link</div></th>
        </tr>
    </thead>
    <tbody>
        {#each matches as match (match.id)}
        <!-- <p>{match.stage.tournament.slug} {tournaments_filters}</p>
        <p>{match.stage.id} {stages_filters}</p> -->
        {#if tournaments_filters.includes(match.stage.tournament.slug) && stages_filters.includes(match.stage.id)}
        <tr>
            <td class="w-1 whitespace-nowrap text-slate-200 capitalize py-2 pl-4 pr-4 border-t border-slate-400/10">{match.stage.tournament.slug.replaceAll('_', ' ')}</td>
            <td class="w-1 whitespace-nowrap text-slate-200 py-2 pr-4 border-t border-slate-400/10">{match.stage.name}</td>
            <td class="text-slate-200 py-2 pr-2 border-t border-slate-400/10">{moment(match.date).format('DD-MMM-YYYY')}</td>
            <td class="py-2 pr-2 border-t border-slate-400/10"><img class="mx-auto h-12 w-12 p-1 rounded-full" class:bg-sky-300="{match.team_1_win}" class:bg-red-300="{!match.team_1_win}" src="{match.team_1.image}" alt="{match.team_1.name}"></td>
            <td class="py-2 pr-2 border-t border-slate-400/10"><img class="mx-auto h-12 w-12 p-1 rounded-full" class:bg-sky-300="{match.team_2_win}" class:bg-red-300="{!match.team_2_win}" src="{match.team_2.image}" alt="{match.team_2.name}"></td>
            <td class="text-sm text-slate-200 py-2 pr-2 border-t border-slate-400/10">
                <a href="https://feed.lolesports.com/livestats/v1/details/{parseInt(match.riot_id) + 1}" target="_blank">
                    <svg class="mx-auto" width="24" height="24" viewBox="-3 -3 30 30" xmlns="http://www.w3.org/2000/svg" fill-rule="evenodd" clip-rule="evenodd"><path fill="currentColor" d="M14.851 11.923c-.179-.641-.521-1.246-1.025-1.749-1.562-1.562-4.095-1.563-5.657 0l-4.998 4.998c-1.562 1.563-1.563 4.095 0 5.657 1.562 1.563 4.096 1.561 5.656 0l3.842-3.841.333.009c.404 0 .802-.04 1.189-.117l-4.657 4.656c-.975.976-2.255 1.464-3.535 1.464-1.28 0-2.56-.488-3.535-1.464-1.952-1.951-1.952-5.12 0-7.071l4.998-4.998c.975-.976 2.256-1.464 3.536-1.464 1.279 0 2.56.488 3.535 1.464.493.493.861 1.063 1.105 1.672l-.787.784zm-5.703.147c.178.643.521 1.25 1.026 1.756 1.562 1.563 4.096 1.561 5.656 0l4.999-4.998c1.563-1.562 1.563-4.095 0-5.657-1.562-1.562-4.095-1.563-5.657 0l-3.841 3.841-.333-.009c-.404 0-.802.04-1.189.117l4.656-4.656c.975-.976 2.256-1.464 3.536-1.464 1.279 0 2.56.488 3.535 1.464 1.951 1.951 1.951 5.119 0 7.071l-4.999 4.998c-.975.976-2.255 1.464-3.535 1.464-1.28 0-2.56-.488-3.535-1.464-.494-.495-.863-1.067-1.107-1.678l.788-.785z"/></svg>
                </a>
            </td>
        </tr>
        {/if}
        {/each}
    </tbody>
</table>
<div class="sticky bottom-0 h-px -mt-px bg-amber-400/40"></div>
