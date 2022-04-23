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

export { GET_ALL_LEAGUES, SEARCH_LEAGUES };