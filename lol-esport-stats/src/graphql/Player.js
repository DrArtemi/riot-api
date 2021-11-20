import { nonNull, objectType, extendType, intArg, list, enumType, stringArg } from 'nexus'

export const Players = objectType({
	name: 'Player',
	definition(t) {
		t.nonNull.id('id', { description: 'The player unique ID' })
        t.nonNull.string('riot_id')
		t.nonNull.string('summoner_name')
		t.nonNull.string('first_name')
		t.nonNull.string('last_name')
        t.nonNull.string('image')
        t.nonNull.string('role')
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
			resolve: (_root, { id }, ctx) => ctx.db.players.findUnique({ where: { id } })
		})
	}
})

export const PlayersQuery = extendType({
	type: 'Query',
	definition(t) {
		t.field('allPlayers', {
			type: list('Player'),
			resolve: (_root, _, ctx) => ctx.db.players.findMany()
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
			resolve: (_root, { name }, ctx) => ctx.db.players.findUnique({ where: { name } })
		})
	}
})