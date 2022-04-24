import { nonNull, objectType, extendType, intArg, list, stringArg } from 'nexus'
import { Team } from './Team'
import { DateScalar } from './Tournament'

export const Match = objectType({
	name: 'Match',
	definition(t) {
		t.nonNull.id('id', { description: 'The match unique ID' })
        t.nonNull.string('riot_id')
        t.field('date', { type: DateScalar })
		t.nonNull.string('state')
		t.string('final_state')
		t.string('evolution')
        t.nonNull.boolean('team_1_id')
        t.nonNull.boolean('team_2_id')
        t.nonNull.boolean('team_1_win')
        t.nonNull.boolean('team_2_win')
        t.field('team_1', { type: Team })
        t.field('team_2', { type: Team })
	}
})

export const MatchQuery = extendType({
	type: 'Query',
	definition(t) {
		t.field('matchById', {
			type: 'Match',
			args: {
				id: nonNull(intArg())
			},
			resolve: (_root, { id }, ctx) => ctx.db.matches.findUnique({
				where: { id }
			})
		})
	}
})

export const MatchesQuery = extendType({
	type: 'Query',
	definition(t) {
		t.field('allMatchs', {
			type: list('Match'),
			resolve: (_root, _, ctx) => ctx.db.matches.findMany()
		})
	}
})

export const MatchByRiotIdQuery = extendType({
	type: 'Query',
	definition(t) {
		t.field('matchByRiotId', {
			type: 'Match',
			args: {
				riot_id: nonNull(stringArg())
			},
			resolve: (_root, { riot_id }, ctx) => ctx.db.leagues.findFirst({
				where: { riot_id }
			})
		})
	}
})

export const LeagueMatchesQuery = extendType({
	type: 'Query',
	definition(t) {
		t.field('leagueMatches', {
			type: list('Match'),
			args: {
				league: stringArg()
			},
			resolve: (_root, { league }, ctx) => {
				if (!league)
					return [];
				return ctx.db.matches.findMany({
                    orderBy: {
                        date: 'desc',
                    },
					where: {
						stage: {
                            tournament: {
                                league: {
                                    slug: {
                                        equals: league
                                    }
                                }
                            }
						},
                        NOT: {
                            date: null
                        }
					},
                    include: {
                        team_1: true,
                        team_2: true
                    }
				})
			}
		})
	}
})