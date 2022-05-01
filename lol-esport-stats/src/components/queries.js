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

const LEAGUE_FRAGMENT = gql`
	fragment LeagueFragment on League {
		id
		slug
		name
		region
	}
`;

const TEAM_FRAGMENT = gql`
	fragment TeamFragment on Team {
		id
		slug
		name
	}
`;

const PLAYER_FRAGMENT = gql`
	fragment PlayerFragment on Player {
		id
		riot_id
		summoner_name
	}
`;

const SEARCH_LEAGUES = gql`
	${LEAGUE_FRAGMENT}
	query SearchLeagues($search: String) {
		searchLeagues(search: $search) {
			...LeagueFragment
		}
	}
`;

const SEARCH_TEAMS = gql`
	${TEAM_FRAGMENT}
	query SearchTeams($search: String) {
		searchTeams(search: $search) {
			...TeamFragment
		}
	}
`;

const SEARCH_PLAYERS = gql`
	${PLAYER_FRAGMENT}
	query SearchPlayers($search: String) {
		searchPlayers(search: $search) {
			...PlayerFragment
		}
	}
`;

export const SEARCH_ALL = gql`
	${LEAGUE_FRAGMENT}
	${TEAM_FRAGMENT}
	${PLAYER_FRAGMENT}
	query SearchAll($search: String) {
		searchLeagues(search: $search) {
			...LeagueFragment
		}
		searchTeams(search: $search) {
			...TeamFragment
		}
		searchPlayers(search: $search) {
			...PlayerFragment
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

const PLAYER_MATCHES = gql`
	query PlayerMatches($player: String!) {
		playerMatches(player: $player) {
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

const TOURNAMENTS_BY_SLUGS = gql`
	query TournamentsBySlugs($slugs: [String]!) {
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

export {
	GET_ALL_LEAGUES,
	SEARCH_LEAGUES,
	SEARCH_TEAMS,
	SEARCH_PLAYERS,
	LEAGUE_MATCHES,
	TEAM_MATCHES,
	PLAYER_MATCHES,
	TOURNAMENTS_BY_SLUGS
};
