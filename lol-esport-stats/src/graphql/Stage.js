import { nonNull, objectType, extendType, intArg, list, enumType, stringArg } from 'nexus'
import { Tournament } from './Tournament'

export const Stage = objectType({
	name: 'Stage',
	definition(t) {
		t.nonNull.id('id', { description: 'The stage unique ID' })
        t.nonNull.string('slug')
		t.nonNull.string('name')
		t.nonNull.string('type')
		t.nonNull.field('tournament', { type: Tournament })
	}
})

export const StageQuery = extendType({
	type: 'Query',
	definition(t) {
		t.field('stageById', {
			type: 'Stage',
			args: {
				id: nonNull(intArg())
			},
			resolve: (_root, { id }, ctx) => ctx.db.stages.findUnique({
				where: { id },
				include: {
					matches: true
				}
			})
		})
	}
})

export const StagesQuery = extendType({
	type: 'Query',
	definition(t) {
		t.field('allStages', {
			type: list('Stage'),
			resolve: (_root, _, ctx) => ctx.db.stages.findMany({
				include: {
					matches: true
				}
			})
		})
	}
})

export const StageSlugQuery = extendType({
	type: 'Query',
	definition(t) {
		t.field('stageBySlug', {
			type: 'Stage',
			args: {
				slug: nonNull(stringArg())
			},
			resolve: (_root, { slug }, ctx) => ctx.db.stages.findUnique({
				where: { slug },
				include: {
					matches: true
				}
			})
		})
	}
})