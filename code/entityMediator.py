class EntityMediator:
    @classmethod
    def verify_collision(cls, entity_list):
        pass

    @classmethod
    def verify_health(cls, entity_list):
        pass


from code.entityMediator import EntityMediator
from code.Const import WIN_WIDTH
from code.enemy import Enemy
from code.enemyShot import EnemyShot
from code.entity import entity
from code.player import Player
from code.playerShot import playerShot


class EntityMediator:
    # Constantes para tipos de dano e pontuações
    PLAYER_1_SHOT = 'Player1Shot'
    PLAYER_2_SHOT = 'Player2Shot'
    PLAYER_1 = 'Player1'
    PLAYER_2 = 'Player2'

    @staticmethod
    def __is_outside_window(ent: entity) -> bool:
       # """Retorna True se a entidade estiver fora das bordas da janela."""
        return (isinstance(ent, Enemy) and ent.rect.right <= 0) or \
            (isinstance(ent, playerShot) and ent.rect.left >= WIN_WIDTH) or \
            (isinstance(ent, EnemyShot) and ent.rect.right <= 0)

    @staticmethod
    def __handle_entity_outside_window(ent: entity):
        #"""Marca saúde como zero se a entidade estiver fora da janela."""
        if EntityMediator.__is_outside_window(ent):
            ent.health = 0

    @staticmethod
    def __are_entities_colliding(ent1: entity, ent2: entity) -> bool:
        collision = (ent1.rect.right >= ent2.rect.left and
                     ent1.rect.left <= ent2.rect.right and
                     ent1.rect.bottom >= ent2.rect.top and
                     ent1.rect.top <= ent2.rect.bottom)
        print(f"Teste colisão entre {ent1.name} e {ent2.name}: {collision}")  # Debug
        return collision

    @staticmethod
    def __handle_entity_collision(ent1: entity, ent2: entity):
        valid_collisions = [
            (Enemy, playerShot),
            (playerShot, Enemy),
            (Player, EnemyShot),
            (EnemyShot, Player),
            (Player, Enemy)
        ]

        # Verificar as posições das entidades
        print(f"Posição de {ent1.name}: {ent1.rect.x}, {ent1.rect.y}")
        print(f"Posição de {ent2.name}: {ent2.rect.x}, {ent2.rect.y}")

        if any(isinstance(ent1, t1) and isinstance(ent2, t2) for t1, t2 in valid_collisions):
            if EntityMediator.__are_entities_colliding(ent1, ent2):
                print(f"COLISÃO DETECTADA entre {ent1.name} e {ent2.name}")  # Debug
                ent1.health -= ent2.damage
                ent2.health -= ent1.damage
                ent1.last_dmg = ent2.name
                ent2.last_dmg = ent1.name

    @staticmethod
    def __update_score_for_enemy(enemy: Enemy, entity_list: list[entity]):
       # """Atualiza a pontuação do jogador para um inimigo destruído."""
        for ent in entity_list:
            if (enemy.last_dmg == EntityMediator.PLAYER_1_SHOT and ent.name == EntityMediator.PLAYER_1) or \
                    (enemy.last_dmg == EntityMediator.PLAYER_2_SHOT and ent.name == EntityMediator.PLAYER_2):
                ent.score += enemy.score

    @staticmethod
    def verify_collision(entity_list: list[entity]):
        for i, entity1 in enumerate(entity_list):
            EntityMediator.__handle_entity_outside_window(entity1)
            for j in range(i + 1, len(entity_list)):
                entity2 = entity_list[j]
                EntityMediator.__handle_entity_collision(entity1, entity2)


    @staticmethod
    def verify_health(entity_list: list[entity]):
      #  """Remove entidades com saúde <= 0 e atualiza a pontuação."""
        dead_entities = [ent for ent in entity_list if ent.health <= 0]
        for ent in dead_entities:
            print(f"{ent.name} foi destruído!")  # Debug para ver quando a entidade é destruída
            if isinstance(ent, Enemy):
                EntityMediator.__update_score_for_enemy(ent, entity_list)
            entity_list.remove(ent)
