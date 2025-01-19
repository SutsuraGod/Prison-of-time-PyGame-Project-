from objects.projectile import Projectile


class Arrow(Projectile):
    def __init__(self, filename, spawn_pos, target_pos, normal_angle, groups):
        super().__init__(filename, spawn_pos, target_pos, normal_angle, *groups)

    def update(self):
        return super().update()
    
    def damage(self):
        return super().damage()