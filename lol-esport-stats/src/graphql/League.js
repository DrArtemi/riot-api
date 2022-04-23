import { nonNull, objectType, extendType, intArg, list, stringArg } from 'nexus'
import { Tournament } from './Tournament'
import { Team } from './Team'

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
		t.list.nonNull.field('teams', { type: Team })
		t.list.nonNull.field('tournaments', { type: Tournament })
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
			resolve: (_root, { id }, ctx) => ctx.db.leagues.findUnique({
				where: { id },
				include: {
					tournaments: true
				}
			})
		})
	}
})

export const LeaguesQuery = extendType({
	type: 'Query',
	definition(t) {
		t.field('allLeagues', {
			type: list('League'),
			resolve: (_root, _, ctx) => ctx.db.leagues.findMany({
				include: {
					tournaments: true
				}
			})
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
			resolve: (_root, { slug }, ctx) => ctx.db.leagues.findFirst({
				where: { slug },
				include: {
					tournaments: true
				}
			})
		})
	}
})

export const SearchLeaguesQuery = extendType({
	type: 'Query',
	definition(t) {
		t.field('searchLeagues', {
			type: list('League'),
			args: {
				search: stringArg()
			},
			resolve: (_root, { search }, ctx) => {
				console.log(search);
				if (!search)
					return ctx.db.leagues.findMany({
						include: {
							tournaments: true
						}
					});
				return ctx.db.leagues.findMany({
					where: {
						name: {
							contains: search,
							mode: 'insensitive',
						}
					},
					include: {
						tournaments: true
					}
				})
			}
		})
	}
})