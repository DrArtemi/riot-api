import { nonNull, objectType, extendType, intArg, list, enumType, stringArg } from 'nexus'

export const Team = objectType({
	name: 'Team',
	definition(t) {
		t.nonNull.id('id', { description: 'The team unique ID' })
        t.nonNull.string('riot_id')
		t.nonNull.string('slug')
		t.nonNull.string('code')
        t.nonNull.string('name')
		t.nonNull.string('image')
		t.nonNull.string('alt_image')
        t.nonNull.string('bg_image')
		t.nonNull.string('status')
	}
})

export const TeamQuery = extendType({
	type: 'Query',
	definition(t) {
		t.field('teamById', {
			type: 'Team',
			args: {
				id: nonNull(intArg())
			},
			resolve: (_root, { id }, ctx) => ctx.db.teams.findUnique({ where: { id } })
		})
	}
})

export const TeamsQuery = extendType({
	type: 'Query',
	definition(t) {
		t.field('allTeams', {
			type: list('Team'),
			resolve: (_root, _, ctx) => ctx.db.teams.findMany()
		})
	}
})

export const TeamSlugQuery = extendType({
	type: 'Query',
	definition(t) {
		t.field('teamBySlug', {
			type: 'Team',
			args: {
				slug: nonNull(stringArg())
			},
			resolve: (_root, { slug }, ctx) => ctx.db.teams.findUnique({ where: { slug } })
		})
	}
})