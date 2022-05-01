import { nonNull, objectType, extendType, intArg, list, scalarType, stringArg } from 'nexus'
import { Stage } from './Stage'
import { League } from './League'

export const DateScalar = scalarType({
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
		t.nonNull.field('league', { type: League })
		t.list.nonNull.field('stages', { type: Stage })
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
			resolve: (_root, { id }, ctx) => ctx.db.tournaments.findUnique({
				where: { id },
				include: {
					stages: true
				}
			})
		})
	}
})

export const TournamentsQuery = extendType({
	type: 'Query',
	definition(t) {
		t.field('allTournaments', {
			type: list('Tournament'),
			resolve: (_root, _, ctx) => ctx.db.tournaments.findMany({
				include: {
					stages: true
				}
			})
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
			resolve: (_root, { slug }, ctx) => ctx.db.tournaments.findUnique({
				where: { slug },
				include: {
					stages: true
				}
			})
		})
	}
})

export const TournamentsSlugsQuery = extendType({
	type: 'Query',
	definition(t) {
		t.field('tournamentsBySlugs', {
			type: list('Tournament'),
			args: {
				slugs: nonNull(list(stringArg()))
			},
			resolve: (_root, { slugs }, ctx) => ctx.db.tournaments.findMany({
				where: {
					slug: { in: slugs }
				},
				include: {
					stages: true
				}
			})
		})
	}
})