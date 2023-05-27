from Engine.GameObjects.Components.Physics.BoxCollider2D import BoxCollider2D
from Engine.GameObjects.Components.Physics.Collider2D import Collider2D
from Engine.GameObjects.Components.Physics.Rigidbody2D import Rigidbody2D
from Engine.Other.Interfaces.IStartable import IStartable
from Engine.Other.Interfaces.IUpdateable import IUpdateable


class CollisionManager(IUpdateable, IStartable):
    def __init__(self, scene_manager):
        self.__scene_manager = scene_manager

    def check_collision(self, collider1, collider2):
        if collider1.collides_with(collider2):
            collider1_entity = collider1.parent
            collider2_entity = collider2.parent

            # Example of adjusting positions to prevent overlap
            if collider1.bounds.right > collider2.bounds.left and collider1.bounds.left < collider2.bounds.left:
                collider1_entity.transform.position.x = collider2.bounds.left - collider1.bounds.width
            elif collider1.bounds.left < collider2.bounds.right and collider1.bounds.right > collider2.bounds.right:
                collider1_entity.transform.position.x = collider2.bounds.right

            if collider1.bounds.bottom > collider2.bounds.top and collider1.bounds.top < collider2.bounds.top:
                collider1_entity.transform.position.y = collider2.bounds.top - collider1.bounds.height
            elif collider1.bounds.top < collider2.bounds.bottom and collider1.bounds.bottom > collider2.bounds.bottom:
                collider1_entity.transform.position.y = collider2.bounds.bottom

            collider = collider1.parent.get_component(Collider2D)

            if collider is not None:
                collider.handle_response(collider2_entity)


    def start(self):
        pass

    def update(self, game_time):
        # Iterate through all colliders or pairs of colliders to check for collisions
        colliders = self.__scene_manager.active_scene.get_all_components_by_type(BoxCollider2D)

        for i in range(len(colliders)):
            for j in range(i + 1, len(colliders)):
                collider1 = colliders[i]
                collider2 = colliders[j]
                self.check_collision(collider1, collider2)
