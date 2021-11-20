import { nonNull, objectType, extendType, intArg, list, stringArg } from 'nexus'

export const League = objectType({
	name: 'League',
	definition(t) {
		t.nonNull.id('id', { description: 'The league unique ID' })
        t.nonNull.string('riot_id')
		t.nonNull.string('slug')
		t.nonNull.string('name')
		t.nonNull.string('region')
        t.nonNull.string('image_url')
        t.nonNull.int('priority')
        t.nonNull.int('priority_position')
        t.nonNull.string('priority_status')
	}
})

export const LeagueQuery = extendType({
	type: 'Query',
	definition(t) {
		t.field('leagueById', {
			type: 'League',
			args: {
				id: nonNull(intArg())
			},
			resolve: (_root, { id }, ctx) => ctx.db.leagues.findUnique({ where: { id } })
		})
	}
})

export const LeaguesQuery = extendType({
	type: 'Query',
	definition(t) {
		t.field('allLeagues', {
			type: list('League'),
			resolve: (_root, _, ctx) => ctx.db.leagues.findMany()
		})
	}
})

export const LeagueBySlugQuery = extendType({
	type: 'Query',
	definition(t) {
		t.field('leagueBySlug', {
			type: 'League',
			args: {
				slug: nonNull(stringArg())
			},
			resolve: (_root, { slug }, ctx) => ctx.db.leagues.findFirst({ where: { slug } })
		})
	}
})