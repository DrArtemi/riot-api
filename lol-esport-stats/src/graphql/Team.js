import { nonNull, objectType, extendType, intArg, list, enumType, stringArg } from 'nexus';
import { Player } from './Player';
import { League } from './League';
import { Match } from './Match';

export const Team = objectType({
	name: 'Team',
	definition(t) {
		t.nonNull.id('id', { description: 'The team unique ID' });
		t.nonNull.string('riot_id');
		t.nonNull.string('slug');
		t.nonNull.string('code');
		t.nonNull.string('name');
		t.string('image');
		t.string('alt_image');
		t.string('bg_image');
		t.string('status');
		t.field('league', { type: League });
		t.list.nonNull.field('current_players', { type: Player });
		t.list.nonNull.field('players', { type: Player });
		t.list.field('matches_team_1', { type: Match });
		t.list.field('matches_team_2', { type: Match });
	}
});

export const TeamQuery = extendType({
	type: 'Query',
	definition(t) {
		t.field('teamById', {
			type: 'Team',
			args: {
				id: nonNull(intArg())
			},
			resolve: (_root, { id }, ctx) =>
				ctx.db.teams.findUnique({
					where: { id },
					include: {
						current_players: true
					}
				})
		});
	}
});

export const TeamsQuery = extendType({
	type: 'Query',
	definition(t) {
		t.field('allTeams', {
			type: list('Team'),
			resolve: (_root, _, ctx) =>
				ctx.db.teams.findMany({
					include: {
						current_players: true
					}
				})
		});
	}
});

export const TeamSlugQuery = extendType({
	type: 'Query',
	definition(t) {
		t.field('teamBySlug', {
			type: 'Team',
			args: {
				slug: nonNull(stringArg())
			},
			resolve: (_root, { slug }, ctx) =>
				ctx.db.teams.findMany({
					where: { slug: { equals: slug } },
					include: {
						current_players: true
					}
				})
		});
	}
});

export const SearchTeamsQuery = extendType({
	type: 'Query',
	definition(t) {
		t.field('searchTeams', {
			type: list('Team'),
			args: {
				search: stringArg()
			},
			resolve: (_root, { search }, ctx) => {
				if (!search) return [];
				return ctx.db.teams.findMany({
					where: {
						name: {
							contains: search,
							mode: 'insensitive'
						}
					},
					include: {
						current_players: true
					}
				});
			}
		});
	}
});
