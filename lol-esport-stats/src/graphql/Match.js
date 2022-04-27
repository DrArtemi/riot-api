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

export const TeamMatchesQuery = extendType({
	type: 'Query',
	definition(t) {
		t.field('teamMatches', {
			type: list('Match'),
			args: {
				team: stringArg()
			},
			resolve: (_root, { team }, ctx) => {
				if (!team)
					return [];
				return ctx.db.matches.findMany({
                    orderBy: {
                        date: 'desc',
                    },
					where: {
						OR: [
							{
								team_1: {
									slug: {
										equals: team
									}
								}
							},
							{
								team_2: {
									slug: {
										equals: team
									}
								}
							}
						],
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

export const PlayerMatchesQuery = extendType({
	type: 'Query',
	definition(t) {
		t.field('playerMatches', {
			type: list('Match'),
			args: {
				player: stringArg()
			},
			resolve: (_root, { player }, ctx) => {
				if (!player)
					return [];
				return ctx.db.matches.findMany({
                    orderBy: {
                        date: 'desc',
                    },
					where: {
						OR: [
							{
								team_1: {
									current_players: {
										some: {
											riot_id: {
												equals: player
											}
										}
									}
								}
							},
							{
								team_2: {
									current_players: {
										some: {
											riot_id: {
												equals: player
											}
										}
									}
								}
							}
						],
                        NOT: {
                            date: null
                        }
					},
                    include: {
                        team_1: {
							include: {
								current_players: true,
							}
						},
                        team_2: {
							include: {
								current_players: true,
							}
						},
                    }
				})
			}
		})
	}
})