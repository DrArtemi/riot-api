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

const SEARCH_PLAYERS = gql`
    query SearchPlayers($search: String) {
        searchPlayers(search: $search) {
            id
            riot_id
            summoner_name
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
            stage {
                id
                name
                tournament {
                    slug
                }
            }
            team_1 {
                id
                name
                image
            }
            team_2 {
                id
                name
                image
            }
        }
    }
`;

const TEAM_MATCHES = gql`
    query TeamMatches($team: String!) {
        teamMatches(team: $team) {
            id
            riot_id
            date
            team_1_win
            team_2_win
            team_1 {
                id
                name
                image
            }
            team_2 {
                id
                name
                image
            }
        }
    }
`;

const PLAYER_MATCHES = gql`
    query PlayerMatches($player: String!) {
        playerMatches(player: $player) {
            id
            riot_id
            date
            team_1_win
            team_2_win
            team_1 {
                id
                name
                image
            }
            team_2 {
                id
                name
                image
            }
        }
    }
`;

const TOURNAMENTS_BY_SLUGS = gql`
    query TournamentsBySlugs($slugs: [String]!){
        tournamentsBySlugs(slugs: $slugs) {
            id
            slug
            stages {
                id
                name
            }
        }
    }
`;

export { GET_ALL_LEAGUES, SEARCH_LEAGUES, SEARCH_TEAMS, SEARCH_PLAYERS, LEAGUE_MATCHES, TEAM_MATCHES, PLAYER_MATCHES, TOURNAMENTS_BY_SLUGS };