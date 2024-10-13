# conda activate my-manim-environment
# manim -pql graph/scene.py VGraphVectors
from manim import *
from networkx import complete_graph


class VGraphAllAnimations(Scene):
    def construct(self):
        layouts = [
            "spring",
            "circular",
            "kamada_kawai",
            "planar",
            "random",
            "shell",
            "spectral",
            "spiral",
        ]
        vertices = [1, 2, 3]
        edges = [(1, 2), (2, 3)]
        g = Graph(vertices, edges, layout=layouts[0])

        self.play(Create(g))
        self.wait()
        self.origin_point = g.vertices[0].get_center()

        for i in range(1, len(layouts)):
            self.play(Transform(g, Graph(vertices, edges, layout=layouts[i])))
            self.wait()


class MovingAngle(Scene):
    def construct(self):
        rotation_center = LEFT

        theta_tracker = ValueTracker(110)
        line1 = Line(LEFT, RIGHT)
        line_moving = Line(LEFT, RIGHT)
        line_ref = line_moving.copy()
        line_moving.rotate(
            theta_tracker.get_value() * DEGREES, about_point=rotation_center
        )
        a = Angle(line1, line_moving, radius=0.5, other_angle=False)
        tex = MathTex(r"\theta").move_to(
            Angle(
                line1, line_moving, radius=0.5 + 3 * SMALL_BUFF, other_angle=False
            ).point_from_proportion(0.5)
        )

        self.add(line1, line_moving, a, tex)
        self.wait()

        line_moving.add_updater(
            lambda x: x.become(line_ref.copy()).rotate(
                theta_tracker.get_value() * DEGREES, about_point=rotation_center
            )
        )

        a.add_updater(
            lambda x: x.become(Angle(line1, line_moving, radius=0.5, other_angle=False))
        )
        tex.add_updater(
            lambda x: x.move_to(
                Angle(
                    line1, line_moving, radius=0.5 + 3 * SMALL_BUFF, other_angle=False
                ).point_from_proportion(0.5)
            )
        )

        self.play(theta_tracker.animate.set_value(40))
        self.play(theta_tracker.animate.increment_value(140))
        self.play(tex.animate.set_color(RED), run_time=0.5)
        self.play(theta_tracker.animate.set_value(350))


class VGraphVectors(VectorScene):
    def construct(self):
        plane = self.add_plane(animate=True).add_coordinates()

        vector = self.add_vector([-3, -2], color=YELLOW)

        basis = self.get_basis_vectors()
        self.add(basis)
        self.vector_to_coords(vector=vector)

        theta_tracker = ValueTracker(0)

        rotating_vector = Vector([2, 2], color=RED).rotate_about_origin(
            theta_tracker.get_value() * DEGREES
        )
        self.add(rotating_vector)

        rotating_vector.add_updater(
            lambda x: x.become(
                Vector([2, 2], color=RED).rotate_about_origin(
                    theta_tracker.get_value() * DEGREES
                )
            )
        )

        self.write_vector_coordinates(vector=rotating_vector)

        self.play(theta_tracker.animate.set_value(40), run_time=2)


class CompleteGraphAllAnimations(Scene):
    def construct(self):
        layouts = [
            "spring",
            "circular",
            "kamada_kawai",
            # "planar",
            "random",
            "shell",
            "spectral",
            "spiral",
        ]

        nxGraph = complete_graph(9)
        g = Graph.from_networkx(nxGraph, layout=layouts[0])

        self.play(Create(g))
        self.wait()

        for i in range(1, len(layouts)):
            self.play(Transform(g, Graph.from_networkx(nxGraph, layout=layouts[i])))
            self.wait()
