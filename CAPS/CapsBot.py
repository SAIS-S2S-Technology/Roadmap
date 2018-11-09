""" 
Terran bot that stays on 1 base, builds 2 barracks and 1 factory
Pushes into enemy base with min 20 marines and 5 cyclones
Repeats that push with same numbers if unsuccessful at first
First push takes place around 5:30 minute mark
Generally defeats hard AI in TvT, TvP and TvZ lineups

Bot made by Leo Klenner for CAPS workshop to explain rule-based agents
"""
import random
import sc2
from sc2 import run_game, maps, Race, Difficulty
from sc2.player import Bot, Computer
from sc2.constants import SCV, COMMANDCENTER, SUPPLYDEPOT, REFINERY, BARRACKS, MARINE, FACTORY, CYCLONE

class CapsBot(sc2.BotAI):  # CapsBot inherits methods from sc2.BotAI
    async def on_step(self, iteration):  # at every step of the game on_step controls what we want to do at that step
        await self.distribute_workers()  # defined in BotAI
        await self.build_workers()   # all remaining methods defined by us
        await self.build_supplydepot()
        await self.build_refinery()
        await self.build_barracks()
        await self.build_marines()
        await self.build_factory()
        await self.build_cyclones()
        await self.attack()
    
    # build workers (SCVs) through the COMMANDCENTER if we can afford a worker and the amount of workers is smaller than 80
    async def build_workers(self):
        for cc in self.units(COMMANDCENTER).ready.noqueue: #  cc has to be ready and not producing sth else
            if self.can_afford(SCV) and self.units(SCV).amount < 80:
                await self.do(cc.train(SCV))
                
    # build SUPPLYDEPOT to increase supply if we have less than 8 supply left, are not already building one and can afford one
    async def build_supplydepot(self):
        if self.supply_left < 8 and not self.already_pending(SUPPLYDEPOT) and self.can_afford(SUPPLYDEPOT):
            if self.units(SUPPLYDEPOT).amount == 0:
                near = self.units(COMMANDCENTER).first  # position first SUPPLYDEPOT near our first COMMANDCENTER 
                await self.build(SUPPLYDEPOT, near)
            else:
                near = self.units(SUPPLYDEPOT)[(self.units(SUPPLYDEPOT).amount - 1)] #  subsequent SUPPLYDs built near to previous one
                await self.build(SUPPLYDEPOT, near)
    
    # build REFINERY to mine gas from vespene geysers if we can afford REFINERY
    async def build_refinery(self):
        vgs = self.state.vespene_geyser.closer_than(10.0, self.units(COMMANDCENTER).first)
        for vg in vgs:
            if not self.can_afford(REFINERY):
                break
            worker = self.select_build_worker(vg.position) #  Need to delegate worker as FACTORY locations require identification
            if worker is None:
                break
            if not self.units(REFINERY).closer_than(1.0, vg).exists:
                await self.do(worker.build(REFINERY, vg))
                
    # build BARRACKS to build MARINEs if we can afford a BARRACKS and the amount of BARRACKS is less than 2
    async def build_barracks(self):
        if self.can_afford(BARRACKS) and self.units(BARRACKS).amount < 2:
            await self.build(BARRACKS, near=self.units(COMMANDCENTER).first)  # position BARRACKS next to first COMMANDCENTER

    # for each BARRACKS build MARINEs if we can afford a MARINE and the amount of MARINEs is smaller than 40
    async def build_marines(self):
        for rax in self.units(BARRACKS):
            if rax.is_ready and rax.noqueue:
                if self.can_afford(MARINE) and self.units(MARINE).amount < 40:
                    await self.do(rax.train(MARINE))
                    
    # build FACTORY to build CYCLONEs if amount of BARRACKS is larger than 1
    # and we can afford a FACTORY and we have no more than 1 FACTORY
    async def build_factory(self):
        if self.units(BARRACKS).amount > 0:
            if self.can_afford(FACTORY) and self.units(FACTORY).amount < 1 and not self.already_pending(FACTORY):
                await self.build(FACTORY, near=self.units(BARRACKS).first)  # position FACTORY next to first BARRACKS
    
    # for each FACTORY build CYCLONEs if we can afford a CYCLONE and the amount of CYCLONEs is smaller than 12
    async def build_cyclones(self):
        for fact in self.units(FACTORY):
            if fact.is_ready and fact.noqueue:
                if self.can_afford(CYCLONE) and self.units(CYCLONE).amount < 12:
                    await self.do(fact.train(CYCLONE))
    
    # function to identify the target of our attack
    def locate_target(self, state):
        if len(self.known_enemy_units) > 0:  
            return random.choice(self.known_enemy_units)  # if we know of more than 0 enemy units, there are our target
        elif len(self.known_enemy_structures) > 0:
            return random.choice(self.known_enemy_structures) # elif we know of more than 0 enemy buildings, there are our target
        else:
            return self.enemy_start_locations[0]  # else, the enemy start location is our target
    
    
    # attack enemy units through push with reinforcements
    async def attack(self):
        
        # if min 16 MARINES and min 3 CYCLONES are produed and known enemy units exist, attack known enemy units
        # used to reinforce first attack push continously so long as unit levels do not fall below the respective minima
        if self.units(MARINE).amount > 15 and self.units(CYCLONE).amount > 2:
            if len(self.known_enemy_units) > 0:
                for m in self.units(MARINE).idle:
                    await self.do(m.attack(random.choice(self.known_enemy_units)))
                for m in self.units(CYCLONE).idle:
                    await self.do(m.attack(random.choice(self.known_enemy_units)))

        # first attack push, attack enemy once min 21 MARINES and min 4 CYCLONES are produced
        if self.units(MARINE).amount > 20 and self.units(CYCLONE).amount > 3:
            for m in self.units(MARINE).idle:
                await self.do(m.attack(self.locate_target(self.state)))
            for c in self.units(CYCLONE).idle:
                await self.do(c.attack(self.locate_target(self.state)))

run_game(maps.get("CatalystLE"), [
    Bot(Race.Terran, CapsBot()),
    Computer(Race.Protoss, Difficulty.Hard)
    ], realtime = False)
