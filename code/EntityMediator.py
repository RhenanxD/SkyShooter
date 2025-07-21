from code.Const import WIN_WIDTH, MENU_OPTION
from code.Enemy import Enemy
from code.EnemyShot import EnemyShot
from code.Entity import Entity
from code.Player import Player
from code.PlayerShot import PlayerShot


class EntityMediator:
    game_mode = None  # Storage New game mode

    @staticmethod
    def set_game_mode(mode: str):
        EntityMediator.game_mode = mode

    @staticmethod
    def __verify_collision_window(ent: Entity):  # If enemies leave the screen health will be set to 0
        if isinstance(ent, Enemy):
            if ent.rect.right <= 0:
                ent.health = 0
        if isinstance(ent, PlayerShot):
            if ent.rect.left >= WIN_WIDTH:
                ent.health = 0
        if isinstance(ent, EnemyShot):
            if ent.rect.right <= 0:
                ent.health = 0

    @staticmethod
    def __verify_collision_entity(ent1, ent2):
        valid_interaction = False
        # Damage player and yours interactions
        player_hit_by_enemy = (isinstance(ent1, Player) and isinstance(ent2, Enemy)) or \
                              (isinstance(ent1, Enemy) and isinstance(ent2, Player))
        player_hit_by_enemy_shot = (isinstance(ent1, Player) and isinstance(ent2, EnemyShot)) or \
                                   (isinstance(ent1, EnemyShot) and isinstance(ent2, Player))
        enemy_hit_by_player_shot = (isinstance(ent1, Enemy) and isinstance(ent2, PlayerShot)) or \
                                   (isinstance(ent1, PlayerShot) and isinstance(ent2, Enemy))

        if player_hit_by_enemy or player_hit_by_enemy_shot or enemy_hit_by_player_shot:
            valid_interaction = True

        if valid_interaction:  # Verifying Valid Interaction
            if (ent1.rect.right >= ent2.rect.left and
                    ent1.rect.left <= ent2.rect.right and
                    ent1.rect.bottom >= ent2.rect.top and
                    ent1.rect.top <= ent2.rect.bottom):

                # Hardcore mode and No hit Challenge code
                if EntityMediator.game_mode == MENU_OPTION[1]:  # HARDCORE MODE
                    # Double damage enemies will cause into player
                    if player_hit_by_enemy_shot:
                        if isinstance(ent1, Player):
                            ent1.health -= (ent2.damage * 2)  # Player receive double damage
                            ent2.health -= ent1.damage  # Same damage bullet player to enemies
                        else:
                            ent2.health -= (ent1.damage * 2)
                            ent1.health -= ent2.damage
                    elif player_hit_by_enemy:  # Collision
                        if isinstance(ent1, Player):
                            ent1.health -= (ent2.damage * 2)
                            ent2.health -= ent1.damage
                        else:
                            ent2.health -= (ent1.damage * 2)
                            ent1.health -= ent2.damage
                    else:
                        ent1.health -= ent2.damage
                        ent2.health -= ent1.damage

                elif EntityMediator.game_mode == MENU_OPTION[2]:  # NO HIT CHALLENGE
                    # Every damage the player will lose
                    if player_hit_by_enemy or player_hit_by_enemy_shot:
                        if isinstance(ent1, Player):
                            ent1.health = 0  # Set health of player to 0
                        else:
                            ent2.health = 0
                    else:
                        ent1.health -= ent2.damage
                        ent2.health -= ent1.damage
                else:
                    ent1.health -= ent2.damage  # New game normal
                    ent2.health -= ent1.damage

                ent1.last_dmg = ent2.name
                ent2.last_dmg = ent1.name

    @staticmethod
    def __give_score(enemy: Enemy, entity_list: list[Entity]):  # Give Score just for enemies killed by Player
        if enemy.last_dmg == 'PlayerShot':
            for ent in entity_list:
                if ent.name == 'Player':
                    ent.score += enemy.score

    @staticmethod
    def verify_collision(entity_list: list[Entity]):  # Verifying Collision
        for i in range(len(entity_list)):
            entity1 = entity_list[i]
            EntityMediator.__verify_collision_window(entity1)
            for j in range(i + 1, len(entity_list)):
                entity2 = entity_list[j]
                EntityMediator.__verify_collision_entity(entity1, entity2)

    @staticmethod
    def verify_health(entity_list: list[Entity]):  # Kill enemies if the health is 0
        for ent in entity_list:
            if ent.health <= 0:
                if isinstance(ent, Enemy):
                    EntityMediator.__give_score(ent, entity_list)  # verifying score
                entity_list.remove(ent)
