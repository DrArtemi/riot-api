<script>
    import * as moment from 'moment';

    export let matches;
</script>

<table>
    <thead class="match-list-header">
        <tr>
            <th class="align-left">Date</th>
            <th class="align-center">Blue side</th>
            <th class="align-center">Red side</th>
            <th class="align-left">Link</th>
        </tr>
    </thead>
    <tbody>
        {#each matches as match (match.id)}
        <tr>
            <td class="align-left">{moment(match.date).format('DD-MMM-YYYY')}</td>
            <td class="align-center"><img class="blue_team_img" class:win="{match.team_1_win}" src="{match.team_1.image}" alt="{match.team_1.name}"></td>
            <td class="align-center"><img class="red_team_img" class:win="{match.team_2_win}" src="{match.team_2.image}" alt="{match.team_2.name}"></td>
            <td class="align-left"><a href="https://feed.lolesports.com/livestats/v1/details/{parseInt(match.riot_id) + 1}" target="_blank">link</a></td>
        </tr>
        {/each}
    </tbody>
</table>

<style>
    .blue_team_img,
    .red_team_img {
        height: 2rem;
        width: 2rem;
        padding: .3rem;
        border-radius: 25px;
        background-color: #ffcdd2;
    }

    .blue_team_img.win,
    .red_team_img.win {
        background-color: #c5cae9;
    }

    th {
        color: #546e7a;
        padding-right: 2rem;
    }

    td {
        padding-right: 2rem;
    }

    .align-left {
        text-align: left;
    }

    .align-center {
        text-align: center;
    }
</style>