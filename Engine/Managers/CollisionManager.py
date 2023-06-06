import math
import time

import pygame
from pygame import Rect

from App.Components.Colliders.TreeCollider2D import TreeCollider
from App.Components.Controllers.EnemyController import EnemyController
from App.Components.Controllers.PlayerController import PlayerController
from App.Constants.Application import Application
from Engine.GameObjects.Character import Character
from Engine.GameObjects.Components.Physics.BoxCollider2D import BoxCollider2D
from Engine.GameObjects.Components.Physics.Collider import Collider
from Engine.GameObjects.Components.Physics.CollisionArea import CollisionArea
from Engine.GameObjects.Components.Physics.Point import Point
from Engine.GameObjects.Components.Physics.QuadTree import QuadTree
from Engine.GameObjects.Components.Physics.Rigidbody2D import Rigidbody2D
from Engine.Graphics.Renderers.Renderer2D import Renderer2D
from Engine.Managers.Manager import Manager
from Engine.Other.Enums.EventEnums import EventCategoryType, EventActionType
from Engine.Other.Enums.RendererLayers import RendererLayers
from Engine.Other.Interfaces.IStartable import IStartable
from Engine.Other.Interfaces.IUpdateable import IUpdateable


class CollisionManager(Manager):
    def __init__(self, collision_range, scene_manager, camera_manager, event_dispatcher):
        super().__init__(event_dispatcher)
        self.__colliders = None
        self.__collision_range = collision_range
        self.__scene_manager = scene_manager
        self.__camera_manager = camera_manager
        self.collision_area = CollisionArea(self.__camera_manager.active_camera.parent.transform.position.x,
                                            self.__camera_manager.active_camera.parent.transform.position.y,
                                            self.__camera_manager.active_camera.viewport.x,
                                            self.__camera_manager.active_camera.viewport.y)
        self.colliders = {}
        self.grid_cell_size = 72  # Adjust the cell size based on your colliders and scene size
        self.grid = {}
        self.colliding_cells = {}
        self.quad_tree = QuadTree(self.collision_area.boundary, 4)

    def update_collision_area(self):
        camera = self.__camera_manager.active_camera
        viewport = camera.viewport
        camera_position = camera.parent.transform.position

        self.collision_area = CollisionArea(
            100,
            100,
            viewport.x,
            viewport.y

        )

        #print("Camera", camera_position.x)
        #print((Application.Player.transform.position.x - camera.viewport.x // 2) - camera_position.x)
        #print(self.collision_area.boundary)

    def collision_area(self):
        return self.collision_area
    def start(self):
        self.__colliders = self.__scene_manager.active_scene.get_all_components_by_type(BoxCollider2D)
        scene_bounds = Rect(0, 0, 120 * 36, 110 * 36)


        self.quad_tree = QuadTree(pygame.Rect(0,0, 1100 * 72, 1100 * 72), 4)

        #print(len(self.__colliders))
        # Insert colliders into the Quadtree
        for collider in self.__colliders:
            #print(collider.parent.name)
            # print(collider.bounds)
            # print(collider.transform.position)
            point = Point(collider.bounds, collider)
            self.quad_tree.insert(point)



    def update(self, game_time):
        # Update the collision area based on the camera position
        self.update_collision_area()

        self.quad_tree.remove(Point(Application.Player.get_component(BoxCollider2D).bounds, Application.Player.get_component(BoxCollider2D)))

        self.quad_tree.insert(Point(Application.Player.get_component(BoxCollider2D).bounds,
                                    Application.Player.get_component(BoxCollider2D)))


        #print(self.collision_area.boundary)
        potential_colliders = self.quad_tree.query(self.collision_area.boundary)

        print(len(self.quad_tree.objects))

        #print(len(potential_colliders))

        for i in range(len(potential_colliders)):
            collider1 = potential_colliders[i]
            for j in range(i + 1, len(potential_colliders)):
                collider2 = potential_colliders[j]
                self.check_collision(collider1.data, collider2.data, game_time)


    def _subscribe_to_events(self):
        self._event_dispatcher.add_listener(EventCategoryType.CollisionManager, self._handle_events)

    def _handle_events(self, event_data):
        if event_data.event_action_type == EventActionType.SetUpColliders:
            self.start()

    def add_collider(self, collider):
        # Add a collider to the dictionary using its parent as the key
        self.colliders[collider.parent] = collider

    def remove_collider(self, collider):
        # Remove a collider from the dictionary using its parent as the key
        if collider.parent in self.colliders:
            del self.colliders[collider.parent]

    def check_collision(self, collider1, collider2, game_time):
        # pass
        collider1_entity = collider1.parent
        collider2_entity = collider2.parent

        #print(collider1_entity.name)
        #print()

        if collider1.collides_with(collider2):
            pass
            #print("SOLO")
        #     if isinstance(collider1, TreeCollider) and isinstance(collider2_entity, Character):
        #         collider1_entity.get_component(Renderer2D).layer = RendererLayers.WorldObjects
        #     elif isinstance(collider2, TreeCollider) and isinstance(collider1_entity, Character):
        #         collider2_entity.get_component(Renderer2D).layer = RendererLayers.WorldObjects
        #
        #     collider1_rigidbody = collider1_entity.get_component(Rigidbody2D)
        #     collider2_rigidbody = collider2_entity.get_component(Rigidbody2D)
        #
        #     is_collider1_static = collider1_entity.game_object_type.Static
        #     is_collider2_static = collider2_entity.game_object_type.Static
        #
        #     displacement = collider1.calculate_displacement_vector(collider2)
        #
        #     if displacement.length_squared() != 0:  # Check for non-zero length
        #         if collider1_rigidbody and collider2_rigidbody:
        #             pass
        #         elif collider1_rigidbody and is_collider2_static:
        #             overlap_x = min(collider1.bounds.right - collider2.bounds.left,
        #                             collider2.bounds.right - collider1.bounds.left)
        #             overlap_y = min(collider1.bounds.bottom - collider2.bounds.top,
        #                             collider2.bounds.bottom - collider1.bounds.top)
        #
        #             if overlap_x < overlap_y:
        #                 if overlap_x == collider1.bounds.right - collider2.bounds.left:
        #                     # Check if it's a corner collision
        #                     if collider1.bounds.bottom == collider2.bounds.top:
        #                         collider1_entity.transform.position.x = collider2.bounds.left - collider1.bounds.width
        #                         collider1_entity.transform.position.y = collider2.bounds.top - collider1.bounds.height
        #                     else:
        #                         collider1_entity.transform.position.x -= overlap_x
        #                 else:
        #                     # Check if it's a corner collision
        #                     if collider1.bounds.bottom == collider2.bounds.top:
        #                         collider1_entity.transform.position.x = collider2.bounds.right
        #                         collider1_entity.transform.position.y = collider2.bounds.top - collider1.bounds.height
        #                     else:
        #                         collider1_entity.transform.position.x += overlap_x
        #             else:
        #                 if overlap_y == collider1.bounds.bottom - collider2.bounds.top:
        #                     # Check if it's a corner collision
        #                     if collider1.bounds.right == collider2.bounds.left:
        #                         collider1_entity.transform.position.y = collider2.bounds.top - collider1.bounds.height
        #                         collider1_entity.transform.position.x = collider2.bounds.left - collider1.bounds.width
        #                     else:
        #                         collider1_entity.transform.position.y -= overlap_y
        #                 else:
        #                     # Check if it's a corner collision
        #                     if collider1.bounds.right == collider2.bounds.left:
        #                         collider1_entity.transform.position.y = collider2.bounds.bottom
        #                         collider1_entity.transform.position.x = collider2.bounds.left - collider1.bounds.width
        #                     else:
        #                         collider1_entity.transform.position.y += overlap_y
        #
        #         elif is_collider1_static and collider2_rigidbody:
        #             overlap_x = min(collider2.bounds.right - collider1.bounds.left,
        #                             collider1.bounds.right - collider2.bounds.left)
        #             overlap_y = min(collider2.bounds.bottom - collider1.bounds.top,
        #                             collider1.bounds.bottom - collider2.bounds.top)
        #
        #             if overlap_x < overlap_y:
        #                 if overlap_x == collider2.bounds.right - collider1.bounds.left:
        #                     # Check if it's a corner collision
        #                     if collider2.bounds.bottom == collider1.bounds.top:
        #                         collider2_entity.transform.position.x = collider1.bounds.left - collider2.bounds.width
        #                         collider2_entity.transform.position.y = collider1.bounds.top - collider2.bounds.height
        #                     else:
        #                         collider2_entity.transform.position.x -= overlap_x
        #                 else:
        #                     # Check if it's a corner collision
        #                     if collider2.bounds.bottom == collider1.bounds.top:
        #                         collider2_entity.transform.position.x = collider1.bounds.right
        #                         collider2_entity.transform.position.y = collider1.bounds.top - collider2.bounds.height
        #                     else:
        #                         collider2_entity.transform.position.x += overlap_x
        #             else:
        #                 if overlap_y == collider2.bounds.bottom - collider1.bounds.top:
        #                     # Check if it's a corner collision
        #                     if collider2.bounds.right == collider1.bounds.left:
        #                         collider2_entity.transform.position.y = collider1.bounds.top - collider2.bounds.height
        #                         collider2_entity.transform.position.x = collider1.bounds.left - collider2.bounds.width
        #                     else:
        #                         collider2_entity.transform.position.y -= overlap_y
        #                 else:
        #                     # Check if it's a corner collision
        #                     if collider2.bounds.right == collider1.bounds.left:
        #                         collider2_entity.transform.position.y = collider1.bounds.bottom
        #                         collider2_entity.transform.position.x = collider1.bounds.left - collider2.bounds.width
        #                     else:
        #                         collider2_entity.transform.position.y += overlap_y
        #
        #     if collider1_entity.get_component(Collider):
        #         collider1_entity.get_component(Collider).handle_response(collider2_entity)
        #
        #     if collider2_entity.get_component(Collider):
        #         collider2_entity.get_component(Collider).handle_response(collider1_entity)
        # else:
        #     if isinstance(collider1, TreeCollider) and isinstance(collider2_entity, Character):
        #         collider1_entity.get_component(Renderer2D).layer = RendererLayers.Tree
        #     elif isinstance(collider2, TreeCollider) and isinstance(collider1_entity, Character):
        #         collider2_entity.get_component(Renderer2D).layer = RendererLayers.Tree
        #
        #     if collider1_entity.get_component(Collider):
        #         collider1_entity.get_component(Collider).handle_collision_exit()
        #
        #     if collider2_entity.get_component(Collider):
        #         collider2_entity.get_component(Collider).handle_collision_exit()



        # self.grid.clear()
        #
        # self.initialize_grid(scene_bounds)
        #
        # # Create a dictionary to store colliding rectangles for each grid cell
        # self.colliding_cells = {}
        #
        # for collider in self.__colliders:
        #     self.assign_collider_to_cells(collider)

    def initialize_grid(self, scene_bounds):
        # Grid dimensions
        grid_size = 100
        grid_width = 72
        grid_height = 72

        self.grid = {}
        for row in range(grid_size):
            for col in range(grid_size):
                rect = pygame.Rect(col * grid_width, row * grid_height, grid_width, grid_height)
                self.grid[(row, col)] = rect

    def assign_collider_to_cells(self, collider):
        collider_rect = collider.bounds
        cells_to_check = []

        grid_width = 72
        grid_height = 72

        # Determine the cells to check based on the collider's position and size
        top_left_cell = (int(collider_rect.y / grid_height), int(collider_rect.x / grid_width))
        bottom_right_cell = (int((collider_rect.y + collider_rect.height) / grid_height),
                             int((collider_rect.x + collider_rect.width) / grid_width))

        # Add cells within the range of the collider's bounding rectangle to the list of cells to check
        for row in range(top_left_cell[0], bottom_right_cell[0] + 1):
            for col in range(top_left_cell[1], bottom_right_cell[1] + 1):
                cells_to_check.append((row, col))

        # Check for collisions with the collider's rectangle against the cells in the list
        for cell in cells_to_check:
            rect = self.grid.get(cell)
            if rect and collider_rect.colliderect(rect):
                if cell not in self.colliding_cells:
                    self.colliding_cells[cell] = []
                self.colliding_cells[cell].append(collider)

        colliders = set()

        for collider_list in self.colliding_cells.values():
            for collider in collider_list:
                colliders.add(collider)






        # # Determine the cells intersecting with the screen
        # start_cell_x = math.floor(self.collision_area.left / self.grid_cell_size)
        # start_cell_y = math.floor(self.collision_area.top / self.grid_cell_size)
        # end_cell_x = math.ceil(self.collision_area.right / self.grid_cell_size)
        # end_cell_y = math.ceil(self.collision_area.bottom / self.grid_cell_size)
        #
        # colliders_in_collision_area = set()
        #
        # # Iterate through the cells within the collision area
        # for x in range(start_cell_x, end_cell_x):
        #     for y in range(start_cell_y, end_cell_y):
        #         cell_key = (x, y)
        #         if cell_key in self.colliding_cells:
        #             colliders_in_collision_area.update(self.colliding_cells[cell_key])
        #
        # print("Colliders in collision area:", len(colliders_in_collision_area))
        #
        # # Perform collision checks on the colliders within the collision area
        # colliders_in_collision_area = list(colliders_in_collision_area)

        # for i in range(len(self.__colliders)):
        #     collider1 = self.__colliders[i]
        #     for j in range(i + 1, len(colliders_in_collision_area)):
        #         collider2 = colliders_in_collision_area[j]
        #         self.check_collision(collider1, collider2, game_time)

    # def update(self, game_time):
    #     # Iterate through all colliders or pairs of colliders to check for collisions
    #     self.collision_area.set_x(self.__camera_manager.active_camera.parent.transform.position.x)
    #     self.collision_area.set_y(self.__camera_manager.active_camera.parent.transform.position.y)
    #
    #     start_time = time.time()
    #     # Determine the cells intersecting with the screen
    #     start_cell_x = math.floor(self.collision_area.left / self.grid_cell_size)
    #     start_cell_y = math.floor(self.collision_area.top / self.grid_cell_size)
    #     end_cell_x = math.ceil(self.collision_area.right / self.grid_cell_size)
    #     end_cell_y = math.ceil(self.collision_area.bottom / self.grid_cell_size)
    #
    #     # Populate colliders_on_screen set
    #     colliders_on_screen = set()
    #     processed_cells = set()  # Store processed cell keys
    #     for x in range(start_cell_x, end_cell_x):
    #         for y in range(start_cell_y, end_cell_y):
    #             cell_key = (x, y)
    #             if cell_key in self.grid and cell_key not in processed_cells:
    #                 colliders_on_screen.update(self.grid[cell_key])
    #                 processed_cells.add(cell_key)
    #
    #     colliders_on_screen = list(colliders_on_screen)
    #
    #     print("Colliders on screen total:", len(colliders_on_screen))
    #
    #     colliders_on_screen = list(colliders_on_screen)
    #
    #     end_time = time.time()
    #
    #     elapsed_time = end_time - start_time
    #
    #     elapsed_time_ms = elapsed_time * 1000
    #     print("Elapsed time:", elapsed_time_ms, "milliseconds")
    #
    #     print("Colliders on screen total", len(colliders_on_screen))
    #
    #     Use colliders_on_screen for further processing or collision checks
    #     for i, collider1 in enumerate(colliders_on_screen):
    #         for collider2 in colliders_on_screen[i + 1:]:
    #             self.check_collision(collider1, collider2, game_time)


