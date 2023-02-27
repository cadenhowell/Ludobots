import random
import string
import numpy as np


class Joint:
    def __init__(self, name, parent, child, type, pos, jointAxis, old_direction, new_direction):
        self.name = name
        self.parent = parent
        self.child = child
        self.type = type
        self.pos = pos
        self.jointAxis = jointAxis
        self.old_direction = old_direction
        self.new_direction = new_direction


class Cube:
    def __init__(self, name, pos, size, is_sensor, direction):
        self.name = name
        self.pos = pos
        self.size = size
        self.isSensor = is_sensor
        self.direction = direction


class Morphology:

    def __init__(self, seed=None, side_len_range=(0.2, 2.2), num_links_range=(3, 10)):
        self.joints = []
        self.links = []
        self.sensors = []
        self.root = ''

        self.min_side_len = side_len_range[0]
        self.max_side_len = side_len_range[1]

        random.seed(seed)
        np.random.seed(seed)

        self.min_num_segments = num_links_range[0]
        self.max_num_segments = num_links_range[1]
        self.initial_num_segments = random.randint(*num_links_range)

        self.build_morphology()

        self.weights = 2 * \
            np.random.rand(len(self.sensors), len(self.joints)) - 1

    def create_cube(self, name, size, direction, isSensor):
        pos = self.get_cube_pos(name, size, direction)

        self.links.append(Cube(name, pos, size, isSensor, direction))
        if isSensor:
            self.sensors.append(name)

    def get_cube_pos(self, name, size, direction):
        pos = [0, 0, 0]
        pos[direction] = size[direction] / 2

        if name == self.root:
            pos[2] = size[2] / 2
        return pos

    def create_joint(self, parent_name, child_name, size, old_direction, new_direction, jointAxis):
        pos = self.get_joint_pos(parent_name, size, old_direction, new_direction)

        self.joints.append(Joint(f'{parent_name}_{child_name}', parent_name, child_name, "revolute", pos, jointAxis, old_direction, new_direction))

    def get_joint_pos(self, parent_name, size, old_direction, new_direction):
        pos = [0, 0, 0]

        if self.root == parent_name and old_direction != 2:
            pos[2] = size[2] / 2

        pos[old_direction] += size[old_direction] / 2

        pos[new_direction] += size[new_direction] / 2
        return pos

    def build_morphology(self):
        dir = random.choice([0, 1, 2])
        self.root = ''.join(random.choices(string.ascii_lowercase, k=32))
        queue = [(dir, self.root)]
        self.build_node(queue)

    def build_node(self, queue):
        child_queue = []

        while len(queue) > 0:
            node = queue.pop(0)
            direction, name = node[0], node[1]

            features = self.random_features(direction)

            self.create_cube(
                name=name,
                direction=direction,
                size=features['size'],
                isSensor=features['isSensor']
            )

            for new_direction in features['newDirections']:
                if len(self.joints) < self.initial_num_segments - 1:
                    child_name = ''.join(random.choices(string.ascii_lowercase, k=32))

                    self.create_joint(
                        parent_name=name,
                        child_name=child_name,
                        old_direction=direction,
                        new_direction=new_direction,
                        size=features['size'],
                        jointAxis=features['jointAxis']
                    )

                    child_queue.append((new_direction, child_name))

        if len(child_queue) > 0:
            self.build_node(child_queue)

    def random_features(self, direction):
        is_sensor = random.random() < 0.5

        size = [0, 0, 0]
        for i in range(3):
            large_dim = i == direction or random.random() < 0.1
            size[i] = self.random_side_len(large_dim)

        joint_axis = [0, 0, 0]
        for i in range(3):
            joint_axis[i] = random.randint(0, 1)
        joint_axis = ' '.join(map(str, joint_axis))

        num_branches = random.choices([1, 2, 3], weights=[0.5, 0.25, 0.25])[0]

        direction_weights = [0.3] * 3
        direction_weights[direction] = 0.4

        new_directions = np.random.choice(
            [0, 1, 2], size=num_branches, replace=False, p=direction_weights)

        return {
            'size': size,
            'isSensor': is_sensor,
            'jointAxis': joint_axis,
            'newDirections': new_directions
        }

    def random_side_len(self, large_dim):
        if large_dim:
            new_min_length = max(self.min_side_len, 0.5 * self.max_side_len)
            return random.random() * (self.max_side_len - new_min_length) + new_min_length

        new_max_length = min(self.max_side_len, 2 * self.min_side_len)
        return random.random() * (new_max_length - self.min_side_len) + self.min_side_len

    def Mutate_Brain(self):
        if len(self.sensors) > 0 and len(self.joints) > 0:
            randomRow = random.randint(0, len(self.sensors) - 1)
            randomColumn = random.randint(0, len(self.joints) - 1)
            self.weights[randomRow][randomColumn] = 2 * random.random() - 1

    def Mutate_Body(self):
        to_change = random.choice(['joint', 'link', 'sensor'])

        if to_change == 'joint':
            change_type = random.choice(['direction', 'jointAxis', 'type'])
            random_joint = random.choice(self.joints)

            if change_type == 'jointAxis':
                self.change_joint_axis(random_joint)
            elif change_type == 'direction':
                self.change_direction(random_joint)
            elif change_type == 'type':
                self.change_type(random_joint)

        elif to_change == 'link':
            change_type = random.choice(['size', 'add', 'delete'])

            if change_type == 'size':
                random_link = random.choice(self.links)
                self.change_link_size(random_link)
            else:
                leaf_links = [link for link in self.links if not any(
                    joint.parent == link.name for joint in self.joints)]
                random_leaf_link = random.choice(leaf_links) if len(leaf_links) > 0 else None

                if change_type == 'add' and random_leaf_link and len(self.links) < self.max_num_segments:
                    self.add_link(random_leaf_link)
                elif change_type == 'delete' and random_leaf_link and len(self.links) > self.min_num_segments:
                    self.delete_link(random_leaf_link)

        elif to_change == 'sensor':
            random_link_1 = random.choice(self.links)
            random_link_2 = random.choice(self.links)

            self.swap_sensor_values(random_link_1, random_link_2)

    def change_joint_axis(self, random_joint):
        joint_axis = random_joint.jointAxis.split(' ')
        target_dim = random.randint(0, 2)
        joint_axis[target_dim] = '1' if joint_axis[target_dim] == '0' else '0'
        random_joint.jointAxis = ' '.join(joint_axis)

    def change_direction(self, random_joint):
        cur_new_direction = random_joint.new_direction
        desired_new_direction = random.choice([0, 1, 2])

        random_joint.new_direction = desired_new_direction
        parent_link = next(link for link in self.links if link.name == random_joint.parent)
        random_joint.pos = self.get_joint_pos(random_joint.parent, parent_link.size, random_joint.old_direction, random_joint.new_direction)

        child_link = next(link for link in self.links if link.name == random_joint.child)
        child_link.direction = desired_new_direction
        child_link.size[cur_new_direction], child_link.size[desired_new_direction] = child_link.size[desired_new_direction], child_link.size[cur_new_direction]
        child_link.pos = self.get_cube_pos(child_link.name, child_link.size, child_link.direction)

        next_joints = [joint for joint in self.joints if joint.parent == child_link.name]
        for next_joint in next_joints:
            next_joint.old_direction = desired_new_direction
            next_joint.pos = self.get_joint_pos(next_joint.parent, child_link.size, next_joint.old_direction, next_joint.new_direction)

    def change_type(self, random_joint):
        random_joint.type = random.choice(['revolute', 'fixed'])

    def change_link_size(self, random_link):
        random_dim = random.randint(0, 2)
        is_large_dim = random_link.direction == random_dim or random.random() < 0.1
        random_link.size[random_dim] = self.random_side_len(is_large_dim)

        random_link.pos = self.get_cube_pos(random_link.name, random_link.size, random_link.direction)

        joints_to_update = [joint for joint in self.joints if joint.parent == random_link.name]

        for joint in joints_to_update:
            joint.pos = self.get_joint_pos(joint.parent, random_link.size, joint.old_direction, joint.new_direction)

    def add_link(self, random_leaf_link):
        new_name = ''.join(random.choices(string.ascii_lowercase, k=32))

        new_direction = random.randint(0, 2)
        
        features = self.random_features(new_direction)

        self.create_joint(
            parent_name=random_leaf_link.name,
            child_name=new_name,
            old_direction=random_leaf_link.direction,
            new_direction=new_direction,
            size=random_leaf_link.size,
            jointAxis=features['jointAxis']
        )

        self.create_cube(
            name=new_name,
            direction=new_direction,
            size=features['size'],
            isSensor=features['isSensor']
        )

        self.weights = np.append(self.weights, np.random.uniform(-1, 1, (self.weights.shape[0], 1)), axis=1)

        if features['isSensor']:
            self.weights = np.append(self.weights, np.random.uniform(-1, 1, (1, self.weights.shape[1])), axis=0)


    def delete_link(self, random_leaf_link):
        self.links.remove(random_leaf_link)
        self.joints = [joint for joint in self.joints if joint.child != random_leaf_link.name]

        if random_leaf_link.isSensor:
            self.weights = np.delete(self.weights, self.sensors.index(random_leaf_link.name), axis=0)
            self.sensors.remove(random_leaf_link.name)

    def swap_sensor_values(self, random_link_1, random_link_2):
        if random_link_1.isSensor != random_link_2.isSensor:
            if random_link_1.isSensor:
                idx = self.sensors.index(random_link_1.name)
                self.sensors[idx] = random_link_2.name
            else:
                idx = self.sensors.index(random_link_2.name)
                self.sensors[idx] = random_link_1.name

            random_link_1.isSensor, random_link_2.isSensor = random_link_2.isSensor, random_link_1.isSensor
