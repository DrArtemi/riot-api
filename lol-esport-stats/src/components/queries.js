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
            name
            region
        }
    }
`;

const SEARCH_TEAMS = gql`
    query SearchTeams($search: String) {
        searchTeams(search: $search) {
            id
            name
        }
    }
`;


export { GET_ALL_LEAGUES, SEARCH_LEAGUES, SEARCH_TEAMS };