from scripts.game_accessor import GameAccessor
from scripts import er_helper
from scripts import database_helper
from scripts import walk_back
from scripts import speedhack
import dxcam
import time
import numpy as np
import cv2
import gymnasium

movement_only_space = {
    0: ['w'],           # forward
    1: ['a'],           # left
    2: ['s'],           # back
    3: ['d'],           # right
    4: ['w', 'space'],  # forward roll
    5: ['a', 'space'],  # left roll
    6: ['s', 'space'],  # back roll
    7: ['d', 'space'],  # right roll
    8: ['space'],       # dodge
    9: ['f'],           # jump
    10: ['w', 'f'],     # forward jump
    11: ['a', 'f'],     # left jump
    12: ['s', 'f'],     # back jump
    13: ['d', 'f'],     # right jump
}

movement_and_heal_space = {
    0: ['w'],           # forward
    1: ['a'],           # left
    2: ['s'],           # back
    3: ['d'],           # right
    4: ['w', 'space'],  # forward roll
    5: ['a', 'space'],  # left roll
    6: ['s', 'space'],  # back roll
    7: ['d', 'space'],  # right roll
    8: ['space'],       # dodge
    9: ['f'],           # jump
    10: ['w', 'f'],     # forward jump
    11: ['a', 'f'],     # left jump
    12: ['s', 'f'],     # back jump
    13: ['d', 'f'],     # right jump
    16: ['r'],          # use item
}

all__action_space = {
    0: ['w'],           # forward
    1: ['a'],           # left
    2: ['s'],           # back
    3: ['d'],           # right
    4: ['w', 'space'],  # forward roll
    5: ['a', 'space'],  # left roll
    6: ['s', 'space'],  # back roll
    7: ['d', 'space'],  # right roll
    8: ['space'],       # dodge
    9: ['f'],           # jump
    10: ['w', 'f'],     # forward jump
    11: ['a', 'f'],     # left jump
    12: ['s', 'f'],     # back jump
    13: ['d', 'f'],     # right jump
    14: ['w', 'f', 'l'],# forward jump + strong attack
    15: ['x'],          # crouch
    16: ['3'],          # switch target left
    17: ['4'],          # switch target right
    18: ['m'],          # attack
    19: ['l'],          # strong attack
    20: ['k'],          # block
    21: ['n'],          # use skill
    22: ['r'],          # use item
}

action_spaces = [movement_only_space, movement_and_heal_space, all__action_space]

class EldenRing(gymnasium.Env):
    def __init__(self, action_space = 0, database_writing = False, n_steps = 1024):
        self.__database_writing = database_writing
        self.__game = GameAccessor()
        self.__camera = dxcam.create()
        left, top, right, bottom = er_helper.client_window_size()
        # This small offset is for a 4k monitor, might be different for others
        self.__region = (12 + left, 52 + top, 12 + right, 52 + bottom)

        self.obs_type = "rgb"
        self.action_space = gymnasium.spaces.Discrete(len(action_spaces[action_space]))
        self.observation_space = gymnasium.spaces.Box(low=0, high=1, shape=((self.__region[3]- self.__region[1]), (self.__region[2] - self.__region[0]), 3), dtype=np.uint8)

        # can switch action spaces and reward function
        self.train_mode = action_space
        # hardcore complex action space for now
        self.key_action_space = action_spaces[2]
        self.reward_function = self.complex_reward
        self.games = 0

        # Used for database writing
        self.time_step_run = 0
        self.time_step_total = 0
        self.n_steps = n_steps
        self.begin_time = 0
        self.end_time = 0

        self.speed_hack = speedhack.SpeedHackConnector(self.__game.get_process_id())
        self.speed = 3
        walk_back.game_speed = self.speed
        er_helper.game_speed = self.speed
        self.speed_hack.set_game_speed(self.speed)

        if self.__database_writing:
            database_helper.create_database()
            self.games = database_helper.get_run_number() + 1 if database_helper.get_run_number() > 0 else 0

        self.__game.reset()

    def kill_player(self):
        self.__game.kill_player()
        self.__game.set_animation_speed(8)
        time.sleep(9)
        self.__game.set_animation_speed(1)

        # if respawn stake, choose round table
        # maybe make it not go to round table if choice
        if self.marika:
            er_helper.key_press('right', 0.08)
            er_helper.key_press('e', 0.08)

    def begin_boss(self):
        # try and start the boss,
        # if too much time has ellapsed since
        # 'walkback' and the 'enemy' being missing,
        # kill player, start again

        self.enemy_id = walk_back.margit()
        self.__game.reset() # Reset when entering new area, just incase

        time.sleep(2)

    def reset(self, seed=0, options=0) -> None:
        self.win = False

        if not self.__game.player_in_roundtable():
            self.kill_player()

        
        while self.__game.loading_state():
            time.sleep(0.1)

        self.__game.set_animation_speed(8)
        time.sleep(1)
        self.__game.set_animation_speed(1)

        # after n games change the walkback function, maybe 1k then 10k then 100k
        self.reward = 0
        self.time_step_run = 0
        self.games += 1
        print(f"RESET CALLED: GAME {self.games} STARTING...")
        er_helper.clean_keys()

        while True:
            self.__game.clean()
            self.begin_boss()
            self.marika = self.__game.stake_of_marika()
            search_timer = time.time()

            while self.__game.enemies == {}:
                time.sleep(0.02)
                self.__game.find_enemies(self.enemy_id.copy())

                if time.time() - search_timer > 1:
                    self.kill_player()
                    break

            if self.__game.enemies != {}:
                idle_anim = self.__game.get_enemy_animation()
                er_helper.enter_boss()
                time.sleep(1.2 / self.speed)
                if self.__game.get_enemy_animation() == idle_anim:
                    self.kill_player()
                else:
                    break

        if self.__database_writing:
            for i in range(0, len(self.enemy_id)):
                database_helper.increase_attempts(self.enemy_id[i])

        self.screenshot()
        self.reset_ground_truth()

        return self.state(), {}

    def reset_ground_truth(self) -> None:
        self.begin_time = time.time()
        # used for rewards
        self.deal_damage_timer = time.time()
        self.take_damage_timer = time.time()

        self.player_max_health = self.__game.get_player_max_health()
        self.player_current_health = self.__game.get_player_health()
        self.player_max_stamina = self.__game.get_player_max_stamina()
        self.player_current_stamina = self.__game.get_player_stamina()
        self.player_max_fp = self.__game.get_player_max_fp()
        self.player_current_fp = self.__game.get_player_fp()
        self.boss_max_health = self.__game.get_enemy_max_health()
        self.boss_current_health = self.__game.get_enemy_health()
        self.player_coordinates = self.__game.get_player_coords()
        self.boss_coordinates = self.__game.get_enemy_coords()
        self.player_animation = self.__game.get_player_animation()
        self.boss_animation = self.__game.get_enemy_animation()
        self.player_current_flasks = self.__game.get_player_heal_flask()

        self.player_previous_health = self.player_current_health
        self.player_previous_stamina = self.player_current_stamina
        self.player_previous_fp = self.player_current_fp
        self.boss_previous_health = self.boss_current_health
        self.player_previous_coordinates = self.player_coordinates
        self.boss_previous_coordinates = self.boss_coordinates
        self.player_previous_animation = self.player_animation
        self.boss_previous_animation = self.boss_animation
        self.player_previous_flasks = self.player_current_flasks

    def perform_action(self, action) -> None:
        er_helper.press_combos(self.key_action_space[action])

    def screenshot(self) -> None:
        # screenshot, convert to correct color space
        # DXCam boasts high screen capture speed, but will throw
        # an error if the frame does not change since last screenshot
        try:
            m = np.array(self.__camera.grab(region = self.__region))
            m = cv2.cvtColor(m, cv2.COLOR_BGRA2RGB)
            self.__screenshot = m
        except:
            return

    def update(self) -> None:
        # update previous and current values
        # needed for reward and database
        self.player_previous_health = self.player_current_health
        self.player_previous_stamina = self.player_current_stamina
        self.player_previous_fp = self.player_current_fp
        self.boss_previous_health = self.boss_current_health
        self.player_previous_coordinates = self.player_coordinates
        self.boss_previous_coordinates = self.boss_coordinates
        self.player_previous_animation = self.player_animation
        self.boss_previous_animation = self.boss_animation
        self.player_previous_flasks = self.player_current_flasks

        self.player_current_health = self.__game.get_player_health()
        self.player_current_stamina = self.__game.get_player_stamina()
        self.player_current_fp = self.__game.get_player_fp()
        self.boss_current_health = self.__game.get_enemy_health()
        self.player_coordinates = self.__game.get_player_coords()
        self.player_animation = self.__game.get_player_animation()
        self.boss_coordinates = self.__game.get_enemy_coords()
        self.boss_animation = self.__game.get_enemy_animation()
        self.player_current_flasks = self.__game.get_player_heal_flask()

        if not self.__database_writing:
            return

        if self.player_animation != self.player_previous_animation:
            database_helper.write_to_database_animations({"Animation_ID": self.player_animation, "Run_Number": self.games, "Boss_ID": 0})

        for i in range(0, len(self.boss_animation)):
            if self.boss_animation[i] != self.boss_previous_animation[i]:
                database_helper.write_to_database_animations({"Animation_ID": self.boss_animation[i], "Run_Number": self.games, "Boss_ID": self.enemy_id[i]})

    def state(self):
        return self.__screenshot

    def simple_reward(self) -> None:
        self.reward = 1 * (self.time_step_run / 128)

        for i in range(0, len(self.__game.enemies)):
        # reward for dealing damage
            if self.boss_current_health[i] < self.boss_previous_health[i]:
                self.deal_damage_timer = time.time()
                self.reward += (1 + ((self.boss_previous_health[i] - self.boss_current_health[i]) / self.boss_max_health[i]))

        # punish for taking damage
        if self.player_current_health < self.player_previous_health:
            self.take_damage_timer = time.time()
            self.reward -= (7 + ((self.player_previous_health - self.player_current_health) / self.player_max_health))

        if time.time() - self.deal_damage_timer > (12 / self.speed):
            self.reward -= (1 + (time.time() - self.deal_damage_timer - (12 / self.speed)) / 10)

    def complex_reward(self) -> None:
        self.simple_reward()

        # punish for low stamina
        if self.player_current_stamina < self.player_max_stamina * 0.25:
            self.reward -= (1 + ((self.player_max_stamina * 0.25 - self.player_current_stamina) / self.player_max_stamina))

        if (self.player_current_flasks < self.player_previous_flasks) and (self.boss_current_health == self.boss_previous_health):
            self.reward -= 5

        if self.player_current_health > self.player_previous_health:
            # reward for healing
            self.reward += (3 + ((self.player_current_health - self.player_previous_health) / self.player_max_health))

            # punish if healing way too early, lvl 1 flask heals 250, so if missing ou
            # on more than 75 potential hp, punish
            # 175 is an arbitrary number in this case
            health_diff = self.player_current_health - self.player_previous_health
            if health_diff < 175:
                self.reward -= (3 + (250 - (self.player_current_health - self.player_previous_health)) / 175)

        # reward if avoiding damage for more than 15 seconds
        if time.time() - self.take_damage_timer > (12 / self.speed):
            self.reward += (1 + (time.time() - self.take_damage_timer) / (12 / self.speed))

    def one_shot_done(self) -> bool:
        return self.reg_done() or (self.player_current_health < self.player_max_health)

    def range_done(self) -> bool:
        return self.reg_done() or self.player_current_health < (self.player_max_health * .4)

    def reg_done(self) -> bool:
        if self.__game.get_player_dead():
            self.reward -= 10
            return True

        for i in self.__game.get_enemy_dead():
            if not i:
                return False

        self.reward += 10
        self.win = True
        return True

    def cutscene_check(self) -> bool:
        # while in cut scene, wait, clean enemies, find enemies, need to update for phase 2 bosses
        # removed for now until workaround can be found
        # TODO:
        #load = False
        #broken = False

        #while self.__game.loading_state():
        #    for i in range(0, len(self.__game.enemies)):
        #        if self.__game.get_enemy_coords()[i] != self.boss_coordinates[i]:
        #            broken = True
        #            break
        #    if broken:
        #        break
        #    load = True
        #    er_helper.key_press('esc', 0.2)
        #    time.sleep(0.01)

        #if load and not broken:
        #    # this will check for the phase 2 enemy
        #    self.__game.clean()
        #    self.__game.find_enemies(self.enemy_id.copy())
        #    print(self.__game.get_enemy_id())
        #    er_helper.clean_keys()
        #    er_helper.key_press('q', .1)
        ...

    def step(self, action):
        # arbitrary delay to ensure that only 7 or so actions are performed per second
        time.sleep(0.10 / (self.speed * self.speed))
        self.cutscene_check()

        self.perform_action(action)

        if not (self.time_step_total % self.n_steps == 0 and self.time_step_total > 1):
            self.update()
        
        self.screenshot()
        self.reward_function()
        done = ([self.one_shot_done(), self.range_done(), self.reg_done()][self.train_mode])

        truncated = False

        if self.time_step_total % self.n_steps == 0 and self.time_step_total > 1:
            truncated = True
            if not self.__game.player_in_roundtable():
                self.__game.kill_player()
            er_helper.clean_keys()

        if self.__database_writing and self.time_step_run % 4 == 0:
            for i in range(0, len(self.enemy_id)):
                step_info = {
                    "Run_Number": self.games,
                    "Timestep": self.time_step_run,
                    "Boss_ID": self.enemy_id[i],
                    "pX": self.player_coordinates[0],
                    "pY": self.player_coordinates[1],
                    "pZ": self.player_coordinates[2],
                    "pHealth": self.player_current_health,
                    "pAnimation": self.player_animation,
                    "pAction": action,
                    "pReward": self.reward,
                    "bX": self.boss_coordinates[i][0],
                    "bY": self.boss_coordinates[i][1],
                    "bZ": self.boss_coordinates[i][2],
                    "bHealth": self.boss_current_health[i],
                    "bAnimation": self.boss_animation[i]
                }

                database_helper.write_to_database_step_boss(step_info)
            database_helper.write_to_database_step_player(step_info)

        if done or truncated:
            er_helper.clean_keys()
            self.kill_player()
            self.end_time = time.time()

            if self.__database_writing:
                for i in range(0, len(self.enemy_id)):
                    run_info = {
                        "Run_Number": self.games,
                        "Boss_ID": self.enemy_id[i],
                        "Boss_Ending_Health": self.boss_current_health[i],
                        "Player_Ending_Health": self.player_current_health,
                        "Total_Time": self.end_time - self.begin_time,
                        "Victory": (self.player_current_health > 0)
                    }

                    database_helper.write_to_database_run(run_info)

            # wait for player to start animation
            time.sleep(4)

            if not self.win:
                self.__game.set_animation_speed(8)
                time.sleep(9)
                self.__game.set_animation_speed(1)

                if self.marika:
                    er_helper.key_press('right', 0.1)
                    er_helper.key_press('e', 0.1)
                    time.sleep(9)

            # if player is in loading screen
            # if self.__game.loading_state():
            # time.sleep(15)

        self.time_step_run += 1
        self.time_step_total += 1

        return self.state(), self.reward, done, truncated, {}

    def close(self) -> None:
        pass

if __name__ == "__main__":
    pass