import { nonNull, objectType, extendType, intArg, list, enumType, stringArg } from 'nexus'

export const Champion = objectType({
	name: 'Champion',
	definition(t) {
		t.nonNull.id('id', { description: 'The player unique ID' })
        t.nonNull.string('riot_id')
		t.nonNull.string('summoner_name')
		t.nonNull.string('first_name')
		t.nonNull.string('last_name')
        t.nonNull.string('image')
        t.nonNull.string('role')
        t.list.nonNull.field('teams', { type: Team })

		t.nonNull.int('BE')
		t.nonNull.int('RP')
		t.list.nonNull.field('attributes', { type: ChampionAttribute })
		t.nonNull.string('resource')
		t.nonNull.float('health')
		t.nonNull.int('HPLevel')
		t.nonNull.float('HPRegen')
		t.nonNull.float('HPRegenLevel')
	}
})

// riot_id         String?      @unique @db.VarChar(50)
//   summoner_name   String?      @db.VarChar(50)
//   first_name      String?      @db.VarChar(50)
//   last_name       String?      @db.VarChar(50)
//   image           String?      @db.VarChar(150)
//   role            String?      @db.VarChar(50)
//   current_team_id Int
//   teams           teams        @relation(fields: [current_team_id], references: [id], onDelete: NoAction, onUpdate: NoAction)
//   PlayerTeam      PlayerTeam[]

export const PlayerQuery = extendType({
	type: 'Query',
	definition(t) {
		t.field('playerById', {
			type: 'Player',
			args: {
				uid: nonNull(intArg())
			},
			resolve: (_root, { id }, ctx) => ctx.db.players.findUnique({ where: { id } })
		})
	}
})

export const PlayerQuery = extendType({
	type: 'Query',
	definition(t) {
		t.field('playerById', {
			type: 'Player',
			args: {
				uid: nonNull(intArg())
			},
			resolve: (_root, { id }, ctx) => ctx.db.players.findUnique({ where: { id } })
		})
	}
})