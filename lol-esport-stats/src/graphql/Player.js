import { nonNull, objectType, extendType, intArg, list, enumType, stringArg } from 'nexus'
import { Team } from './Team'

export const Player = objectType({
	name: 'Player',
	definition(t) {
		t.nonNull.id('id', { description: 'The player unique ID' })
        t.nonNull.string('riot_id')
		t.nonNull.string('summoner_name')
		t.string('first_name')
		t.string('last_name')
        t.string('image')
        t.nonNull.string('role')
		t.nonNull.int('current_team_id')
		t.field('current_team', { type: Team })
		t.list.field('teams', { type: Team })
	}
})

export const PlayerQuery = extendType({
	type: 'Query',
	definition(t) {
		t.field('playerById', {
			type: 'Player',
			args: {
				id: nonNull(intArg())
			},
			resolve: (_root, { id }, ctx) => ctx.db.players.findUnique({
				where: { id },
				include: {
					current_team: true,
				}
			})
		})
	}
})

export const PlayersQuery = extendType({
	type: 'Query',
	definition(t) {
		t.field('allPlayers', {
			type: list('Player'),
			resolve: (_root, _, ctx) => ctx.db.players.findMany({
				include: {
					current_team: true,
				}
			})
		})
	}
})

export const PlayerNameQuery = extendType({
	type: 'Query',
	definition(t) {
		t.field('playerByName', {
			type: 'Player',
			args: {
				name: nonNull(stringArg())
			},
			resolve: (_root, { name }, ctx) => ctx.db.players.findUnique({
				where: { name },
				include: {
					current_team: true,
				}
			})
		})
	}
})