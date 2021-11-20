import { nonNull, objectType, extendType, intArg, list, scalarType, stringArg } from 'nexus'

const DateScalar = scalarType({
	name: 'Date',
	asNexusMethod: 'date',
	description: 'Date custom scalar type',
	parseValue(value) {  
		return new Date(value)
	},
	serialize(value) {
		return value.getTime()
	},
	parseLiteral(ast) {
	  	if (ast.kind === Kind.INT) {
			return new Date(ast.value)
	  	}
	  	return null
	},
})

export const Tournament = objectType({
	name: 'Tournament',
	definition(t) {
		t.nonNull.id('id', { description: 'The tournament unique ID' })
        t.nonNull.string('riot_id')
		t.nonNull.string('slug')
		t.nonNull.field('start_date', { type: DateScalar })
        t.nonNull.field('end_date', { type: DateScalar })
	}
})

export const TournamentQuery = extendType({
	type: 'Query',
	definition(t) {
		t.field('tournamentById', {
			type: 'Tournament',
			args: {
				id: nonNull(intArg())
			},
			resolve: (_root, { id }, ctx) => ctx.db.tournaments.findUnique({ where: { id } })
		})
	}
})

export const TournamentsQuery = extendType({
	type: 'Query',
	definition(t) {
		t.field('allTournaments', {
			type: list('Tournament'),
			resolve: (_root, _, ctx) => ctx.db.tournaments.findMany()
		})
	}
})

export const TournamentSlugQuery = extendType({
	type: 'Query',
	definition(t) {
		t.field('tournamentBySlug', {
			type: 'Tournament',
			args: {
				slug: nonNull(stringArg())
			},
			resolve: (_root, { slug }, ctx) => ctx.db.tournaments.findUnique({ where: { slug } })
		})
	}
})