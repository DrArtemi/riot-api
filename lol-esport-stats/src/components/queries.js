import { gql } from '@apollo/client/core';

const GET_ALL_LEAGUES = gql`
    {
        allLeagues {
            id
            slug
            name
            region
        }
    }
`;

const SEARCH_LEAGUES = gql`
    query SearchLeagues($search: String) {
        searchLeagues(search: $search) {
            id
            slug
            name
            region
        }
    }
`;

const SEARCH_TEAMS = gql`
    query SearchTeams($search: String) {
        searchTeams(search: $search) {
            id
            slug
            name
        }
    }
`;

const LEAGUE_MATCHES = gql`
    query LeagueMatches($league: String!) {
        leagueMatches(league: $league) {
            id
            riot_id
            date
            team_1_win
            team_2_win
            team_1 {
                id
                name
            }
            team_2 {
                id
                name
            }
        }
    }
`;



export { GET_ALL_LEAGUES, SEARCH_LEAGUES, SEARCH_TEAMS, LEAGUE_MATCHES };