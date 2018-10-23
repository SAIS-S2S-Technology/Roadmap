import random
import sc2
from sc2 import run_game, maps, Race, Difficulty
from sc2.player import Bot, Computer
from sc2.constants import SCV, COMMANDCENTER, SUPPLYDEPOT, REFINERY, BARRACKS, MARINE, FACTORY, CYCLONE

class CapsBot(sc2.BotAI):
    async def on_step(self, iteration):
        await self.distribute_workers()
        await self.build_workers()
        await self.build_supplydepot()
        await self.build_refinery()
        await self.build_barracks()
        await self.build_marines()
        await self.build_factory()
        await self.build_cyclones()
        await self.attack()

    async def build_workers(self):
        for cc in self.units(COMMANDCENTER).ready.noqueue: #  cc has to be ready and not producing sth else
            if self.can_afford(SCV) and self.units(SCV).amount < 80:
                await self.do(cc.train(SCV))

    async def build_supplydepot(self):
        if self.supply_left < 8 and not self.already_pending(SUPPLYDEPOT) and self.can_afford(SUPPLYDEPOT):
            if self.units(SUPPLYDEPOT).amount == 0:
                near = self.units(COMMANDCENTER).first
                await self.build(SUPPLYDEPOT, near)
            else:
                near = self.units(SUPPLYDEPOT)[(self.units(SUPPLYDEPOT).amount - 1)]
                await self.build(SUPPLYDEPOT, near)

    async def build_refinery(self):
        vgs = self.state.vespene_geyser.closer_than(10.0, self.units(COMMANDCENTER).first)
        for vg in vgs:
            if not self.can_afford(REFINERY):
                break
            worker = self.select_build_worker(vg.position)
            if worker is None:
                break
            if not self.units(REFINERY).closer_than(1.0, vg).exists:
                await self.do(worker.build(REFINERY, vg))

    async def build_barracks(self):
        if self.can_afford(BARRACKS) and self.units(BARRACKS).amount < 2:
            await self.build(BARRACKS, near=self.units(COMMANDCENTER).first)

    async def build_marines(self):
        for rax in self.units(BARRACKS):
            if rax.is_ready and rax.noqueue:
                if self.can_afford(MARINE) and self.units(MARINE).amount < 40:
                    await self.do(rax.train(MARINE))

    async def build_factory(self):
        if self.units(BARRACKS).amount > 0:
            if self.can_afford(FACTORY) and self.units(FACTORY).amount < 1 and not self.already_pending(FACTORY):
                await self.build(FACTORY, near=self.units(BARRACKS).first)

    async def build_cyclones(self):
        for fact in self.units(FACTORY):
            if fact.is_ready and fact.noqueue:
                if self.can_afford(CYCLONE) and self.units(CYCLONE).amount < 12:
                    await self.do(fact.train(CYCLONE))

    def locate_target(self, state):
        if len(self.known_enemy_units) > 0:
            return random.choice(self.known_enemy_units)
        elif len(self.known_enemy_structures) > 0:
            return random.choice(self.known_enemy_structures)
        else:
            return self.enemy_start_locations[0]

    async def attack(self):
        # if self.units(MARINE).amount > 5:
        #     if len(self.known_enemy_units) > 0:
        #         for m in self.units(MARINE).idle:
        #             await self.do(m.attack(random.choice(self.known_enemy_units)))

        if self.units(MARINE).amount > 20 and self.units(CYCLONE).amount > 4:
            for m in self.units(MARINE).idle:
                await self.do(m.attack(self.locate_target(self.state)))
            for c in self.units(CYCLONE).idle:
                await self.do(c.attack(self.locate_target(self.state)))

run_game(maps.get("CatalystLE"), [
    Bot(Race.Terran, CapsBot()),
    Computer(Race.Protoss, Difficulty.Hard)
    ], realtime = False)
